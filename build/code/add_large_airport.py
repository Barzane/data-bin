# -*- coding: utf-8 -*-

def add(data_hold):
    
    print
    print 'add large airport indicator'
    
    airport_size_2dict = {}
            
    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
        
        if origin not in airport_size_2dict:
            
            airport_size_2dict[origin] = data_hold[key]['pax']
            
        else:
            
            airport_size_2dict[origin] += data_hold[key]['pax']
        
        if destination not in airport_size_2dict:
            
            airport_size_2dict[destination] = data_hold[key]['pax']
            
        else:
            
            airport_size_2dict[destination] += data_hold[key]['pax']     
    
    airport_size = airport_size_2dict.items()
    
    airport_size_2 = []
    
    for i in airport_size:
        
        airport_size_2.append([int(i[1]), i[0]])
        
    airport_size_2.sort(reverse=True)
    
    large_airport_list = []
    
    for i in airport_size_2[:10]:
        
        large_airport_list.append(i[1])            
    
    print '\nlarge airports:\n\n\t',
    
    tick = 1
    
    for airport in large_airport_list:
        
        print airport + ' (' + str(tick) + ')',
        tick += 1
        
    print
    
    for key in data_hold:
        
        list_v = key.split('_')
        origin = list_v[0]
        destination = list_v[1]
    
        if ((origin in large_airport_list) or (destination in large_airport_list)):
            
            data_hold[key]['largeAirport'] = 1
            
        else:
            
            data_hold[key]['largeAirport'] = 0          
           
    return data_hold
