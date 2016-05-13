# -*- coding: utf-8 -*-

import time, os, zipfile, shutil

import safe_cPickle, segment_timer
import sort_coupon_csv_2011_on
import coupon_descriptives

def parse_csv(src, security, security_max, year, quarter):
    
    print 'parse DB1B Coupon data from .zip to coupon_year_quarter.bin'
    
    assert isinstance(src, str), 'src must be a string'
    assert isinstance(security, bool), 'security must be a Boolean'
    assert ((security_max > 0) and isinstance(security_max, int)),\
        'security_max must be a positive integer'
    
    print    
    print '[source] ' + src
    
    dst_folder = '..\\input\\Origin_and_Destination_Survey_DB1BCoupon_' + str(year) + '_' + str(quarter) + '_FOLDER.csv'

    t_unzip_csv_start = segment_timer.timer(True)

    print 'unzipping folder to \\input'
    
    print '[destination] ' + dst_folder
    
    zip = zipfile.ZipFile(src)
    zip.extractall(dst_folder)
    zip.close()
    
    src_csv = dst_folder + '\\Origin_and_Destination_Survey_DB1BCoupon_' + str(year) + '_' + str(quarter) + '.csv'    
    dst_csv = '..\\temp\\Origin_and_Destination_Survey_DB1BCoupon_' + str(year) + '_' + str(quarter) + '.csv'
    dst_csv_2011q1_to_2013q4_temp = '..\\temp\\Origin_and_Destination_Survey_DB1BCoupon_' + str(year) + '_' + str(quarter) + '_UNSORTED.csv'

    if year >= 2014:
        
        raise Exception('sort not implemented', year)

    if 2011 <= year <= 2013:
                
        print '[sort csv for 2011Q1 to 2013Q4 inclusive]'
        print 'copying .csv from \\input (folder) to \\temp'
        
        shutil.move(src_csv, dst_csv_2011q1_to_2013q4_temp)
        
        sort_coupon_csv_2011_on.sort_coupon_csv(dst_csv_2011q1_to_2013q4_temp, dst_csv, year, quarter)
    
    else:
        
        print 'copying .csv from \\temp (folder) to \\temp'
        
        shutil.move(src_csv, dst_csv)
    
    print 'deleting redundant folder from \\input'

    shutil.rmtree(dst_folder)
    
    print '[warning] .csv \\input datafile is large'
    
    print 'opening .csv file for line count'
    
    data_reader = open(dst_csv, 'r')    
    
    print '%0.3f seconds to unzip and open file'%(segment_timer.timer(False, t_unzip_csv_start))

#    count number of lines in .csv file
    
    if security:
        
        print '[** running in reduced-lines mode **]'
        max_count = None
        
    else:
        
        print 'counting number of lines in dataset'    
        max_count = 0
    
        t_count_lines_start = segment_timer.timer(True)
    
        for line in data_reader:
            max_count += 1
    
        print '%0.3f seconds to count lines in file'%(segment_timer.timer(False, t_count_lines_start))
        print 'number of lines of data (including header):', max_count
        print 'sleeping for 5 seconds'
        
        time.sleep(5)    
    
    data_reader.close()
    
    print 're-open .csv file for parse'
    
    t_reopen_csv_start = segment_timer.timer(True)
    
    data_reader = open(dst_csv, 'r')
    
    print '%0.3f seconds to re-open file'%(segment_timer.timer(False, t_reopen_csv_start))
        
    large_carriers_dict = {'Southwest':'WN', 'American':'AA', 'Continental':'CO',\
                    'Delta':'DL', 'Northwest':'NW', 'Skywest':'OO',\
                    'United':'UA', 'US Airways':'US', 'American Eagle':'MQ',\
                    'Airtran Airways':'FL', 'Express Jet':'EV',\
                    'Jetblue':'B6', 'Alaska Airlines':'AS', 'Endeavor Air':'9E'}
    
    large_carrier_condition = False    
     
    print 'construct list of Coupon .csv variable names, in key_list'
    
    t_parse_timer = segment_timer.timer(True)
    
    key_list = []
    
    for line in data_reader:
        
        key_list_raw = line.split('"')[1:-1]
        
        for variable_name in key_list_raw:
            
            if variable_name != ',':
                key_list.append(variable_name)
            else:
                pass
        break               
    
    print 'list of variables in dataset (.csv column order):',\
          len(key_list),'variables'
    print '[variables]',
    
    for variable_name in key_list:
        print variable_name,
        
    retain_names_list = ['ItinID', 'Year', 'Quarter', 'Origin', 'Dest',\
        'OpCarrier', 'Passengers', 'TkCarrier', 'Distance', 'FareClass']
    
    print
    print 'retaining following variables (list order):',\
          len(retain_names_list), 'variables'
    print '[variables]',

    for variable_name in retain_names_list:
        if variable_name in key_list:
            print variable_name,
        else:
            print variable_name, '(not available)'
            raise Exception('variable_name missing from retain_names_list')
    print
    
