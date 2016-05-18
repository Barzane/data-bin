# -*- coding: utf-8 -*-

import cPickle

import add_distance
import filter_t100_volume
import add_mean_fares
import add_percentiles
import add_passengers
import add_t100
import add_population
import add_herfindahl
import add_route_market_share
import add_temperature
import add_airport_market_share
import add_gdp
import add_southwest_indicator
import add_airport_coords
import add_large_airport
import add_time

def build(year, quarter, t_count):
    
    print 'filter + add variables to data dictionary'
    
    src_t100 = '..\\temp\\T100_merge_' + str(year) + '.bin'
    src_route_carrier = '..\\temp\\routecarrier_' + str(year) + '_' + str(quarter) + '.bin'
    src_cpi = '..\\temp\\CPI2013Q4_dict.bin'
    
    print '\nloading' + src_cpi

    f = open(src_cpi, 'rb')
    CPI2013Q4Dict = cPickle.load(f)
    f.close()    
    
    print 'loading ' + src_t100
    
    f = open(src_t100, 'rb')
    T100 = cPickle.load(f)
    f.close()
    
    print 'loading ' + src_route_carrier
    
    f = open(src_route_carrier, 'rb')
    route_carrier = cPickle.load(f)
    f.close()
    
    data_hold = dict([item, {}] for item in route_carrier)
    
    data_hold = filter_t100_volume.filter(data_hold, T100)    
    data_hold = add_distance.add(data_hold, route_carrier)    
    data_hold = add_mean_fares.add(data_hold, route_carrier)     
    data_hold = add_percentiles.add(data_hold, route_carrier, [25, 75, 50, 10, 90])
    data_hold = add_passengers.add(data_hold, route_carrier)
    data_hold = add_t100.add(data_hold, T100)    
    data_hold = add_population.add(data_hold)    
    data_hold = add_herfindahl.add(data_hold)
    data_hold = add_route_market_share.add(data_hold)    
    data_hold = add_temperature.add(data_hold)
    data_hold = add_airport_market_share.add(data_hold)    
    data_hold = add_gdp.add(data_hold, CPI2013Q4Dict)
    data_hold = add_southwest_indicator.add(data_hold)
    data_hold = add_airport_coords.add(data_hold)
    data_hold = add_large_airport.add(data_hold)
    
    sss
    
    data_hold = add_time.add(data_hold, t_count)
    
    return data_hold
    
def wrapper(test_run, test_periods, full_periods, security = None, security_max = None):
        
    if test_run:
        
        year_list = test_periods[0]
        quarter_list = test_periods[1]
        
    else:
                
        year_list = full_periods[0]
        quarter_list = full_periods[1]
    
    t_count = 0    
    
    for year in year_list:
        
        for quarter in quarter_list:
            
            try:
                                
                data_hold = build(year, quarter, t_count)
                    
            except IOError:
    
                raise IOError('data unavailable: year ' + str(year) + ' , quarter ' + str(quarter))
    
            dst_data = '..\\output\\data_' + str(year) + '_' + str(quarter) + '.bin'  

            print 'saving', dst_data
            print
    
            f = open(dst_data, 'wb')
            cPickle.dump(data_hold, f)
            f.close()
            
            t_count += 1
    
    return None
