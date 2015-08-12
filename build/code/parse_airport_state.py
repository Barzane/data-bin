# -*- coding: utf-8 -*-

import cPickle, shutil

def parse():
    
    src = '..\\..\\data\\AirportState\\airportStateCSV.csv'
    dst = '..\\input\\airportStateCSV.csv'   
    dst_airport_state_bin = '..\\temp\\airportState.bin'   
    
    print 'copying airport state data'
    print 'from', src
    print 'to', dst
    
    shutil.copy(src, dst)
    
    print 'parsing airport state data, save .bin to \\temp'    
    
    f = open(dst, 'r')
    
    airport_state_dict = {}

    for line in f:
        
        data = line.split(';')
        
        if data[0] not in airport_state_dict:
            
            airport_state_dict[data[0]] = data[2].strip()
    
    f.close()
    
    del airport_state_dict['airport']
        
    f = open(dst_airport_state_bin, 'wb')
    cPickle.dump(airport_state_dict, f)
    f.close()

    return None
