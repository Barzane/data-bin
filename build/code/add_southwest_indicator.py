# -*- coding: utf-8 -*-

def add(data_hold):
    
    print
    print 'add Southwest presence indicator'

    wn_present_list = []
        
    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        carrier = list_v[2]
        
        route = origin + '_' + destination
        
        if carrier == 'WN':
            
            wn_present_list.append(route)

    wn_present_list.sort()

    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        
        route = origin + '_' + destination
        
        if route in wn_present_list:
            
            data_hold[key]['WNpresence'] = 1
            
        else:
            
            data_hold[key]['WNpresence'] = 0
                    
    return data_hold
        