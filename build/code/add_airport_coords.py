# -*- coding: utf-8 -*-

import find_iata_code

def add(data_hold):
    
    print
    print 'add airport coordinates (degrees)'
    
    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        
        airport_coords_origin = find_iata_code.find(origin)
    
        if airport_coords_origin is None:
            
            data_hold[key]['originLatitude'] = 'NA'
            data_hold[key]['originLongitude'] = 'NA'
            
        else:
            
            data_hold[key]['originLatitude'] = airport_coords_origin[0]
            data_hold[key]['originLongitude'] = airport_coords_origin[1]                
    
        airport_coords_destination = find_iata_code.find(destination)
    
        if airport_coords_destination is None:
            
            data_hold[key]['destinationLatitude'] = 'NA'
            data_hold[key]['destinationLongitude'] = 'NA'
            
        else:
            
            data_hold[key]['destinationLatitude'] = airport_coords_destination[0]
            data_hold[key]['destinationLongitude'] = airport_coords_destination[1]          
           
    return data_hold
 