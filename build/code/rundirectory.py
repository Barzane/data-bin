# -*- coding: utf-8 -*-

import os, glob, shutil

import parse_coupon_csv

print
print 'manually transfer .zip datafiles to data\\DB1BCoupon before continuing'
print 'e.g. Origin_and_Destination_Survey_DB1BCoupon_2010_1.zip'
print

raw_input('press a key to continue')

print
print 'clear contents of \output and \\temp and \input'

sss

for folder in ['..\\output\\*', '..\\temp\\*', '..\\input\\*']:

    folder_contents = glob.glob(folder)

    for filename in folder_contents:
        os.remove(filename)

print 'parse DB1B Coupon data from .zip to coupon_year_quarter.bin'

#test_run = True parses Coupon for one quarter only
#security = True considers first (security_max) lines only

coupon_parse_options = {}
coupon_parse_options['test_run'] = False
coupon_parse_options['security'] = True
coupon_parse_options['security_max'] = 10000

parse_coupon_csv.wrapper(**coupon_parse_options)

print
print 'move pyc files (byte code) from \code to \\temp'
    
src = '.\\'
dst = '..\\temp\\'

for folder in [src + '*.pyc']:
    
    folder_contents = glob.glob(folder)
    
    for filename in folder_contents:        
        filename_split = filename.split('\\')[-1]
        shutil.move(filename, dst + filename_split)