#    initialize data dictionary:
#    key/ variable name from retain_names_list, value/ list (empty by default)
#    the set of ith elements of the lists corresponds to one itinerary observation 
    
    data_itin_dict = {}
    
    for variable_name in retain_names_list:
        data_itin_dict[variable_name] = []
    
    if large_carrier_condition:
        
        print 'retaining following large carriers:'
        for i in large_carriers_dict:
            print i+' : ',
        print
        
    else:
        
        print 'retaining all carriers'
    
    count = 1
    
    if not security:
        
        t_intermediate_parse = segment_timer.timer(True)
        
        print 'parsing data, percentage completed:'
        
        top_count = max_count / 100
        print count / top_count
    
#    loop over all lines in .csv file
    
    for line in data_reader:
        
        count += 1
    
        if not security:
            
            if float(count / top_count) == float(count) / top_count:

                print str(count / top_count)+'\t','%0.3f seconds'%(segment_timer.timer(False, t_intermediate_parse))

                t_intermediate_parse = segment_timer.timer(True)  
    
#        line_data_list is a list of evaluated data elements
        
        line_split = line.split(',')[:-1]
        
        line_data_list = [eval(element) for element in line_split]
    
#        new itinerary for retained operating carrier if SeqNum == 1
#        deals with possible incomplete itinerary at start of data_reader (skipped)
        
        itin_test = line_data_list[key_list.index('ItinID')]   
        
#        if itin_test == eval('201122538709'):
#            print 'out', line_data_list
        
        if line_data_list[key_list.index('SeqNum')] == 1 and line_data_list[key_list.index('Coupons')] == 2:

#            number of coupons in newly-identified itinerary
            
            coupons_new = line_data_list[key_list.index('Coupons')]
                        
            if coupons_new == 1:
#                one-way
                pass
            
            elif coupons_new == 2:
                    
#                list of data corresponding to newly-identified itinerary
                
                line_data_list_first = line_data_list[:]
        
#                carrier_list will contain OpCarrier for each coupon in itinerary
#                to enable constant OpCarrier itineraries to be retained
#                (also applies to fare_class_list, passengers_list, and tk_carrier_list if required)
                
                carrier_list = [line_data_list[key_list.index('OpCarrier')][:]]            
                fare_class_list = [line_data_list[key_list.index('FareClass')][:]]
                passengers_list = [line_data_list[key_list.index('Passengers')]]
                tk_carrier_list = [line_data_list[key_list.index('TkCarrier')][:]]
                coupon_type_list = [line_data_list[key_list.index('CouponType')][:]]
                
#                if segment has trip break at SeqNum==1, create candidate destination variable
                
                if line_data_list[key_list.index('Break')] == 'X':
                    
                    count_break = 1
                    line_data_list_dest = line_data_list[key_list.index('Dest')][:]
                    
                else:
                    
                    count_break = 0            
                        
#                once new itinerary identified, continue to loop over lines in .csv file
                
                for line_ in data_reader:
                    
                    count += 1
        
#                    if in test mode, exit data parse
                    
                    if security and count >= security_max:
                        break
        
                    if not security:
                        if float(count / top_count) == float(count) / top_count:
                            
                            print str(count / top_count) + '\t', '%0.3f seconds'%(segment_timer.timer(False, t_intermediate_parse))
                            t_intermediate_parse = segment_timer.timer(True)
                       
                    line_split_ = line_.split(',')[:-1]
                    line_data_list_ = [eval(element_) for element_ in line_split_]
                    
                    itin_test_ = line_data_list_[key_list.index('ItinID')]   
                    
                    if itin_test != itin_test_:
                        break
        
