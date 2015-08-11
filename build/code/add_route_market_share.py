# -*- coding: utf-8 -*-

import scipy

import route_pax
            
def add(data_hold):
    
    print
    print 'add route market share' 

    hhi_dict_db1b = route_pax.build_hhi_dict_db1b(data_hold)
            
    market_share_dict = {}

    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        carrier = list_v[2]
        
        if origin + '_' + destination + '_' + carrier not in market_share_dict:
            
            market_share_dict[origin + '_' + destination + '_' + carrier] =\
                scipy.array(data_hold[key]['pax']) / float(sum(scipy.array(hhi_dict_db1b[origin + '_' + destination])))
        else:
            
            raise KeyError('repeated key')
    
    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        carrier = list_v[2]

        data_hold[key]['marketShareRoute'] = market_share_dict[origin + '_' + destination + '_' + carrier]

    return data_hold
