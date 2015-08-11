# -*- coding: utf-8 -*-

import cPickle, copy

import add_distance
import filter_t100_volume
import add_mean_fares
import add_percentiles
import add_passengers
import add_t100
import add_population
import add_herfindahl

def build(year, quarter):
    
    src_t100 = '..\\temp\\T100_merge_' + str(year) + '.bin'
    src_route_carrier = '..\\temp\\routecarrier_' + str(year) + '_' + str(quarter) + '.bin'

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
    
    return data_hold
    
def wrapper(test_run, test_periods, full_periods, security = None, security_max = None):
        
    if test_run:
        
        year_list = test_periods[0]
        quarter_list = test_periods[1]
        
    else:
                
        year_list = full_periods[0]
        quarter_list = full_periods[1]
    
    for year in year_list:
        
        for quarter in quarter_list:
            
            try:
                                
                data_hold = build(year, quarter)
                    
            except IOError:
    
                raise IOError('requested data unavailable: year ' + str(year) + ' , quarter ' + str(quarter))
    
            var_list = copy.deepcopy(data_hold[data_hold.keys()[0]].keys())
            var_list.sort()
    
            dst_data = '..\\output\\data_' + str(year) + '_' + str(quarter) + '.bin'  
    
            f = open(dst_data, 'wb')
            cPickle.dump(data_hold, f)
            f.close()
    
    return None
