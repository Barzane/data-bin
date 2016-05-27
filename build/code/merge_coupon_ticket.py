# -*- coding: utf-8 -*-

import cPickle, copy

import segment_timer
import cpi_parse

def merge(src_coupon, src_ticket, yyyy, q):
    
    print 'merge Coupon and Ticket .bin files to Itinerary'    
    
    t_start_total = segment_timer.timer(True)
    
    print
    print '[loading]\n\n\t' + src_ticket
    
    t_start = segment_timer.timer(True)
    
    f = open(src_ticket, 'r')
    ticket = cPickle.load(f)
    f.close()
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    print '\n[loading]\n\n\t' + src_coupon
    
    t_start = segment_timer.timer(True)
    
    f = open(src_coupon, 'r')
    coupon = cPickle.load(f)
    f.close()
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
      
    print '\ncopying coupon dictionary'
    
    t_start = segment_timer.timer(True)
    
    output = copy.deepcopy(coupon)
    output['ItinFare'] = []
    output['ItinFareReal'] = []
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    coupon_length = len(coupon[coupon.keys()[0]])
    ticket_length = len(ticket[ticket.keys()[0]])
    
    del coupon    
    
    ticket_dict = {}
    dollar_cred_dict = {}
    bulk_fare_dict = {}
    
    print '\nbuilding ticket, DollarCred and BulkFare dictionaries'
    
    t_start = segment_timer.timer(True)
    
    for i in range(ticket_length):
        
        ticket_dict[ticket['ItinID'][i]] = ticket['ItinFare'][i]
        dollar_cred_dict[ticket['ItinID'][i]] = ticket['DollarCred'][i]
        bulk_fare_dict[ticket['ItinID'][i]] = int(ticket['BulkFare'][i])
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))

    del ticket
    
    if len(ticket_dict) != ticket_length:
        raise Exception('duplicate key in ticketDict')
    
    print '\nparsing CPI data'

    CPI2013Q4_dict = cpi_parse.parse()
    
    print '\nadd ItinFare and ItinFareReal (2013Q4 prices) to output dictionary'
    
    t_start = segment_timer.timer(True)
    
    for i in range(coupon_length):
        
        fare_nominal = ticket_dict[output['ItinID'][i]]
        fare_real = fare_nominal * CPI2013Q4_dict[str(yyyy) + '_' + str(q)]
        output['ItinFare'].append(fare_nominal)
        output['ItinFareReal'].append(fare_real)
    
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    print '\nremove itineraries with DollarCred = 0'

    t_start = segment_timer.timer(True)
    
    output2 = {}
    
    for key in output.keys():
        
        output2[key] = []
    
    count_remove = 0
    
    for i in range(coupon_length):
        
        if dollar_cred_dict[output['ItinID'][i]] == 1:
            
            for key in output2.keys():
                
                output2[key].append(output[key][i])
                
        else:
            
#            fare not credible (DollarCred = 0)
            count_remove += 1

    del output

    output = copy.deepcopy(output2)
    
    del output2    
    
    print str(count_remove) + ' itineraries removed'
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))

    coupon_length_ = len(output[output.keys()[0]])
    
    print '\nremove itineraries with BulkFare = 1'

    t_start = segment_timer.timer(True)
    
    output2 = {}
    
    for key in output.keys():
        
        output2[key] = []
    
    count_remove = 0
    
    for i in range(coupon_length_):
        
        if bulk_fare_dict[output['ItinID'][i]] == 0:
            
            for key in output2.keys():
                
                output2[key].append(output[key][i])
                
        else:
            
#            bulk fare (BulkFare = 1)
            count_remove += 1

    del output

    output = copy.deepcopy(output2)
    
    del output2    
    
    print str(count_remove) + ' itineraries removed'
    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    coupon_length_after_dollar_and_bulk_fare_cred = len(output[output.keys()[0]])

    output_explode_passengers = {}
    
    for key in output.keys():
        
        output_explode_passengers[key] = []

    for i in range(coupon_length_after_dollar_and_bulk_fare_cred):
        
        for key in output_explode_passengers.keys():
            
            for j in range(int(output['Passengers'][i])):
                
                output_explode_passengers[key].append(output[key][i])
    
    del output    
    
    del output_explode_passengers['Passengers']
    
    dst_itinerary = '..\\temp\\itinerary_' + str(yyyy) + '_' + str(q) + '.bin'

    f = open(dst_itinerary, 'wb')
    
    print '\nsave itinerary ' + dst_itinerary
    
    t_start = segment_timer.timer(True)
    
    cPickle.dump(output_explode_passengers, f)

    del output_explode_passengers

    print '%0.3f seconds '%(segment_timer.timer(False, t_start))
    
    f.close()
    
    print '\nTotal time: ' + ('%0.3f seconds '%(segment_timer.timer(False, t_start_total)))
    
    del ticket_dict
    del dollar_cred_dict
    del bulk_fare_dict
    del fare_nominal
    del fare_real    
    
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

            src_coupon = '..\\temp\\coupon_' + str(year) + '_' + str(quarter) + '.bin'
            src_ticket = '..\\temp\\ticket_' + str(year) + '_' + str(quarter) + '.bin'
            
            try:
                            
                merge(src_coupon, src_ticket, year, quarter)
                
            except IOError:

                raise IOError('requested data unavailable: year ' + str(year) + ', quarter ' + str(quarter))
    
    return None