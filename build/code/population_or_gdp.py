# -*- coding: utf-8 -*-

#Compute U.S. airport local population from MSA data
#
#1. MSA populations given by 1990, 2000, 2010 U.S. Census
#    (linear interpolation / extrapolation)
#2. Each MSA linked to coordinates of first-listed city/town
#3. Each airport (IATA code) linked to coordinates
#4. Given airport, search across all MSAs
#5. If MSA within 50 miles of airport, record population
#
#The syntax is as follows:
#
#    import population
#    a = population.local_population('LGA')
#
#If a is None returns False, we can use a (for LGA this returns 19813938)
#
#If a is None returns True, then the IATA code is not valid
#    e.g. a = population.local_population('bert')
#
#Once a valid IATA code has been requested, all
#subsequent calls will return directly from a results dictionary,
#and no further computation will be required.
#For this reason - and for simplicity - the local threshold
#of 50 (in whatever units are chosen) has been hard-coded.
#
#In some cases, a valid airport code will have no local population
#(computed using U.S. MSA data), and in this case the function
#will return the value 0, e.g. a = population.local_population('LHR')

import cPickle, scipy

#dictionary will contain IATA code: {year: population}
#(subsequent calls of a given IATA code will not recompute population)

src_msa = '../temp/population_by_msa_dict.bin'
src_airport = '../temp/airport_location_degrees.bin'

#Load MSA geographical coordinates and populations

f = open(src_msa, 'rb')
population_by_msa_dict = cPickle.load(f)
f.close()

#Load airport (IATA code) geographical coordinates

f = open(src_airport, 'rb')
airport_location_degrees = cPickle.load(f)
f.close()
    
population_dict = {}

def local_population(test_airport):
    """
    Compute local population to airport IATA code.
    """
    
    def find_iata(code):
        """
        Returns coordinates corresponding to airport IATA code.
        """
    
        try:
            
            return tuple(airport_location_degrees[code][1])
            
        except KeyError:
            
            return None
    
    def distance_fn(p1, l1, p2, l2, units='m'):
        """
        Simplified Vincenty formula.
        Returns distance between coordinates.
        """
    
        assert (units in ['km', 'm', 'nm']), 'Units must be km, m, or nm'
    
        if units == 'km':
            
            r = 6372.7974775959065
            
        elif units == 'm':
            
            r = 6372.7974775959065 * 0.621371
            
        elif units == 'nm':
            
            r = 6372.7974775959065 * 0.539957
    
    #    compute Vincenty formula
    
        l = abs(l1 - l2)
        num = scipy.sqrt(((scipy.cos(p2) * scipy.sin(l)) ** 2) +\
            (((scipy.cos(p1) * scipy.sin(p2)) - (scipy.sin(p1) * scipy.cos(p2) * scipy.cos(l))) ** 2))
        den = scipy.sin(p1) * scipy.sin(p2) + scipy.cos(p1) * scipy.cos(p2) * scipy.cos(l)
        theta = scipy.arctan(num / den)
        distance = abs(int(round(r * theta)))
    
        return distance

#    neighbourhood fixed at 50 (default: m; otherwise, km or nm)

    radius = 50

#    search for IATA code in dictionary
#    if found, return local population directly
#    if not found, compute local population
    
    try:
        
        return population_dict[test_airport]
        
    except KeyError:
        
        airport_coords = find_iata(test_airport)

        if airport_coords is None:
            
            return None

        else:

            population_dict[test_airport] = {}

#            convert decimal coordinates to radians
            
            p1 = (scipy.pi / 180) * airport_coords[0]
            l1 = (scipy.pi / 180) * airport_coords[1]

            for year in range(1990, 2014):

#                initialize cumulative local population
                
                population_sum = 0
    
#                loop across all MSAs
    
                for msa_coords in population_by_msa_dict:
    
#                    convert decimal coordinates to radians
                    
                    p2 = (scipy.pi / 180) * msa_coords[0]
                    l2 = (scipy.pi / 180) * msa_coords[1]
    
#                    compute distance between airport and MSA
    
                    distance = distance_fn(p1, l1, p2, l2)
                    
#                    if MSA and airport are local, add population
                    
                    if distance <= radius:
                        
                        population_sum += population_by_msa_dict[msa_coords][year]
    
                population_dict[test_airport][year] = population_sum

            return population_dict[test_airport]
