# -*- coding: utf-8 -*-

import os, glob, shutil

import parse_coupon_csv
import parse_ticket_csv
import merge_coupon_ticket
import aggregate_route_level
import parse_t100

def manual_transfer_reminder():

    print
    print 'manually transfer .zip datafiles to data\\DB1BXXXXXX before continuing'
    print 'e.g. Origin_and_Destination_Survey_DB1BXXXXXXX_2010_1.zip'
    print
    
    raw_input('press a key to continue')
    
    return None

def move_bin_output_to_input():

    for folder in ['..\\output\\*']:
    
        folder_contents = glob.glob(folder)
    
    for src in folder_contents:
        
        if src[-4:] == '.bin':
        
            dst = '..\\input\\' + src.split('..\\output\\')[1]
            
            shutil.move(src, dst)
    
    return None

def move_all_input_to_temp():

    for folder in ['..\\input\\*']:
    
        folder_contents = glob.glob(folder)
        
    for filename in folder_contents:
        
        dst = '..\\temp\\' + filename.split('..\\input\\')[-1]
    
        shutil.move(filename, dst)
    
    return None

def clear_output_temp_input():
    
    for folder in ['..\\output\\*', '..\\temp\\*', '..\\input\\*']:
    
        folder_contents = glob.glob(folder)
    
        for filename in folder_contents:
            os.remove(filename)        
    
    return None

def clear_temp():
    
    for folder in ['..\\temp\\*']:
    
        folder_contents = glob.glob(folder)
    
        for filename in folder_contents:
            os.remove(filename)        
    
    return None
    
def clear_bin_input():

    for folder in ['..\\input\\*']:
    
        folder_contents = glob.glob(folder)
    
    for src in folder_contents:
        
        if src[-4:] == '.bin':
            
            os.remove(src)
    
    return None
    
#manual_transfer_reminder()
#
#print
#print 'clear contents of \output and \\temp and \input'
#    
#clear_output_temp_input()
#
##test_run = True parses Coupon or Ticket for one quarter only
##security = True considers first (security_max) lines only
#
#parse_options = {}
#parse_options['test_run'] = True
#parse_options['security'] = False
#parse_options['security_max'] = 10000
#parse_options['test_periods'] = ([2010], [1])
#parse_options['full_periods'] = (xrange(1993, 2014, 1), xrange(1, 5))
#
#print
#print 'parse DB1B Coupon data from .zip to coupon_year_quarter.bin'
#
#parse_coupon_csv.wrapper(**parse_options)
#
#print
#print 'clear \\temp'
#
#clear_temp()
#
#print
#print 'parse DB1B Ticket data from .zip to coupon_year_quarter.bin'
#
#parse_ticket_csv.wrapper(**parse_options)
#
#print
#print 'clear \\temp'
#
#clear_temp()
#
#print
#print 'move .bin files from \\output to \\input'
#    
#move_bin_output_to_input()
#
#print
#print 'merge Coupon and Ticket .bin files to Itinerary'
#
#merge_coupon_ticket.wrapper(**parse_options)
#
#print 'move all files in \\input to \\temp'
#    
#move_all_input_to_temp()
#
#print
#print 'move .bin files from \\output to \\input'
#
#move_bin_output_to_input()
#
#print 'aggregate itinerary*.bin to route-level'
#
#aggregate_route_level.wrapper(**parse_options)
#
#print
#print 'clear all .bin files from \\input'
#    
#clear_bin_input()

print
print 'parse T-100 .csv files to .bin, save to \\temp'

parse_t100.wrapper(**parse_options)

print
print 'move pyc files (byte code) from \code to \\temp'

src = '.\\'
dst = '..\\temp\\'

for folder in [src + '*.pyc']:
    
    folder_contents = glob.glob(folder)
    
    for filename in folder_contents:        
        filename_split = filename.split('\\')[-1]
        shutil.move(filename, dst + filename_split)
