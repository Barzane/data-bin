# -*- coding: utf-8 -*-

import cPickle, copy

def convert(year, quarter):
    
    print 'convert .bin to .txt'
    
    src_data = '..\\output\\data_' + str(year) + '_' + str(quarter) + '.bin'
    
#    data .bin loaded from \output, not moved to \temp first
    
    print
    print 'loading', src_data
    
    f = open(src_data, 'rb')
    data_hold = cPickle.load(f)
    f.close()
    
    var_list = copy.deepcopy(data_hold[data_hold.keys()[0]].keys())
    
#    http://stackoverflow.com/questions/16581695/python-how-to-sort-lists-alphabetically-with-respect-to-capitalized-letters

    var_list = sorted(var_list, key=lambda L: (L.lower(), L))
    
    data_dict = {}
    
    for key in data_hold:
        
        data_dict[key] = []
        
        for var in var_list:
            
            data_dict[key].append(data_hold[key][var])
    
    output_string = ''

    first_key = data_dict.keys()[0].split('_')
    
    dst_txt = '..\\output\\'+'data_' + first_key[-2] + '_' + first_key[-1] + '.txt'

    header_line = 'origin' + '\t' + 'dest' + '\t' + 'carrier' +\
        '\t' + 'year' + '\t' + 'quarter' + '\t'

    for i in var_list:
        
        header_line += str(i)
        header_line += '\t'
        
    header_line = header_line.rstrip()    
    header_line += '\n'

    output_string += header_line

    for key in data_dict.keys():
        
        data_line = key.split('_') + data_dict[key]
        
        for item in data_line:
            
            output_string += str(item)
            output_string += '\t'
            
        output_string = output_string.rstrip()
        output_string += '\n'
        
    output_string = output_string.rstrip()

    print 'saving', dst_txt
    print

    f = open(dst_txt, 'w')
    f.write(output_string)
    f.close()
    
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
            
            try:
                                
                convert(year, quarter)
                    
            except IOError:
    
                raise IOError('data unavailable: year ' + str(year) + ' , quarter ' + str(quarter))

    return None
