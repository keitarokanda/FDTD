# ファイル名 'runfdtd.py'



import csv
import time
from collections import namedtuple

#import fdtd
from fdtd import *

if __name__ == "__main__":


#----シミュレーション空間の設定----
    regionx = 30.0  # object region
    regiony = 30.0  # object region
    regionz = 30.0  # object region
    dxtarget = 3.0e-1  # dx [m]
    dytarget = 3.0e-1  # dy [m]
    dztarget = 3.0e-1  # dz [m]


#----電磁波----
    source = 'dipole'  # 'dipole' or 'plane' wave source
    pulse = 'pulse'  # 'pulse' or 'cw' source

#中心波長（真空中）[m]
    lambda0 = 1.0  
#クーラン条件(のCourant factor)
    courantfac = 0.5  

#時間発展の回数
    mt= 2**8  # must be integer power of 2
#スペクトル計算に用いる時間波形の回数
    mfft= 2**5  # must be integer power of 2
#スペクトル計算時の0充填をサンプリング時間の何倍行うか
    extrapol = 4  


#散乱場領域の大きさ
    msf = 3  # (>=3)
#PMLの層数
    mpml = 8  
#PMLパラメータ
    kappamax = 100.0  
    amax = 10.0  
    mpow = 3  


#球の半径
    r1 = 1.0

    Obj = namedtuple('Obj', ('shape', 'material', 'position', 'size'))

    objs = (
#背景を真空に
        Obj('background', 'vacuum', 0, 0),
#真空中にシリカの板を置く
        Obj('substrate', 'vacuum', (0, 0, r1), 0),
#銀の球
        Obj('sphere', 'vacuum', (0, 0, 0), r1)
        )



    Dipole = namedtuple('Dipole', ('pol', 'phase', 'x', 'y', 'z'))
    dipoles= (Dipole('z', 'in', 0, 0, 0),) # phase: 'in' in-phase, 'anti' antiphase


# ----field monitor----
#出力データ数
    savenum = 2**8 
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


    r1 = 5.0  # radius of sphere

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

setting_log = [
    ['region', regionx, regiony, regionz], \
    ['meshsize', dxtarget, dytarget, dztarget], \
    ['source', source], \
    ['pulsse', pulse]
    ]

with open('field/settingcsv', 'w') as f :
    writer = csv.writer(f)
    writer.writerows(setting_log)
