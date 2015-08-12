# -*- coding: utf-8 -*-

import cPickle

def find(code):
    """
    Return coordinates corresponding to airport IATA code
    """

    try:
        
        airport_location_degrees_dict
        
    except NameError:
        
        src_airport_location = '..\\temp\\airport_location_degrees.bin'

        f = open(src_airport_location, 'rb')
        airport_location_degrees_dict = cPickle.load(f)
        f.close()

    try:
        
        return tuple(airport_location_degrees_dict[code][1])
        
    except KeyError:
        
        return None
