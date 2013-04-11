#!/usr/bin/env python
""" parses an alog that has been post processed with drtk """
import sys,os
from math import sqrt
from pprint import pprint as pp
import scipy.io as sio
from pdb import set_trace


class TruthData(object):

    r1X = []
    r1Y = []
    r1Z = []
    r2X = []
    r2Y = []
    r2Z = []

    moos_vars = 'zX', 'zY', 'zZ'

    def __init__(self):
        object.__init__(self)

        self.r1_holder = {}
        self.r2_holder = {}
        for v in self.moos_vars:
            self.r1_holder[v] = None
            self.r2_holder[v] = None

    def new_data(self, sens, meas, value):
        holder = getattr(self, sens+'_holder')
        holder[meas] = value
        
        for v in holder.itervalues():
            if not v: return
        #     pp(holder)
        # print 'accepting update'

        for v in self.moos_vars: # need to redo if including stddev
            getattr(self, sens+meas[-1]).append( getattr(self, sens+'_holder')[meas] )




class DrtkAlogData(object):

    time = []
    status = []
    
    lpx = []
    lpy = []
    lpz = []
    mag_lpxyz = []
    lpe = []
    lpn = []
    lpu = []
    
    hpx = []
    hpy = []
    hpz = []
    mag_hpxyz = []
    hpe = []
    hpn = []
    hpu = []
    
    truth = TruthData()

    def __init__(self, novatel_alog, drtk_alog, skip=False):
        object.__init__(self)
        if skip: return
        self.novatel_alog = open(novatel_alog, 'r')
        self.drtk_alog = open(drtk_alog, 'r')
        self.parse_drtk_alog()
        self.parse_novatel_alog()

    def parse_drtk_alog(self):
        for line in self.drtk_alog:
            if '%' in line:
                continue

            sens = line[:-1].split()[2]
            meas = line[:-1].split()[1]

            if meas == 'zRpv':
                data = line[:-1].split()[3].split('{')[1].rstrip('}').split(',')
                self.time.append(float(data[0]))
                self.status.append(int(data[1]))

                self.lpx.append(float(data[2]))
                self.lpy.append(float(data[3]))
                self.lpz.append(float(data[4]))
                self.lpe.append(float(data[5]))
                self.lpn.append(float(data[6]))
                self.lpu.append(float(data[7]))

                self.hpx.append(float(data[8]))
                self.hpy.append(float(data[9]))
                self.hpz.append(float(data[10]))
                self.hpe.append(float(data[11]))
                self.hpn.append(float(data[12]))
                self.hpu.append(float(data[13]))

    def parse_novatel_alog(self):
        for line in self.novatel_alog:
            if '%' in line:
                continue

            sens = line[:-1].split()[2]
            meas = line[:-1].split()[1][:-3]
            # print sens, meas
            if sens in ('r1','r2') and meas in self.truth.moos_vars:
                self.truth.new_data( sens, meas, float(line[:-1].split()[3]) )




alog_dir = '/media/rgcofield/StorageDrive/alog_Files/err_prop/testing/consolidate_log'

r1r2_drtk_alog =    os.path.join(alog_dir, 'output', 'r1r2_drtk_cleaned.alog')
r1r2_novatel_alog = os.path.join(alog_dir, 'output', 'r1r2_novatel.alog')
r2r3_drtk_alog =    os.path.join(alog_dir, 'output', 'r2r3_drtk_cleaned.alog')
r2r3_novatel_alog = os.path.join(alog_dir, 'output', 'r2r3_novatel.alog')
r1r3_drtk_alog =    os.path.join(alog_dir, 'output', 'r1r3_drtk_cleaned.alog')
r1r3_novatel_alog = os.path.join(alog_dir, 'output', 'r1r3_novatel.alog')

r1r2 = DrtkAlogData(r1r2_novatel_alog, r1r2_drtk_alog)
r2r3 = DrtkAlogData(r2r3_novatel_alog, r2r3_drtk_alog)
r1r3 = DrtkAlogData(r1r3_novatel_alog, r1r3_drtk_alog)