#                    if itin_test_ == eval('201122538709'):
#                        print 'return', line_data_list_
                
                    carrier_list.append(line_data_list_[key_list.index('OpCarrier')][:])        
                    fare_class_list.append(line_data_list_[key_list.index('FareClass')][:])
                    passengers_list.append(line_data_list_[key_list.index('Passengers')])
                    tk_carrier_list.append(line_data_list_[key_list.index('TkCarrier')][:])
                    coupon_type_list.append(line_data_list_[key_list.index('CouponType')][:])
    
#                    if at end of itinerary, create candidate final destination variable
#                    if not at end of itinerary, but segment has trip break, 
#                    create candidate destination variable
                    
                    if line_data_list_[key_list.index('SeqNum')] == coupons_new:
                        
                        if line_data_list_[key_list.index('Break')] == 'X':
                            
                            count_break += 1
                            line_data_list_final_dest = line_data_list_[key_list.index('Dest')][:]
        
#                        break out of inner (line_) for loop
#                        and check whether to retain itinerary
                            
                        break
                    
                    else:
                        
                        if line_data_list_[key_list.index('Break')] == 'X':
                            
                            countBreak += 1
                            line_data_list_dest=line_data_list_[key_list.index('Dest')][:]
                            
                        else:
                            
                            pass
        
                    break
                
#                retain itinerary if the following conditions are satisfied:
#                1) exactly 2 trip breaks
#                2) origin=destination (round-trip)
#                3) maximum 2 coupons - Jan. 2014: change to 4 for hub flights
#                4) constant OpCarrier
#                5) constant FareClass
#                6) constant Passengers
#                7) constant TkCarrier, not necessarily same as OpCarrier
#                8) no 'E' in CouponType (no cabotage on itinerary)
#                i.e. direct return flights only (directional)
#                9) specify which carriers to keep
#                10) legs in lower 48 states only
#                11) restricted and unrestricted coach class tickets only
#                12) only retain non-code shared flights
        
#                to do: need to check whether OpCarrier code (IATA?) is constant over time
#                or if there is an alternative unique carrier code
        
#                older versions of code retained all itineraries with <= 4 coupons
        
#                for large carrier restriction, add condition:
#                and carrier_list[0] in large_carriers_dict.values()
                
                itinerary_condition = (
                                    (count_break == 2)
                                    and (line_data_list_first[key_list.index('Origin')] == line_data_list_final_dest)
                                    and (line_data_list_first[key_list.index('Coupons')] == 2)
                                    and carrier_list.count(carrier_list[0]) == len(carrier_list)
                                    and fare_class_list.count(fare_class_list[0]) == len(fare_class_list)
                                    and passengers_list.count(passengers_list[0]) == len(passengers_list)
                                    and tk_carrier_list.count(tk_carrier_list[0]) == len(tk_carrier_list)
                                    and coupon_type_list.count('E') == 0
                                    and (line_data_list[key_list.index('ItinGeoType')] == 2)
                                    and ((line_data_list[key_list.index('FareClass')] in ['X','Y','C','D','F','G']))
                                    and tk_carrier_list[0] == carrier_list[0]
                                    )
                
#                if itin_test_ == eval('201122538709'):
#                    print 'testing ItinID 201122538709'
#                    print itinerary_condition
#                    print count_break
#                    print line_data_list_first[key_list.index('Origin')]
#                    print line_data_list_final_dest
#                    print line_data_list_first[key_list.index('Coupons')]
#                    print carrier_list
#                    print fare_class_list
#                    print passengers_list
#                    print tk_carrier_list
#                    print coupon_type_list
#                    print line_data_list[key_list.index('ItinGeoType')]
#                    print line_data_list[key_list.index('FareClass')]
#                    print
                    
