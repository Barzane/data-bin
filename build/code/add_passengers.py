# -*- coding: utf-8 -*-

def add(data_hold, route_carrier):
    
    print
    print 'add passengers (pax)'

    for key in data_hold:
        
        data_hold[key]['pax'] = len(route_carrier[key][1])
        
    return data_hold
     