# summed 
r1r2r3 = DrtkAlogData(None, None, skip=True)



### output to matlab
r1r2_mat = {}
r2r3_mat = {}
r1r3_mat = {}
for mat,obj in zip( [r1r2_mat, r2r3_mat, r1r3_mat], [r1r2, r2r3, r1r3] ):

        mat['time'] = obj.time,
        mat['status'] = obj.status,

        mat['lpx'] = obj.lpx,
        mat['lpy'] = obj.lpy,
        mat['lpz'] = obj.lpz,
        mat['mag_lpxyz'] = obj.mag_lpxyz
        mat['lpe'] = obj.lpe,
        mat['lpn'] = obj.lpn,
        mat['lpu'] = obj.lpu,

        mat['hpx'] = obj.hpx,
        mat['hpy'] = obj.hpy,
        mat['hpz'] = obj.hpz,
        mat['mag_hpxyz'] = obj.mag_hpxyz
        mat['hpe'] = obj.hpe,
        mat['hpn'] = obj.hpn,
        mat['hpu'] = obj.hpu,

        mat['truth'] = {
            'r1X': obj.truth.r1X,
            'r1Y': obj.truth.r1Y,
            'r1Z': obj.truth.r1Z,
            'r2X': obj.truth.r2X,
            'r2Y': obj.truth.r2Y,
            'r2Z': obj.truth.r2Z
        }


# r2r3_mat = {
#     'lp': {
#         'x': r2r3.lp.x,
#         'y': r2r3.lp.y,
#         'z': r2r3.lp.z,
#         'e': r2r3.lp.e,
#         'n': r2r3.lp.n,
#         'u': r2r3.lp.u,
#         'mag_xyz': r2r3.lp.mag_xyz,
#         'mag_enu': r2r3.lp.mag_enu
#     },
#     'hp': {
#         'x': r2r3.hp.x,
#         'y': r2r3.hp.y,
#         'z': r2r3.hp.z,
#         'e': r2r3.hp.e,
#         'n': r2r3.hp.n,
#         'u': r2r3.hp.u,
#         'mag_xyz': r2r3.hp.mag_xyz,
#         'mag_enu': r2r3.hp.mag_enu
#     },
#     'time': r2r3.time,
#     'status': r2r3.status,
#     'truth': {
#         'r1X': r2r3.truth.r1X,
#         'r1Y': r2r3.truth.r1Y,
#         'r1Z': r2r3.truth.r1Z,
#         'r2X': r2r3.truth.r2X,
#         'r2Y': r2r3.truth.r2Y,
#         'r2Z': r2r3.truth.r2Z
#     }
# }

# r1r3_mat = {
#     'lp': {
#         'x': r1r3.lp.x,
#         'y': r1r3.lp.y,
#         'z': r1r3.lp.z,
#         'e': r1r3.lp.e,
#         'n': r1r3.lp.n,
#         'u': r1r3.lp.u,
#         'mag_xyz': r1r3.lp.mag_xyz,
#         'mag_enu': r1r3.lp.mag_enu
#     },
#     'hp': {
#         'x': r1r3.hp.x,
#         'y': r1r3.hp.y,
#         'z': r1r3.hp.z,
#         'e': r1r3.hp.e,
#         'n': r1r3.hp.n,
#         'u': r1r3.hp.u,
#         'mag_xyz': r1r3.hp.mag_xyz,
#         'mag_enu': r1r3.hp.mag_enu
#     },
#     'time': r1r3.time,
#     'status': r1r3.status,
#     'truth': {
#         'r1X': r1r3.truth.r1X,
#         'r1Y': r1r3.truth.r1Y,
#         'r1Z': r1r3.truth.r1Z,
#         'r2X': r1r3.truth.r2X,
#         'r2Y': r1r3.truth.r2Y,
#         'r2Z': r1r3.truth.r2Z
#     }
# }

mat_out = os.path.join(alog_dir, 'output', 'all3.mat')

sio.savemat(mat_out,
    {
        'r1r2':r1r2_mat,
        'r2r3':r2r3_mat,
        'r1r3':r1r3_mat
    }
)