#!/usr/bin/env python
import sys,os
from break_alog import out_dir

files_in = [
    os.path.join(out_dir, 'r1r2_drtk.alog'),
    os.path.join(out_dir, 'r2r3_drtk.alog'),
    os.path.join(out_dir, 'r1r3_drtk.alog')
]

files_out = [
    os.path.join(out_dir, 'r1r2_drtk_cleaned.alog'),
    os.path.join(out_dir, 'r2r3_drtk_cleaned.alog'),
    os.path.join(out_dir, 'r1r3_drtk_cleaned.alog')
]


for f_in, f_out in zip(files_in, files_out):
    fin = open(f_in, 'r')
    fout = open(f_out, 'w+')

    for line in fin:
        if '%' in line or line[:-1].split()[1] == 'zRpv':
            fout.write(line)

    fout.close(); fin.close()