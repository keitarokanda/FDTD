# ファイル名 'runfdtd.py'



import csv
import time
from collections import namedtuple

#import fdtd
from fdtd import *

if __name__ == "__main__":


#----シミュレーション空間の設定----
    region_size = 20.0
    grid_size = 0.1

    regionx = region_size  # object region
    regiony = region_size  # object region
    regionz = region_size  # object region

    dxtarget = grid_size  # dx [m]
    dytarget = grid_size  # dy [m]
    dztarget = grid_size  # dz [m]
    
    gridnum_x = regionx / dxtarget
    gridnum_y = regiony / dytarget
    gridnum_z = regionz / dztarget


#----電磁波----
    source = 'dipole'  # 'dipole' or 'plane' wave source
    pulse = 'pulse'  # 'pulse' or 'cw' source

#中心波長（真空中）[m]
    lambda0 = 1.0  
#クーラン条件(のCourant factor)
    courantfac = 0.5  

#時間刻み
    time_step = courantfac * dxtarget / 3.0e8
#Coutant条件
    courant_condtion = dxtarget / (3.0e8 *np.sqrt(3))

#時間発展の回数
    mt= 2**8  # must be integer power of 2
#スペクトル計算に用いる時間波形の回数
    mfft= 2**5  # must be integer power of 2
#スペクトル計算時の0充填をサンプリング時間の何倍行うか
    extrapol = 4  
#総計算時間
    total_time = time_step * mt
#進む距離
    reach_ditance = total_time * 3e8

#散乱場領域の大きさ
    msf = 3  # (>=3)
#PMLの層数
    mpml = 8  
#PMLパラメータ
    kappamax = 100.0  
    amax = 10.0  
    mpow = 3  


#球の半径
    r1 = 2.0

    Obj = namedtuple('Obj', ('shape', 'material', 'position', 'size'))

    objs = (
#背景を真空に
        Obj('background', 'vacuum', 0, 0),
#真空中にシリカの板を置く
        Obj('substrate', 'vacuum', (0, 0, r1), 0),
#銀の球
        Obj('sphere', 'vacuum', (0, 0, 0), r1)
        )


#----dipoleのセッティング----
    Dipole = namedtuple('Dipole', ('pol', 'phase', 'x', 'y', 'z'))
    dipoles= (Dipole('z', 'in', 0, 0, 2.0),) # phase: 'in' in-phase, 'anti' antiphase


# ----field monitor----
#出力データ数
    savenum = mt 
#データ保存のインターバル
    saveint = mt//savenum 

    Fmon= namedtuple('Fmon', ('ehfield', 'axis', 'position'))
    fieldmons = (savenum, saveint,
        Fmon('Ex', 'y', 0),
        Fmon('Ex', 'z', 0),
        Fmon('Ez', 'y', 0),
        Fmon('Hy', 'x', 0)
        )


# ----epsilon monitors----
    Epsmon = namedtuple('Epsmon', ('pol', 'axis', 'position'))
    epsmons = (
        Epsmon('x', 'z', 0), \
        Epsmon('x', 'y', 0), \
        Epsmon('z', 'z', 0)
        )


    #r1 = 2.0  # radius of sphere

    Dtct = namedtuple('Dtct', ('pol', 'x', 'y', 'z'))

    detectors = (
        Dtct('x', 0, 0, 0),
        Dtct('x', r1 * 1.5, 0, 0),
        Dtct('z', r1 * 1.5, 0, 0),
        Dtct('x', r1, 0, r1),
        Dtct('z', r1, 0, r1),
        )



    em = Fdtd(\
        source, pulse, lambda0, courantfac, mt, mfft, extrapol, \
        regionx, regiony, regionz, dxtarget, dytarget, dztarget, \
        mpml, msf, kappamax, amax, mpow, \
        objs, fieldmons, epsmons, detectors, dipoles)

    start = time.time()

    em.sweep()

    print('Elapsed time = %f s' % (time.time() - start))


#====setting logの作成====
setting_log = [
    ['region size [m]', regionx, regiony, regionz], \
    ['grid size [m]', dxtarget, dytarget, dztarget], \
    ['number of grid', gridnum_x, gridnum_y, gridnum_z], \
    ['====source setting===='], \
    ['source (dipole/plane)', source], \
    ['type (pulse/cw)', pulse], \
    ['center wavelength [m]', lambda0], \
    ['====time setting===='], \
    ['Courant factor', courantfac], \
    ['time step [sec]', time_step], \
    ['Couran condition [sec]', courant_condtion], 
    ['interaction time', mt], \
    ['mfft', mfft], \
    ['ectrapol', extrapol], \
    ['total time [sec]', total_time], 
    ['maximum propagation distance [m]', reach_ditance], \
    ['====MSF, PML===='], \
    ['number of MSF layer', msf], \
    ['number of PML', mpml, 'kappamax :', kappamax, 'amax :', amax, 'mpow :', mpow], \
    ['====object setting===='], \
    ['radius of sphere [m]', r1], \
    ['Obj'], [objs], \
    ['====diple setting===='], [dipoles], \
    ['====saving setting===='], \
    ['how many times to save result', savenum], \
    ['result saving interval', saveint], \
    ['Fmon'], [fieldmons], \
    ['Epsmon'], [epsmons], \
    ['Dtct'], [detectors], \
    ['elapsed time [sec]', time.time() - start]
    ]

with open('field/0_setting_log.csv', 'w') as f :
    writer = csv.writer(f)
    writer.writerows(setting_log)