# -*- coding: utf-8 -*-

import time, cPickle, scipy, zipfile, shutil, os

import segment_timer, safe_cPickle

def add_s(line_data, x):

    for i in x:
        
        c = i.split(',')
        
        for j in c:
            
            if j != '':
                
                line_data.append(j)           
                
    return line_data

def add_to_b(next_line_list):

    line_data = []
    
    pos1 = 3
    pos2 = 7
    pos3 = 10
    pos4 = 16
    
    line_data = add_s(line_data, next_line_list[:pos1])
    line_data.append(next_line_list[pos1])
    
    line_data = add_s(line_data, next_line_list[pos1 + 1:pos2])
    line_data.append(next_line_list[pos2])
    
    line_data = add_s(line_data, next_line_list[pos2 + 1:pos3])
    line_data.append(next_line_list[pos3])
    
    line_data = add_s(line_data, next_line_list[pos3 + 1:pos4])
    line_data.append(next_line_list[pos4])
    
    line_data = add_s(line_data, next_line_list[pos4 + 1:])
    
    return line_data

def parse(src, year):
   
    assert isinstance(src, str), 'src must be a string'
    assert isinstance(year, int), 'year must be an integer'

    error_string = ''
    
    print    
    print '[source] ' + src
    
    dst_folder = '..\\input\\' + str(year) + '_T100D_SEGMENT_ALL_CARRIER_FOLDER.csv'

    t_unzip_csv_start = segment_timer.timer(True)

    print 'unzipping folder to \\input'
    
    print '[destination] ' + dst_folder
    
    zip = zipfile.ZipFile(src)
    zip.extractall(dst_folder)
    zip.close()
    
    src_csv = dst_folder + '\\' + str(year) + '_T100D_SEGMENT_ALL_CARRIER.csv'    
    dst_csv = '..\\temp\\' + str(year) + '_T100D_SEGMENT_ALL_CARRIER.csv'
        
    print 'copying .csv from \\input (folder) to \\temp'
        
    shutil.move(src_csv, dst_csv)
    
    print 'deleting redundant folder from \\input'

    shutil.rmtree(dst_folder)
    
    print '[warning] .csv \\input datafile is large'

    print 'opening: ' + dst_csv
        
    f = open(dst_csv, 'r')
    
    header = f.readline().strip().split('"')
   
    header_list = []
    
    for variable in header:
        
        if variable != ',':
            
            header_list.append(variable)       
            
        else:
            
          pass
        
    header_list = header_list[1:]
    
    print 'List of variables in dataset (.csv column order):',\
        len(header_list), 'variables'
        
    print
    
    for variable_name in header_list:
        print variable_name,
        
    print
    
    retain_name_list = ['YEAR', 'QUARTER', 'ORIGIN', 'DEST', 'CARRIER',\
                        'CARRIER_GROUP', 'PASSENGERS', 'SEATS', 'CLASS',\
                        'AIRCRAFT_GROUP', 'AIRCRAFT_TYPE', 'AIRCRAFT_CONFIG',\
                        'AIR_TIME', 'RAMP_TO_RAMP', 'DEPARTURES_PERFORMED']
        
    retain_list = ['DEPARTURES_PERFORMED', 'CARRIER_GROUP', 'PASSENGERS',\
                    'SEATS','AIRCRAFT_GROUP','AIRCRAFT_TYPE','AIRCRAFT_CONFIG',\
                    'AIR_TIME','RAMP_TO_RAMP']
    
    print
    print 'Retaining following variables (list order):',\
        len(retain_name_list), 'variables' 
    
    print
    
    for variable_name in retain_name_list:
        
        if variable_name in header_list:
            
            print variable_name,
            
        else:
            
            print variable_name, '(not available)'
            raise Exception ('variable_name missing from retain_name_list')
    
    print
    
    data_itin_dict = dict([x, []] for x in retain_name_list)
    
    print

    t_open_csv_start = segment_timer.timer(True)

    intermediate_dict={}
    
    count = 0
    
    for line in f:
        
        count += 1
        
        next_line = line.strip().split('"')
        
        next_line_list = []
        
        for variable in next_line:
            
            if variable != ',':
                
               next_line_list.append(variable)       
               
            else:
                
              pass
          
        next_line_list = next_line_list[0:47]
        
        line_data = add_to_b(next_line_list)    
        
        if len(line_data) != len(header_list):
            
            print
            print 'line length problem in line', count + 1, 'for year', year
            error_msg = 'line length problem in line' + str(count + 1) + ' for year ' + str(year)
            error_string += error_msg
            error_string += '\n'
        
        if len(line_data)==len(header_list):
        
            key_list=[]
        
            key_list.append(line_data[header_list.index('ORIGIN')])
            key_list.append(line_data[header_list.index('DEST')])    
            key_list.sort()
            
            key_list.append(line_data[header_list.index('CARRIER')])
            key_list.append(line_data[header_list.index('YEAR')])
            key_list.append(line_data[header_list.index('QUARTER')])  
