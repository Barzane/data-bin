# -*- coding: utf-8 -*-

import cPickle

import state_map
import parse_airport_state
import parse_temperature

def add(data_hold):
    
    parse_airport_state.parse()    
    parse_temperature.parse()    
    
    print
    print 'add temperature differential (Fahrenheit)'
    
    src_airport_state = '..\\temp\\airportState.bin'
    src_temperature = '..\\temp\\tavg.bin'
    
    f = open(src_temperature, 'rb')
    temp_dict = cPickle.load(f)
    f.close()

    f = open(src_airport_state, 'rb')
    state_dict = cPickle.load(f)
    f.close()
    
#    statemap = state_map.build()
#    
#    qm = {1: '01', 2: '04', 3: '07',4: '10'}            
#    
#    for key in data_hold:
#        
#        list_v = key.split('_')
#        origin = list_v[0]
#        destination = list_v[1]
#        year = list_v[3]
#        quarter = list_v[4]
#        
#        try:
#            
#            temp_dict[statemap[state_dict[origin]]][int(str(year) + qm[quarter])]
#            temp_dict[statemap[state_dict[destination]]][int(str(year) + qm[quarter])]
#            data_hold[key]['absTempDiff'] = abs(temp_dict[statemap[state_dict[origin]]][int(str(year) + qm[quarter])] - temp_dict[statemap[state_dict[destination]]][int(str(year) + qm[quarter])])
#            
#        except KeyError:
#            
#            data_hold[key]['absTempDiff'] = 'NA'    
    
    return data_hold
