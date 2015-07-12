# -*- coding: utf-8 -*-

#   Raw data from ftp://ftp.bls.gov/pub/special.requests/cpi/cpiai.txt
#   U.S. Department of Labor, Consumer Price Index, All Urban Consumers
#
#   Syntax e.g. 300*CPI2013Q4Dict['2002_2'] gives 388.63 (2 d.p.)
#   i.e. 2002Q2$300 is equivalent to 2013Q4$388.63
#   and CPI2013Q4Dict['2002_2'] gives 1.30 (2 d.p.), indicating
#   that prices increased by 30% between 2002Q2 and 2013Q4.

import cPickle, shutil

def parse():
    
    src = '..\\..\\data\\ConsumerPriceIndex\\CPIUrbanMonthly.txt'
    dst = '..\\input\\CPIUrbanMonthly.txt'   
    dst_cpi_bin = '..\\temp\\CPI2013Q4_dict.bin'   
    
    print 'copying CPI data from \\data\\ConsumerPriceIndex to \\input'
    
    shutil.copy(src, dst)
    
    print 'parsing CPI data, save .bin to \\temp'    
    
    f = open(dst, 'r')
    
    header = f.readline().strip().split()
    
    inflation_dict = {}
    
    for i in f:
        
        j = i.strip().split()[:13]
        
        inflation_dict[j[0]+'_1'] = eval(j[3])
        inflation_dict[j[0]+'_2'] = eval(j[6])
        inflation_dict[j[0]+'_3'] = eval(j[9])
        inflation_dict[j[0]+'_4'] = eval(j[12])
    
    f.close()
    
    CPI2013Q4_dict = {}
    
    for yq in inflation_dict.keys():
        
        CPI2013Q4_dict[yq] = inflation_dict['2013_4'] / float(inflation_dict[yq])
    
    f = open(dst_cpi_bin, 'wb')
    cPickle.dump(CPI2013Q4_dict, f)
    f.close()
    
    print 'CPI2013Q4_dict *returned directly* to merge_coupon_ticket.py (not loaded from \\temp)'
    
    return CPI2013Q4_dict
