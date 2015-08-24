# -*- coding: utf-8 -*-

import cPickle, copy, scipy

import segment_timer

def compress(src, yyyy, q):
    
    t_start_total = segment_timer.timer(True)
    
    print
    print 'loading: ' + src
        
    t_start = segment_timer.timer(True)
    
    f = open(src, 'r')
    itinerary = cPickle.load(f)
    f.close()
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    length_itinerary = len(itinerary[itinerary.keys()[0]])
    
    route_level_dict = {}
    
    print 'creating route-level dictionary'
    print '- remove all tickets with (nominal) ItinFare < $20'
    
    t_start = segment_timer.timer(True)
    
    for i in range(length_itinerary):
        
        origin = itinerary['Origin'][i]
        destination = itinerary['Dest'][i]
        opcarrier = itinerary['OpCarrier'][i]
        year = str(itinerary['Year'][i])
        quarter = str(itinerary['Quarter'][i])
        
#        non-directional route
        
        route = [origin, destination]
        route.sort()
    
        key = (route[0] + '_' + route[1] + '_' + opcarrier +
            '_' + year + '_' + quarter)
    
        distance = itinerary['Distance'][i]
        tkcarrier = itinerary['TkCarrier'][i]
        fareclass = itinerary['FareClass'][i]
        itinfare = itinerary['ItinFare'][i]
        itinfarereal = itinerary['ItinFareReal'][i]
        
#        no need to use ItinID from here onwards
        
        value = [distance, tkcarrier, fareclass, itinfare, itinfarereal]
        
        frequent_flyer = (itinfare < 20.0)
        
        if not frequent_flyer:    
        
            if key not in route_level_dict.keys():
                
                route_level_dict[key] = [value]
                
            else:
                
                route_level_dict[key].append(value)

    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    print '# route-carriers', len(route_level_dict.keys())
    
    del itinerary
    
    route_level_dict_2 = copy.deepcopy(route_level_dict)
    
    del route_level_dict
    
    route_level_dict_3 = {}
    
    print '- remove all tickets with (nominal) ItinFare > 99th percentile of route-carrier-quarter fare distribution'
    
    t_start = segment_timer.timer(True)
            
    for k in route_level_dict_2.keys():
       
        nominal_fare_list = []
        
        for ticket in route_level_dict_2[k]:
            
            nominal_fare_list.append(ticket[3])
            
        p99 = scipy.percentile(scipy.array(nominal_fare_list), 99)
        
        for ticket in route_level_dict_2[k]:
            
            high_fare = (ticket[3] > p99)
            
            if not high_fare:
                
                if k not in route_level_dict_3.keys():
                    
                    route_level_dict_3[k] = [ticket]
                    
                else:
                    
                    route_level_dict_3[k].append(ticket)
    
    del route_level_dict_2
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    print '# route-carriers', len(route_level_dict_3.keys())
    
    route_level_dict_4 = {}

    print '- remove all WN routes that involve DFW, from 1993Q1 to 1999Q4'

    t_start = segment_timer.timer(True)
    
    count_wn_dfw_tickets = 0
    
    for k in route_level_dict_3.keys():
        
        k__ = k.split('_')
        
        origin_ = k__[0]
        dest_ = k__[1]
        carrier_ = k__[2]
        year_ = int(k__[3])
        
        condition = (
                    (carrier_ == 'WN')
                    and ((origin_ == "DFW") or (dest_ == "DFW"))
                    and (year_ in range(1993, 2000))
                    )
        
        if condition:
            
            count_wn_dfw_tickets += 1
            
        else:
            
            route_level_dict_4[k] = route_level_dict_3[k]
        
    del route_level_dict_3

    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    print '# WN DFW routes removed:', count_wn_dfw_tickets
    print '# route-carriers', len(route_level_dict_4.keys())
    
    d_class = {}
    
    for key in route_level_dict_4:
        
        for ticket in route_level_dict_4[key]:
            
            if ticket[1] not in d_class.keys():
                
                d_class[ticket[1]] = {'coach' : 0, 'other' : 0}
                
            if ticket[2] not in ['X','Y']:
                
                d_class[ticket[1]]['other'] += 1
                
            else:
                d_class[ticket[1]]['coach'] += 1
                
    d_class_coach_only = {}
    
    for key in d_class:
        
        num = float(d_class[key]['other'])
        den = float(d_class[key]['coach'] + d_class[key]['other'])
        d_class_coach_only[key] = num / den
        
    print
    
    for key in d_class_coach_only:
        
        print key, '%0.1f percent not coach'%(100 * d_class_coach_only[key])
    
    print
    
    print 'compress dictionary, no error trap for Distance, TkCarrier, FareClass'
        
    t_start = segment_timer.timer(True)
    
    route_level_dict_5 = {}
    
    for key in route_level_dict_4.keys():
        
        distance = route_level_dict_4[key][0][0]
        nominal_fare_list = []
        real_fare_list = []
        fare_class_list = []
        
        for ticket in route_level_dict_4[key]:
            
