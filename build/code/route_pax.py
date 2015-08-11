# -*- coding: utf-8 -*-

def build_hhi_dict_db1b(data_hold):
            
    hhi_dict_db1b = {}

    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        
        if origin + '_' + destination not in hhi_dict_db1b:
            
            hhi_dict_db1b[origin + '_' + destination] = [data_hold[key]['pax']]
            
        else:
            
            hhi_dict_db1b[origin + '_' + destination].append(data_hold[key]['pax'])           
    
    return hhi_dict_db1b
