# -*- coding: utf-8 -*-

import os, glob, shutil, sys

import parse_coupon_csv
import parse_ticket_csv
import merge_coupon_ticket
import aggregate_route_level
import parse_t100
import parse_population_by_msa
import parse_airport_coordinates
import parse_gdp_by_msa
import merge_bin
import data_full_bin_descriptives
                    
def horizontal():
    
    print
    print '-'*90
    print
    
    return None

def manual_transfer_reminder():

    print 'manually transfer .zip datafiles to data\\DB1BXXXXXX before continuing'
    print 'e.g., Origin_and_Destination_Survey_DB1BXXXXXXX_2010_1.zip'
    print
    print '** DISK SPACE REQUIREMENT: ~ 4 GB for 10 quarter parse (temp/ files) **'
    print '** T100 datafiles must be manually renamed after download from U.S. DOT **'
    print
    
    raw_input('press a key to continue')
    
    return None

def clear_output_temp_input():
    
    print 'clear contents of \output and \\temp and \input'

    for folder in ['..\\output\\*', '..\\temp\\*', '..\\input\\*']:
    
        folder_contents = glob.glob(folder)
    
        for filename in folder_contents:
            
            os.remove(filename)
    
    return None

horizontal()
   
manual_transfer_reminder()
horizontal()
    
clear_output_temp_input()
horizontal()

#print 'test_run = True parses Coupon or Ticket for one quarter only'
#print 'security = True considers first (security_max) lines only'

parse_options = {}
parse_options['test_run'] = True
parse_options['security'] = False
parse_options['security_max'] = 10000
parse_options['test_periods'] = ([2013], [4])
parse_options['full_periods'] = (xrange(1993, 2014, 1), xrange(1, 5))

#print 'parse DB1B Coupon data from .zip to coupon_year_quarter.bin'

parse_coupon_csv.wrapper(**parse_options)

#print 'parse DB1B Ticket data from .zip to coupon_year_quarter.bin'

horizontal()

parse_ticket_csv.wrapper(**parse_options)

#print 'merge Coupon and Ticket .bin files to Itinerary'

horizontal()

merge_coupon_ticket.wrapper(**parse_options)

#print 'aggregate itinerary*.bin to route-level'

horizontal()

aggregate_route_level.wrapper(**parse_options)

#print 'parse T-100 .csv files to .bin, save to \\temp'
#print '** note that raw T-100 .zip and .csv must be renamed as yyyy_*.* before use **'

horizontal()

parse_t100.wrapper(**parse_options)

#print 'parse regional population (by MSA) data'

horizontal()

parse_population_by_msa.parse()

#print 'parse airport coordinates'

horizontal()

parse_airport_coordinates.parse()

#print 'parse regional GDP (by MSA) data'

horizontal()

parse_gdp_by_msa.parse()

import build_dataset
import convert_bin_to_text

#print 'filter + add variables to data dictionary'

horizontal()

build_dataset.wrapper(**parse_options)

#print 'convert .bin to .txt'

convert_bin_to_text.wrapper(**parse_options)

#print 'merge .bin files'

horizontal()

merge_bin.wrapper(**parse_options)

#print 'results for text and table of summary statistics'

horizontal()

data_full_bin_descriptives.wrapper(**parse_options)

print
print 'move pyc files (byte code) from \code to \\temp'

src = '.\\'
dst = '..\\temp\\'

for folder in [src + '*.pyc']:
    
    folder_contents = glob.glob(folder)
    
    for filename in folder_contents:
        
        filename_split = filename.split('\\')[-1]
        shutil.move(filename, dst + filename_split)