#                itinerary_condition_wn_first_class=(
#                                    (count_break == 2)
#                                    and (line_data_list_first[key_list.index('Origin')] == line_data_list_final_dest)
#                                    and (line_data_list_first[key_list.index('Coupons')] == 2)
#                                    and carrier_list.count(carrier_list[0]) == len(carrier_list)
#                                    and fare_class_list.count(fare_class_list[0]) == len(fare_class_list)
#                                    and passengers_list.count(passengers_list[0]) == len(passengers_list)
#                                    and tk_carrier_list.count(tk_carrier_list[0]) == len(tk_carrier_list)
#                                    and coupon_type_list.count('E') == 0
#                                    and (line_data_list[key_list.index('ItinGeoType')] == 2)
#                                    and ((line_data_list[key_list.index('FareClass')] in ['F','G']))
#                                    and tk_carrier_list[0] == carrier_list[0]
#                                    and carrier_list[0] == 'WN'
#                                    )            
                
                if large_carrier_condition:
                    
                    itinerary_condition = (itinerary_condition and carrier_list[0] in large_carriers_dict.values())
#                    itinerary_condition_wn_first_class = (itinerary_condition_wn_first_class and carrier_list[0] in large_carriers_dict.values())
                
#                if (itinerary_condition or itinerary_condition_wn_first_class):
                
                if itinerary_condition:
                    
#                    if itinerary_condition satisfied, retain all data for itinerary
#                    otherwise, continue searching for a new itinerary in data_reader
#                    also retain WN "first class" tickets
#                    also retain any class from C, D, F, G, X, Y (business, first, coach)
                    
                    for name in retain_names_list:
                        
                        if name != 'Dest':
                            
                            data_itin_dict[name].append(line_data_list_first[key_list.index(name)])
                            
                        else:
                            
                            data_itin_dict['Dest'].append(line_data_list_dest)
                
                    if itin_test_ == eval('201122538709'):
                        
                        for key in data_itin_dict.keys():
                            print key, data_itin_dict[key][-1]
                
                else:
        
#                    continue with outer (line) for loop
                    
                    continue
    
#                if itin_test_ == eval('201122538709'):
#                    print data_itin_dict['OpCarrier'].count('WN')
    
#        if in test mode, exit data parse
    
        if security and count >= security_max:
            break

    print '%0.3f seconds to parse data'%(segment_timer.timer(False, t_parse_timer))
    
    print 'number of retained itineraries:', len(data_itin_dict[data_itin_dict.keys()[0]])
    print 'number of lines read:', count
    
    print 'illustrative itineraries:'
    
    if len(data_itin_dict[data_itin_dict.keys()[0]]) >= 3:
        for itin_number in xrange(3):
            for variable in retain_names_list:
                print variable, data_itin_dict[variable][itin_number],
            print
        
    if not security:
        print 'total number of lines:', max_count
    
#    safe_cPickle Python dictionary coupon_year_quarter
    
    print 'save .bin to \\temp'
    
#    if large_carrier_condition == True, dst filename will not change    
    
    dst = '..\\temp\\' + 'coupon_' + str(year) + '_' + str(quarter) + '.bin'

    print '[temp] ' + dst
                            
    safe_cPickle.safe_cPickle_dump(dst, data_itin_dict)
    
    if not security:
        
        print 'sleeping for 15 seconds'
        time.sleep(15)
        
    data_reader.close()
    
    print 'deleting .csv file from \\temp'
    
    os.remove(dst_csv)
    
#    descriptive statistics for 2013Q4 (any quarter can be called)    
    
    if (year == 2013) and (quarter == 4):    
        
        coupon_descriptives.compute(year, quarter)
    
    return None

def wrapper(test_run, security, security_max, test_periods, full_periods):
    
    if test_run:
        
        year_list = test_periods[0]
        quarter_list = test_periods[1]
        
    else:
                
        year_list = full_periods[0]
        quarter_list = full_periods[1]
    
    for year in year_list:
        for quarter in quarter_list:

            src = '..\\..\\data\\DB1BCoupon\\Origin_and_Destination_Survey_DB1BCoupon_' + str(year) + '_' + str(quarter) + '.zip'
            
            try:
                            
                parse_csv(src, security, security_max, year, quarter)
                
            except IOError:

                raise IOError('requested data unavailable: year ' + str(year) + ', quarter ' + str(quarter))
    
    return None
