# -*- coding: utf-8 -*-

import copy

def add(data_hold):
    
    print
    print 'add airport market share'
    
    airport_pax = {}
    airport_carrier_pax_share = {}
    
    for kk in data_hold:
        
        list_v = kk.split('_')
        origin = list_v[0]
        destination = list_v[1]
        carrier = list_v[2]
        
        if origin not in airport_pax:
            
            airport_pax[origin] = data_hold[kk]['pax']
            
        else:
            
            airport_pax[origin] += data_hold[kk]['pax']
        
        if destination not in airport_pax:
            
            airport_pax[destination] = data_hold[kk]['pax']
            
        else:
            
            airport_pax[destination] += data_hold[kk]['pax']
            
        if origin not in airport_carrier_pax_share:
            
            airport_carrier_pax_share[origin] = {}
            
        if destination not in airport_carrier_pax_share:
            
            airport_carrier_pax_share[destination] = {}
            
        if carrier not in airport_carrier_pax_share[origin]:
            
            airport_carrier_pax_share[origin][carrier] = data_hold[kk]['pax']
            
        else:
            
            airport_carrier_pax_share[origin][carrier] += data_hold[kk]['pax']
        
        if carrier not in airport_carrier_pax_share[destination]:
            
            airport_carrier_pax_share[destination][carrier] = data_hold[kk]['pax']
            
        else:
            
            airport_carrier_pax_share[destination][carrier] += data_hold[kk]['pax']
    
    airport_market_share = copy.deepcopy(airport_carrier_pax_share)
    
    for airport in airport_carrier_pax_share:
        
        for carrier in airport_carrier_pax_share[airport]:
            
            airport_market_share[airport][carrier] =\
                float(airport_carrier_pax_share[airport][carrier]) / airport_pax[airport]
    
    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        carrier = list_v[2]
            
        data_hold[key]['marketShareOrigin'] = airport_market_share[origin][carrier]
        data_hold[key]['marketShareDest'] = airport_market_share[destination][carrier]          
           
    return data_hold
        