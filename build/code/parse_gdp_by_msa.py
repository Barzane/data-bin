# -*- coding: utf-8 -*-

import cPickle, copy, shutil

def parse():
    
    src = '..\\..\\data\\GDP\\gdpDataFinal.txt'
    dst = '..\\input\\gdpDataFinal.txt'   
    dst_bin = '..\\temp\\gdp_by_msa_dict.bin'   
    
    print 'copying GDP data from \\data\\GDP to \\input'
    
    shutil.copy(src, dst)
    
    print 'opening ' + dst

    f = open(dst, 'r')
    
    header = f.readline()
    header = header.split('\t')
    
    msa_location = {}
    
    for line in f:
        
        a = line.split('\t')
        
        hold_dict = {}
        
        for year in range(1990, 2014):
            
            latitude = float(a[-2].strip().replace(',', '.'))
            longitude = float(a[-1].strip().replace(',', '.'))
            
            hold_dict[year] = float(a[header.index(str(year))].replace(',', '.'))
            msa_location[(latitude, longitude)] = copy.deepcopy(hold_dict)
    
    f.close()
    
    print 'saving ' + dst_bin
    
    f = open(dst_bin, 'wb')
    cPickle.dump(msa_location, f)
    f.close() 

    return None