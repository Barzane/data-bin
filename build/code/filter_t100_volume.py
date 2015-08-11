# -*- coding: utf-8 -*-

import copy

def filter(data_hold, T100):
    
    print
    print 'remove DB1B route-carrier-quarters with low T-100 volume, or that are missing from T-100'

    found_key_count = 0
    missing_key_count = 0
        
    a = copy.deepcopy(data_hold.keys())
    
    for key in a:
        
        try:
            
            T100[key]
            
            if int(T100[key]['PASSENGERS']) >= 2000 and int(T100[key]['SEATS']) >= 2000:
                
                found_key_count += 1
                
            else:
                
                missing_key_count += 1
                del data_hold[key]
                
        except KeyError:
            
            missing_key_count += 1
            del data_hold[key]

    print '...keys retained', found_key_count, '(', 100 * float(found_key_count) / (found_key_count + missing_key_count), '% )'
    print '...keys dropped', missing_key_count, '(', 100 * float(missing_key_count) / (found_key_count + missing_key_count), '% )'                  
    
    return data_hold
