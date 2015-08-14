# -*- coding: utf-8 -*-

import cPickle, sets, scipy

def compute(year, quarter):

    src = '..\\temp\\coupon_' + str(year) + '_' + str(quarter) + '.bin'
    
    try:
        
        f = open(src, 'rb')
        coupon = cPickle.load(f)
        f.close()
        
    except IOError:
        
        print
        print 'file not found', src
    
    print
    print 'descriptives:'
    
    print '\t', src
    
    print    
    print 'keys:'
    
    for key in coupon:
        print '\t', key
    
    print    
    print 'number of itineraries:'
    
    print '\t', len(coupon[key])
    
    print    
    print 'number of passengers:'
    
    passenger_count = 0
    
    for item in coupon['Passengers']:
        
        passenger_count += item
        
    print '\t', int(passenger_count)
    
    print    
    print 'operating carriers:'
    
    op_carrier_list = []
    
    for item in coupon['OpCarrier']:
    
        if item not in op_carrier_list:
            
            op_carrier_list.append(item)
    
    op_carrier_list.sort()

    for carrier in op_carrier_list:
        
        print '\t', carrier
    
    print    
    print 'number of operating carriers:'
    
    print '\t', len(op_carrier_list)
    
    print    
    print 'number of origin airports:'    
    
    origin_list = []
    
    for item in coupon['Origin']:
        
        if item not in origin_list:
            
            origin_list.append(item)
            
    print '\t', len(origin_list)
    
    print    
    print 'number of destination airports:'
    
    dest_list = []
    
    for item in coupon['Dest']:
        
        if item not in dest_list:
            
            dest_list.append(item)
            
    print '\t', len(dest_list)
    
    print    
    print 'origin versus destination airports:'
    
    for origin in origin_list:
        
        if origin not in dest_list:
            
            print '\t', origin, 'Origin not a Dest'
            
    for dest in dest_list:
        
        if dest not in origin_list:
            
            print '\t', dest, 'Dest not an Origin'
    
    print    
    print 'number of unique airports:'
    
    all_airports_list = origin_list + dest_list    
    unique_airports = sets.Set(all_airports_list)
    unique_airports_list = list(unique_airports)
    
    print '\t', len(unique_airports_list)
    
    print    
    print 'number of unidirectional routes:'
    
    route_list = []
    
    for i in range(len(coupon['Origin'])):
        
        hold = [coupon['Origin'][i], coupon['Dest'][i]]
        hold.sort()
        
        route = hold[0] + hold[1]
        
        if route not in route_list:
            
            route_list.append(route)
    
    print '\t', len(route_list)
    
    distance_list = []
    
    for i in range(len(coupon['Distance'])):
        
        distance_list.append([coupon['Distance'][i]] * int(coupon['Passengers'][i]))
    
#    http://stackoverflow.com/questions/952914/making-a-flat-list-out-of-list-of-lists-in-python
    
    distance_list_flattened = [item for sublist in distance_list for item in sublist]
    
    print    
    print 'minimum distance:'
    
    print '\t', min(distance_list_flattened)
    
    print    
    print 'maximum distance:'
    
    print '\t', max(distance_list_flattened)
    
    print    
    print 'mean distance:'
    
    print '\t', scipy.mean(distance_list_flattened)
    
    print
    
    return None
    