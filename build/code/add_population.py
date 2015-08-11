# -*- coding: utf-8 -*-

import math

import population_or_gdp

def add(data_hold):
    
    print
    print 'add population'

    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]           
        year = int(list_v[3])
    
        a = population_or_gdp.local_population(origin)

        if (a is not None):
            
            pass
        
        else:
            
            print 'error', origin
        
        b = population_or_gdp.local_population(destination)
        
        if (b is not None):
            
            pass
        
        else:
            
            print 'error', destination
        
        if (a is not None) and (b is not None):
            
            geo_mean = math.sqrt(float(a[year]) * b[year])
            max_pop = max(a[year], b[year])
            data_hold[key]['meanPopulation'] = geo_mean
            data_hold[key]['maxPopulation'] = max_pop
        
    return data_hold
 