# -*- coding: utf-8 -*-

import cPickle, shutil, glob

def parse():
    
    src_temperature_path = '..\\..\\data\\Climate\\'
    src_temperature = src_temperature_path + '*.txt'
    dst_temperature_path = '..\\input\\'
    
    print
    print 'copying temperature data'
    print
    
    dst_temperature_all = []    
    
    for src_temperature_state in glob.glob(src_temperature):
        
        state_name = src_temperature_state.split(src_temperature_path)[1]
        dst_temperature = dst_temperature_path + state_name
        
        dst_temperature_all.append(dst_temperature)        
        
        print 'from', src_temperature_state
        print 'to', dst_temperature
    
        shutil.copy(src_temperature_state, dst_temperature)
    
    print
    print 'parsing temperature data, save .bin to \\temp'
    print
    
    data_dict = {}
    
    for name in dst_temperature_all:
        
        print name

        f = open(name)
        
        header = f.readline().split(',')
        header = [i.strip() for i in header]
        
        state_index = header.index('StateCode')
        year_month_index = header.index('YearMonth')
        temp_index = header.index('TAVG')
        
        first = True
        
        for line in f:
            
            data = line.split(',')
            data = [i.strip() for i in data]
        
            if first:
                
                state = data[state_index]
                data_dict[state] = {}
                
                first = False
            
            if data[year_month_index] not in data_dict[state]:
                
                data_dict[state][int(data[year_month_index])] = float(data[temp_index])
        
        f.close()
    
    dst_temperature_parsed = '..\\temp\\tavg.bin'

    f=open(dst_temperature_parsed, 'wb')
    cPickle.dump(data_dict, f)
    f.close()

    return None
    