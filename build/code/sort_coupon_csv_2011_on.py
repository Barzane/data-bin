# -*- coding: utf-8 -*-

import time, segment_timer, os

def sort_coupon_csv(dst_csv_2011q1_to_2013q4_temp, dst_csv, year, quarter):
    
    data_reader = open(dst_csv_2011q1_to_2013q4_temp, 'r')
    
    print
    print '[sorting file] ' + dst_csv_2011q1_to_2013q4_temp
    
    t_start = segment_timer.timer(True)
    
    key_list = []
    
    h = 'X'
    
    while h != '':
        
        flag = True
        
        bp = data_reader.tell()
        
        while flag:
            
            data_reader.seek(bp)
            h = data_reader.readline()
            check_itin_id = h.split(',')[0][:4]
            h_ = h.split(',')
            
            try:
                
                if bp != 0 and eval(check_itin_id) != year:
                    
                    bp -= 1   
                    
                else:
                    
                    flag = False                   
                    
            except SyntaxError:
                
#                fiddle : may lose last line (or more) of file?
                
                flag = False
                h = ''
                
        if bp != 0 and h != '':
            
            key_itin_id = h_[0].split('"')[-1]
            seq_num = h_[2]
            
            if eval(seq_num) <= 9:
                
                key_a = eval(key_itin_id + '0' + seq_num)
                
            else:
                
                key_a = eval(key_itin_id + seq_num)
                
            key_list.append([key_a, bp])
                
        if len(key_list)%100000 == 0:
            
            print len(key_list)
    
    key_list.sort()
    
    print 'sorted keys'
    print ('runtime : %0.3f seconds'%(segment_timer.timer(False, t_start)))
    
    t_start = segment_timer.timer(True)
    
#    remove repeated items from key_list
#    (possibly created by byte position (backwards) correction above)
    
    key_list_ = []
    
    count_duplicates = 0
    
    for idx in range(len(key_list) - 1):
        
        if key_list[idx][0] != key_list[idx + 1][0]:
            
            key_list_.append(key_list[idx])
            
        else:
            
            count_duplicates += 1
            
    key_list_.append(key_list[-1])

    print 'removed duplicates :', count_duplicates
    print ('runtime : %0.3f seconds'%(segment_timer.timer(False, t_start)))
    
    t_start = segment_timer.timer(True)
    
    print '[saving sorted file] ' + dst_csv    
    
    f = open(dst_csv, 'w')
    
    data_reader.seek(0)
    line_out = data_reader.readline()
    
    f.write(line_out)
    
    for key in key_list_:
        
        catch_byte = key[1]
        data_reader.seek(catch_byte)
        line_out=data_reader.readline()
        f.write(line_out)

    f.close()
    
    data_reader.close()
    
    print 'end of sort'
    print ('runtime : %0.3f seconds'%(segment_timer.timer(False, t_start)))

    print '[deleting unsorted .csv] ' + dst_csv_2011q1_to_2013q4_temp
    os.remove(dst_csv_2011q1_to_2013q4_temp)
    
    print
    
    return None
