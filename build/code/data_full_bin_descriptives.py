# -*- coding: utf-8 -*-

import cPickle, numpy, math

def weighted_avg_and_std(values, weights):

#        http://stackoverflow.com/questions/2413522/weighted-standard-deviation-in-numpy
    
    average = numpy.average(values, weights=weights)
    variance = numpy.average((values - average) ** 2, weights=weights)
    
    return (average, math.sqrt(variance))
        
def compute():

    src = '..\\output\\data_full.bin'
    
    try:
        
        f = open(src, 'rb')
        data = cPickle.load(f)
        f.close()
        
    except IOError:
        
        print
        print 'file not found', src
    
    print
    print 'descriptives:'
    
    print '\t', src
    
    southwest_routes = {}    
    year_list = []
    carrier_list = []
    route_list = []
    airport_list = []
    pax = {}
    southwest_pax = {}
    
    data_1999_2013 = {}

    pax_list = []
    distance_list = []
    pax_list_legacy = []
    distance_list_legacy = []
    pax_list_1999 = []
    distance_list_1999 = []
    pax_list_2013 = []
    distance_list_2013 = []
    pax_hhi = {}
    hhi = {}
    pax_hhi_legacy = {}
    hhi_legacy = {}
    pax_hhi_1999 = {}
    hhi_1999 = {}
    pax_hhi_2013 = {}
    hhi_2013 = {}
    
    legacy = ['AA', 'CO', 'DL', 'NW', 'TW', 'UA', 'US']
    
    for key in data:
        
        key_split = key.split('_')
        
        origin = key_split[0]
        destination = key_split[1]
        carrier = key_split[2]
        year = int(key_split[3])
        quarter = int(key_split[4]) 
        
        route = origin + '_' + destination
        
        if year not in southwest_routes:
            
            southwest_routes[year] = {}
            year_list.append(year)
            pax[year] = {}
            southwest_pax[year] = {}
            
        if quarter not in southwest_routes[year]:
            
            southwest_routes[year][quarter] = 0
            pax[year][quarter] = 0
            southwest_pax[year][quarter] = 0
        
        pax[year][quarter] += data[key]['pax']
        
        if quarter not in pax_hhi:
            
            pax_hhi[quarter] = []
            pax_hhi_legacy[quarter] = []
            pax_hhi_1999[quarter] = []
            pax_hhi_2013[quarter] = []
            
        if quarter not in hhi:
            
            hhi[quarter] = []
            hhi_legacy[quarter] = []
            hhi_1999[quarter] = []
            hhi_2013[quarter] = []
        
        if carrier == 'WN':
            
            southwest_routes[year][quarter] += 1
            southwest_pax[year][quarter] += data[key]['pax']

        if year >= 1999:
            
            data_1999_2013[key] = data[key]

        if carrier not in carrier_list:
            
            carrier_list.append(carrier)
            
        if route not in route_list:
            
            route_list.append(route)
            
        if origin not in airport_list:
            
            airport_list.append(origin)
            
        if destination not in airport_list:
            
            airport_list.append(destination)

        pax_list.append(data[key]['pax'])
        distance_list.append(data[key]['distance'])
        pax_hhi[quarter].append(data[key]['pax'])
        hhi[quarter].append(data[key]['hhiDB1B'])
        
        if carrier in legacy:
            
            pax_list_legacy.append(data[key]['pax'])
            distance_list_legacy.append(data[key]['distance'])
            pax_hhi_legacy[quarter].append(data[key]['pax'])
            hhi_legacy[quarter].append(data[key]['hhiDB1B'])
            
        if year == 1999:
            
            pax_list_1999.append(data[key]['pax'])
            distance_list_1999.append(data[key]['distance'])
            pax_hhi_1999[quarter].append(data[key]['pax'])
            hhi_1999[quarter].append(data[key]['hhiDB1B'])
            
        if year == 2013:
            
            pax_list_2013.append(data[key]['pax'])
            distance_list_2013.append(data[key]['distance'])
            pax_hhi_2013[quarter].append(data[key]['pax'])
            hhi_2013[quarter].append(data[key]['hhiDB1B'])

    year_list.sort()
    carrier_list.sort()
    route_list.sort()
    airport_list.sort()
    
    print    
    print 'number of Southwest routes by year-quarter:'
    
    for year in year_list:
        
        print '\t', year, southwest_routes[year]    
    
    southwest_route_list = []

    for year in southwest_routes:
        
        for quarter in southwest_routes[year]:
            
            item = southwest_routes[year][quarter]
            
            if item != 0:
                
                southwest_route_list.append(item)
    
    print
    print 'minimum number of Southwest routes by year-quarter:'
    
    print '\t', min(southwest_route_list)    
    
    print
    print 'maximum number of Southwest routes by year-quarter:'
    
    print '\t', max(southwest_route_list) 
        
    print
    print 'number of Southwest passengers by year-quarter:'
    
    for year in year_list:
        
        print '\t', year, southwest_pax[year]
    
    southwest_pax_percentage = []
    
    for year in southwest_routes:
        
        for quarter in southwest_routes[year]:
            
            item = 100 * float(southwest_pax[year][quarter]) / float(pax[year][quarter])
            
            if item != 0.0:
                
                southwest_pax_percentage.append(item)
    
    print
    print 'minimum % of Southwest pax (to total) by year-quarter:'
    
    print '\t', min(southwest_pax_percentage)    
    
    print
    print 'maximum % of Southwest pax (to total) by year-quarter:'
    
    print '\t', max(southwest_pax_percentage) 
    
    print
    print 'retaining years >= 1999'
    
    data = data_1999_2013
    
    del data_1999_2013
    
    print
    print 'number of observations (route-carrier-quarters):'
    
    print '\t', len(data)
    
    print
    print 'number of carriers:'
    
    print '\t', len(carrier_list)
    
