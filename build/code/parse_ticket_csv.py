# -*- coding: utf-8 -*-

import time, os, zipfile, shutil

import safe_cPickle, segment_timer

def parse_csv(src, security, security_max, year, quarter):    
    
    assert isinstance(src, str), 'src must be a string'
    assert isinstance(security, bool), 'security must be a Boolean'
    assert ((security_max > 0) and isinstance(security_max, int)),\
        'security_max must be a positive integer'
    
    print    
    print '[source] ' + src
    
    dst_folder = '..\\input\\Origin_and_Destination_Survey_DB1BTicket_' + str(year) + '_' + str(quarter) + '_FOLDER.csv'

    t_unzip_csv_start = segment_timer.timer(True)

    print 'unzipping folder to \\input'
    
    print '[destination] ' + dst_folder
    
    zip = zipfile.ZipFile(src)
    zip.extractall(dst_folder)
    zip.close()
    
    src_csv = dst_folder + '\\Origin_and_Destination_Survey_DB1BTicket_' + str(year) + '_' + str(quarter) + '.csv'    
    dst_csv = '..\\temp\\Origin_and_Destination_Survey_DB1BTicket_' + str(year) + '_' + str(quarter) + '.csv'
        
    print 'copying .csv from \\input (folder) to \\temp'
        
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
     
    print 'construct list of Ticket .csv variable names, in key_list'
    
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
        
    retain_names_list = ['ItinID', 'ItinFare', 'DollarCred', 'BulkFare']
    
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
        
#        if in test mode, exit data parse
        
        if security and count >= security_max:
            break      

        if not security:
            if float(count / top_count) == float(count) / top_count:
                
                print str(count / top_count) + '\t', '%0.3f seconds'%(segment_timer.timer(False, t_intermediate_parse))
                t_intermediate_parse = segment_timer.timer(True)
           
        line_split = line.split(',')[:-1]
        line_data_list = [eval(element) for element in line_split]
        
#        build dictionary: append values to lists, for each retained variable
#        no error trap for multiple occurrences of the same ItinID

        for name in retain_names_list:
                            
            data_itin_dict[name].append(line_data_list[key_list.index(name)])

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
    
#    safe_cPickle Python dictionary ticket_year_quarter
    
    print 'save .bin to \\temp'
        
    dst = '..\\temp\\' + 'ticket_' + str(year) + '_' + str(quarter) + '.bin'

    print '[temp] ' + dst
                            
    safe_cPickle.safe_cPickle_dump(dst, data_itin_dict)
    
    if not security:
        
        print 'sleeping for 15 seconds'
        time.sleep(15)
    
    data_reader.close()
    
    print 'deleting .csv file from \\temp'
    
    os.remove(dst_csv)
    
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

            src = '..\\..\\data\\DB1BTicket\\Origin_and_Destination_Survey_DB1BTicket_' + str(year) + '_' + str(quarter) + '.zip'
            
            try:
                            
                parse_csv(src, security, security_max, year, quarter)
                
            except IOError:

                raise IOError('requested data unavailable: year ' + str(year) + ', quarter ' + str(quarter))
    
    return None
