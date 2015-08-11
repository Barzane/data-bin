# -*- coding: utf-8 -*-

def add(data_hold, T100):
    
    print
    print 'add T-100 variables'

    for key in data_hold:
        
        data_hold[key]['T100pax'] = int(T100[key]['PASSENGERS'])
        data_hold[key]['T100seats'] = int(T100[key]['SEATS'])
        data_hold[key]['T100loadfactor'] = T100[key]['LOAD_FACTOR']
        data_hold[key]['T100airtime'] = T100[key]['MEAN_AIR_TIME']
        data_hold[key]['T100ramptoramptime'] = T100[key]['MEAN_RAMP_TO_RAMP']
        
    return data_hold
