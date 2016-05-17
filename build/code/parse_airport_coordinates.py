# -*- coding: utf-8 -*-

#Key: IATA code. Value: ['Airport (Country)', [latitude, longitude]].
#coordinates in degrees, not radians.

import csv, cPickle, shutil

def parse():
    
    print 'parse airport coordinates'
    
    src = '..\\..\\data\\Coordinates\\airport_locations.csv'
    dst = '..\\input\\airport_locations.csv'   
    dst_bin = '..\\temp\\airport_location_degrees.bin'   
    
    print '\ncopying population data from \\data\\Coordinates to \\input'
    
    shutil.copy(src, dst)
    
    f = open(dst, 'r')
    reader = csv.reader(f)
    
    airport_location_dict = {}
    
    print '\nparsing ' + dst
    
    for row in reader:
        
        element1 = row[1] + ' (' + row[3] + ')'
        element2 = [float(row[5]), float(row[6])]
        
        airport_location_dict[row[0]] = [element1, element2]

    f.close()
    
    print '\nillustrative data: ', airport_location_dict['ORD']
    
    print '\nsaving ' + dst_bin
          
    f = open(dst_bin, 'wb')
    cPickle.dump(airport_location_dict, f)
    f.close()
    
    return None
