# -*- coding: utf-8 -*-

import cPickle

def merge(src_data, yyyy, q, full_data):
    
    print 'merge .bin files'
    
    print '\n[loading]', src_data
        
    f = open(src_data, 'r')
    data = cPickle.load(f)
    f.close()

#    http://stackoverflow.com/questions/38987/how-can-i-merge-two-python-dictionaries-in-a-single-expression
        
    full_data.update(data)
    
    del data    
        
    return full_data

def wrapper(test_run, test_periods, full_periods, security = None, security_max = None):
    
    full_data = {}
    
    if test_run:
        
        year_list = test_periods[0]
        quarter_list = test_periods[1]
        
    else:
                
        year_list = full_periods[0]
        quarter_list = full_periods[1]    
    
    for year in year_list:
        for quarter in quarter_list:

            src_data = '..\\output\\data_' + str(year) + '_' + str(quarter) + '.bin'
            
            try:
                            
                full_data = merge(src_data, year, quarter, full_data)
                
            except IOError:

                raise IOError('requested data unavailable: year ' + str(year) + ', quarter ' + str(quarter))
    
    dst_full_data = '..\\output\\data_full.bin'    
    
    print
    print '[saving]', dst_full_data    
    
    f = open(dst_full_data, 'wb')
    cPickle.dump(full_data, f)
    f.close()

    del full_data
       
    return None