#    print
#    print carrier_list
    
    print
    print 'number of routes:'
    
    print '\t', len(route_list)
    
    print
    print 'number of airports:'
    
    print '\t', len(airport_list)
    
#    print
#    print airport_list
    
    print
    print '[full sample] pax weighted mean distance (miles) and biased std. dev.:'

    print '\t', weighted_avg_and_std(distance_list, pax_list)
    
    print
    print '[legacy] pax weighted mean distance (miles) and biased std. dev.:'

    print '\t', weighted_avg_and_std(distance_list_legacy, pax_list_legacy)

    print
    print '[1999] pax weighted mean distance (miles) and biased std. dev.:'

    print '\t', weighted_avg_and_std(distance_list_1999, pax_list_1999)    
    
    print
    print '[2013] pax weighted mean distance (miles) and biased std. dev.:'

    print '\t', weighted_avg_and_std(distance_list_2013, pax_list_2013)
    
    print
    print '[full sample] pax weighted mean HHI and biased std. dev.:'
    
    for quarter in hhi:
        
        print '\t', quarter, weighted_avg_and_std(hhi[quarter], pax_hhi[quarter]) 

    print
    print '[legacy] pax weighted mean HHI and biased std. dev.:'
    
    for quarter in hhi:
        
        print '\t', quarter, weighted_avg_and_std(hhi_legacy[quarter], pax_hhi_legacy[quarter])

    print
    print '[1999] pax weighted mean HHI and biased std. dev.:'
    
    for quarter in hhi:
        
        print '\t', quarter, weighted_avg_and_std(hhi_1999[quarter], pax_hhi_1999[quarter])
     
    print
    print '[2013] pax weighted mean HHI and biased std. dev.:'
    
    for quarter in hhi:
        
        print '\t', quarter, weighted_avg_and_std(hhi_2013[quarter], pax_hhi_2013[quarter])
             
    return None

compute()

    