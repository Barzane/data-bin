# -*- coding: utf-8 -*-

def add(data_hold, route_carrier):
    
    print
    print 'add distance'

    for key in data_hold:
        
        data_hold[key]['distance'] = route_carrier[key][0]    
    
    return data_hold
