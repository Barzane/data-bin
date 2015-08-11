# -*- coding: utf-8 -*-

import scipy

def build_hhi_dict_db1b(data_hold):
            
    hhi_dict_db1b = {}

    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        carrier = list_v[2]
        
        if origin + '_' + destination not in hhi_dict_db1b:
            
            hhi_dict_db1b[origin + '_' + destination] = [data_hold[key]['pax']]
            
        else:
            
            hhi_dict_db1b[origin + '_' + destination].append(data_hold[key]['pax'])           
    
    return hhi_dict_db1b
            
def add(data_hold):
    
    print
    print 'add Herfindahl index' 

    hhi_dict_db1b = build_hhi_dict_db1b(data_hold)
    
    hhi_dict_db1b_2 = {}

    for key in hhi_dict_db1b:
        
        hhi_dict_db1b_2[key] = sum((scipy.array(hhi_dict_db1b[key]) / float(sum(scipy.array(hhi_dict_db1b[key])))) ** 2)
    
    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        
        data_hold[key]['hhiDB1B'] = hhi_dict_db1b_2[origin + '_' + destination]
   
    return data_hold
        