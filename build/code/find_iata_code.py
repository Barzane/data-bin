# -*- coding: utf-8 -*-

import cPickle

src_airport_location = '..\\temp\\airport_location_degrees.bin'

f = open(src_airport_location, 'rb')
airport_location_degrees_dict = cPickle.load(f)
f.close()
        
def find(code):
    """
    Return coordinates corresponding to airport IATA code
    """

    try:
        
        return tuple(airport_location_degrees_dict[code][1])
        
    except KeyError:
        
        return None
