# -*- coding: utf-8 -*-

def add(data_hold, t_count):
    
    print
    print 'add time'

    for key in data_hold:
        
        data_hold[key]['time'] = t_count    
    
    return data_hold