#            note that ticket[1] is the ticketing, not operating carrier; even if ticketing=operating here
            
            if d_class_coach_only[ticket[1]] > 0.75:
                
                nominal_fare_list.append(ticket[3])
                real_fare_list.append(ticket[4])
                fare_class_list.append(ticket[2])

            else:
                
                if ticket[2] in ['X','Y']:
                    
                    nominal_fare_list.append(ticket[3])
                    real_fare_list.append(ticket[4])
                    fare_class_list.append(ticket[2])
                    
        nominal_fare_list.sort()
        real_fare_list.sort()
        route_level_dict_5[key] = [distance, nominal_fare_list, real_fare_list]
        
        condition = (
                    (key.split('_')[2] == 'WN')
                    and (('F' in fare_class_list) or ('G' in fare_class_list))
                    )
                    
        if condition:
            
            dst_wn = '..\\temp\\' + key + '.txt'
            
            output_string = ''
            output_string += 'Southwest reporting first class tickets:\n'
            output_string += ('# coach class on route-carrier-quarter ' + key + ':\n')
            output_string += (str((fare_class_list.count('X') + fare_class_list.count('Y'))) + '\n')
            output_string += ('# first class on route-carrier-quarter ' + key + ':\n')
            output_string += (str((fare_class_list.count('F') + fare_class_list.count('G'))) + '\n')
            
            print 'saving temporary file: ' + dst_wn
            
            f = open(dst_wn, 'w')
            f.write(output_string)
            f.close()
            
    del route_level_dict_4
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    route_carrier_list = route_level_dict_5.keys()[:]
    
    route_level_dict_6 = {}
    
    print '- remove all route-carriers with < 100 passengers in quarter'
    
    t_start = segment_timer.timer(True)
    
    for j in route_carrier_list:
        
        low_volume = (len(route_level_dict_5[j][2]) < 100)
            
        if not low_volume:
            
            route_level_dict_6[j] = route_level_dict_5[j]
        
    del route_level_dict_5
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    print '# route-carriers', len(route_level_dict_6.keys())
    
    dst_route_carrier = '..\\temp\\routecarrier_' + str(yyyy) + '_' + str(q) + '.bin'
    
    print 'saving: ' + dst_route_carrier
    
    t_start = segment_timer.timer(True)
    
    f = open(dst_route_carrier, 'wb')
    cPickle.dump(route_level_dict_6, f)
    f.close()

    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    print 'total time:'
    print '%0.3f seconds '%(segment_timer.timer(False, t_start_total))

    del route_level_dict_6

    return None

def wrapper(test_run, test_periods, full_periods, security = None, security_max = None):
        
    if test_run:
        
        year_list = test_periods[0]
        quarter_list = test_periods[1]
        
    else:
                
        year_list = full_periods[0]
        quarter_list = full_periods[1]
    
    for year in year_list:
        for quarter in quarter_list:

            src_itinerary = '..\\temp\\itinerary_' + str(year) + '_' + str(quarter) + '.bin'
            
            try:
                            
                compress(src_itinerary, year, quarter)
                
            except IOError:

                raise IOError('requested data unavailable: year ' + str(year) + ', quarter ' + str(quarter))
    
    return None