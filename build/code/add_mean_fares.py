# -*- coding: utf-8 -*-

import scipy

def add(data_hold, route_carrier):
    
    print
    print 'add mean fares'

    for key in data_hold:
        
        data_hold[key]['meanFare'] = scipy.mean(route_carrier[key][1])
        data_hold[key]['meanRealFare'] = scipy.mean(route_carrier[key][2])    
    
    return data_hold
