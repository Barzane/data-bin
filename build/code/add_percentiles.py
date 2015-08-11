# -*- coding: utf-8 -*-

import scipy

def add(data_hold, route_carrier, percentile_list):
    
    print
    print 'add percentile fares', percentile_list

    for key in data_hold:
        
        for perc in percentile_list:        
        
            data_hold[key]['p' + str(perc) + 'Fare'] = scipy.percentile(route_carrier[key][1], perc)
            data_hold[key]['p' + str(perc) + 'RealFare'] = scipy.percentile(route_carrier[key][2], perc)
    
    return data_hold
