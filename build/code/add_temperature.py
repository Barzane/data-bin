# -*- coding: utf-8 -*-

import cPickle

import state_map
import parse_airport_state

def add(data_hold):
    
    parse_airport_state.parse()    
    
    print
    print 'add temperature differential (Fahrenheit)'
    
#    f = open('../Climate/tavg.bin', 'rb')
#    temp_dict = cPickle.load(f)
#    f.close()
#
#    f = open('../Climate/airportState.bin', 'rb')
#    state_dict = cPickle.load(f)
#    f.close()
#    
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
