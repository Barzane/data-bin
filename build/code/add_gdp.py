# -*- coding: utf-8 -*-

import math

import population_or_gdp

def add(data_hold, CPI2013Q4Dict):
    
    print
    print 'add GDP'

    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]            
        year = int(list_v[3])
        quarter = int(list_v[4])
    
        a = population_or_gdp.local_gdp(origin)

        if (a is not None):
            
            pass
        
        else:
            
            raise Exception(origin)
        
        b = population_or_gdp.local_gdp(destination)
        
        if (b is not None):
            
            pass
        
        else:
            
            raise Exception(destination)
        
        if (a is not None) and (b is not None):
            
            geomean = math.sqrt(float(a[year]) * b[year])
            max_gdp = max(a[year], b[year])
            geo_mean_real = geomean * CPI2013Q4Dict[str(year) + '_' + str(quarter)]
            max_gdp_real = max_gdp * CPI2013Q4Dict[str(year) + '_' + str(quarter)]
            
            data_hold[key]['meanGDP'] = geo_mean_real
            data_hold[key]['maxGDP'] = max_gdp_real
    
        aP = population_or_gdp.local_population(origin)

        if (aP is not None):
            
            pass
        
        else:
            
            raise Exception(origin)
        
        bP = population_or_gdp.local_population(destination)
        
        if (bP is not None):
            
            pass
        
        else:
            
            raise Exception(destination)
        
        if (a is not None) and (b is not None) and (aP is not None) and (bP is not None):
            
            try:
                
                gdp_per_capita_origin = float(a[year]) / float(aP[year])
                gdp_per_capita_dest = float(b[year]) / float(bP[year])
                geomean_gdp_per_capita = math.sqrt(gdp_per_capita_origin * gdp_per_capita_dest)
                data_hold[key]['meanGDPperCapita'] = geomean_gdp_per_capita * CPI2013Q4Dict[str(year) + '_' + str(quarter)]
                
            except ZeroDivisionError:
                
                data_hold[key]['meanGDPperCapita'] = 'NA'
        
    return data_hold
    