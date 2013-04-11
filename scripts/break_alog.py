#!/usr/bin/env python
""" take alog of all three receivers and make three alogs
    r1r2.alog
    r2r3.alog
    r1r3.alog
"""
import sys,os
from copy import deepcopy as dcp


raw = open('/media/rgcofield/StorageDrive/alog_Files/err_prop/testing/consolidate_log/MOOSLog_10_4_2013_____16_01_17/MOOSLog_10_4_2013_____16_01_17.alog',  'r')
out_dir =  '/media/rgcofield/StorageDrive/alog_Files/err_prop/testing/consolidate_log/output'
r1r2_out = open(os.path.join(out_dir, 'r1r2_novatel.alog'), 'w+')
r2r3_out = open(os.path.join(out_dir, 'r2r3_novatel.alog'), 'w+')
r1r3_out = open(os.path.join(out_dir, 'r1r3_novatel.alog'), 'w+')
header = []

for line in raw: 
    if '%' in line: # send header to all files
        for f in r1r2_out, r2r3_out, r1r3_out:
            f.write(line)
        continue

    sens = line[:-1].split()[2]
    # direct each line to proper file
    if sens == 'r1':
        r1r2_out.write(line)
        r1r3_out.write(line)
    elif sens == 'r2':
        r1r2_out.write(line)
        # r2 becomes r1 in r2r3
        line = line.replace('_r2 ', '_r1 ').replace(' r2 ', ' r1 ')
        r2r3_out.write(line)    
    elif sens == 'r3':
        # r3 becomes r2 in r2r3 and r1r3
        line = line.replace('_r3 ', '_r2 ').replace(' r3 ', ' r2 ')
        r2r3_out.write(line)
        r1r3_out.write(line)


for f in r1r2_out, r2r3_out, r1r3_out:
    f.close()