#            key_list.append(line_data[header_list.index('CLASS')])
            
            key = '_'.join(key_list)
            
            if line_data[header_list.index('CLASS')] in ['F','L']:
                            
                if key not in intermediate_dict:
                    
                    intermediate_dict[key] = {}
                    
                    for k in retain_list:
                        
                        if k in ['PASSENGERS', 'RAMP_TO_RAMP', 'AIR_TIME', 'SEATS', 'DEPARTURES_PERFORMED']:
                            
                            intermediate_dict[key][k] = [eval(line_data[header_list.index(k)])]
                        
                        else:
                            
                            intermediate_dict[key][k]=[line_data[header_list.index(k)]]                            
                    
                else:
            
                    for k in retain_list:
                        
                        if k in ['PASSENGERS', 'RAMP_TO_RAMP', 'AIR_TIME', 'SEATS', 'DEPARTURES_PERFORMED']:
                            
                            intermediate_dict[key][k].append(eval(line_data[header_list.index(k)]))
                            
                        else:
                            
                            intermediate_dict[key][k].append(line_data[header_list.index(k)])           
    
    f.close()
    
    data_dict = {}

    for key in intermediate_dict:
        
        data_dict[key] = {}
        
        for variable in intermediate_dict[key]:
            
            if variable in ['PASSENGERS', 'SEATS']:
                
                data_dict[key][variable] = sum(intermediate_dict[key][variable])
                
        if data_dict[key]['SEATS'] != 0.0:
            
            data_dict[key]['LOAD_FACTOR'] = 100.0 * float(data_dict[key]['PASSENGERS']) / data_dict[key]['SEATS']
            
        for variable in intermediate_dict[key]:
            
            if variable in ['AIR_TIME', 'DEPARTURES_PERFORMED']:
                
              data_dict[key][variable] = sum(intermediate_dict[key][variable])
              
        if data_dict[key]['DEPARTURES_PERFORMED'] != 0.0:
            
            data_dict[key]['MEAN_AIR_TIME'] = data_dict[key]['AIR_TIME'] / data_dict[key]['DEPARTURES_PERFORMED']
            
        for variable in intermediate_dict[key]:
            
            if variable in ['RAMP_TO_RAMP', 'DEPARTURES_PERFORMED']:
                
              data_dict[key][variable] = sum(intermediate_dict[key][variable])
              
        if data_dict[key]['DEPARTURES_PERFORMED'] != 0.0:
            
            data_dict[key]['MEAN_RAMP_TO_RAMP'] = data_dict[key]['RAMP_TO_RAMP'] / data_dict[key]['DEPARTURES_PERFORMED']
                     
    print count,'lines'
    print ('%0.3f seconds to parse data'%(segment_timer.timer(False, t_open_csv_start)))

    dst_temp = '..\\temp\\T100_merge_' + str(year) + '.bin'

    print 'save file: ' + dst_temp
    
    f = open (dst_temp, 'wb')
    cPickle.dump(data_dict, f)
    f.close()

    dst_error = '..\\temp\\error_string.txt'
    
    if error_string != '':
        
        f = open(dst_error, 'wb')
        f.write(error_string)
        f.close()

    print 'deleting redundant file from \\input: ' + dst_csv
    
    os.remove(dst_csv)

    return None

def wrapper(test_run, test_periods, full_periods, security = None, security_max = None):
        
    if test_run:
        
        year_list = test_periods[0]
        
    else:
                
        year_list = full_periods[0]
    
    for year in year_list:

        src_t100 = '..\\..\\data\\T100\\' + str(year) + '_T100D_SEGMENT_ALL_CARRIER.zip'
            
        try:
                            
            parse(src_t100, year)
                
        except IOError:

            raise IOError('requested data unavailable: year ' + str(year))
    
    return None
    