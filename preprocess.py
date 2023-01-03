# ファイル名 'preprocess.py'



import math
import sys
from collections import namedtuple

import numpy as np


#----'Preprocess'クラスの定義----
class Preprocess():


#----コンストラクタの定義----
    def __init__(
            self, source, pulse, lambda0, courantfac, \
            mt, mfft, extrapol, \
            regionx, regiony, regionz, dxtarget, dytarget, dztarget, \
            mpml, msf, kappamax, amax, mpow, \
            objs, fieldmons, epsmons, detectors, dipoles):
    
        self._constants()


#----波源の選択（処理はfdtdの中で）----
        if source == 'plane' or source == 'dipole':
            self.source = source
        else:
            print('Error: no such source! ', source)
            sys.exit() #エラーあればプログラムを終了


#----パルス波/cw波----
        if pulse == 'pulse' or pulse == 'cw':
            self.pulse = pulse
        else:
            print('Error: no such source! ', pulse)
            sys.exit() #エラーあればプログラムを終了

#----時間発展の回数----
        self.mt = mt
#----スペクトル計算に用いる時間波形のサンプリング数----
        self.mfft = mfft

        self.sampint = mt//mfft
#----スペクトル計算の0充填をサンプリング数の何倍行うか----
        self.extrapol = extrapol        
#----中心各周波数の計算：ω=2πf----
        self.omega0 = 2.0* math.pi* self.cc/ lambda0

        self.mfft2 = self.mfft* self.extrapol

        
#----gridの定義？---
        self._setgrid(regionx, regiony, regionz, dxtarget, dytarget, dztarget,mpml, msf)

        self._set_param(courantfac)
#----PMLのアレイ作ってる？----
        self._create_arrays(mpml)
#----座標軸に垂直な断面の電場分布または磁場分布を一定時間間隔で保存するためのパラメータを指定----
        self._set_fieldmon(fieldmons)
#----保存する座標軸に垂直な断面の媒質の分布の位置を指定----
        self._set_epsmons(epsmons)


        if self.source == 'dipole':
            self._set_dipoles(dipoles)


#----時間発展波形及びスペクトルを保存する電場/磁場、及びその位置を指定----
        self._set_detectors(detectors)
#----波源の中心波長？----
        self._set_materials(lambda0)
#----物体空間に配置する物体の設定----
        self._set_objects(objs)

        self._devparam()
#----PMLのパラメータ----
        self._cpmlparam(mpml, kappamax, amax, mpow)



#----物理定数メソッドの定義----
    def _constants(self):
        self.cc = 2.99792458e8  #新空中の光速[m/s]
        self.mu0 = 4.0* math.pi*1.0e-7  # permeability of free space [H/m]
        self.eps0 = 1.0 / (self.cc*self.cc*self.mu0) #真空の誘電率[F/m]
        self.zz0 = math.sqrt(self.mu0/self.eps0)  #真空のインピーダンス

#----グリッド作成メソッドの定義----
    def _setgrid(self, regionx, regiony, regionz, dxtarget, dytarget, dztarget, mpml, msf):

        self.mx = round(regionx/dxtarget) #小数を丸めて
        self.my = round(regiony/dytarget)
        self.mz = round(regionz/dztarget)

#----セルの大きさ----
        self.dx = regionx/self.mx 
        self.dy = regiony/self.my
        self.dz = regionz/self.mz

#----物体空間の原点----
        self.x0 = regionx/2 
        self.y0 = regiony/2
        self.z0 = regionz/2


#----散乱領域の設定----
        if self.source == 'dipole':
            msf = 0
        else:
            msf= msf


#--------計算空間のセッティング--------
#mx1→mx0のこと、mx2→mx1のこと？添字変わってる？


#セル数の話
#----散乱場の始まりの座標（x方向）----
        self.mx1 = mpml  
#----シミュレーション空間の大きさ（x方向）----
        self.mxx = self.mx + mpml*2 + msf*2
#----散乱場領域の端っこの座標（x方向）----
        self.mx2 = self.mx1 + self.mx + msf*2
#----物体領域の始まりの座標（x）----
        self.mox1 = self.mx1 + msf
#----物体領域の端っこの座標（x）
        self.mox2 = self.mx2 - msf  


#----　シミュレーション空間の大きさ（y方向）----
        self.myy = self.my + mpml*2 + msf*2
#----散乱場領域の始まりの座標（y方向）----
        self.my1 = mpml 
#----散乱場領域の端っこの座標（y方向）----
        self.my2 = self.my1 + self.my + msf*2
#----物体領域の始まりの座標（y）----
        self.moy1 = self.my1 + msf  
#----物体領域の端っこの座標（y）----
        self.moy2 = self.my2 - msf  


#----　シミュレーション空間の大きさ（z）----
        self.mzz = self.mz + mpml*2 + msf*2
#----散乱場領域の始まりの座標（z）----
        self.mz1 = mpml  
#----散乱場領域の端っこの座標（z）----
        self.mz2 = self.mz1 + self.mz + msf*2
#----物体領域の始まりの座標（z）----
        self.moz1 = self.mz1 + msf  
#----物体領域の終わりの座標（z）----
        self.moz2 = self.mz2 - msf  

#----TF/SF interface (z-position)  for source calculation----
        self.izst= self.mz1 + msf - 2

        
#----アレイの作成----
    def _create_arrays(self, mpml):

        """
        Creating arrays for fields
        """

        self.idx = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1), dtype=np.int)
        self.idy = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1), dtype=np.int)
        self.idz = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1), dtype=np.int)

        self.isdx = np.zeros((self.mzz+ 1), dtype=np.int)
        self.isdy = np.zeros((self.mzz+ 1), dtype=np.int)
        self.isdz = np.zeros((self.mzz+ 1), dtype=np.int)



        self.Ex1 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Ey1 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Ez1 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))

        self.Hx1 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Hy1 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Hz1 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))

        self.Ex2 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Ey2 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Ez2 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))

        self.Hx2 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Hy2 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))
        self.Hz2 = np.zeros((self.mzz+ 1, self.myy+ 1, self.mxx+ 1))



        self.psiEzx1m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiEyx1m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiEzx2m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiEyx2m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))

        self.psiHzx1m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiHyx1m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiHzx2m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiHyx2m = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))



        self.psiEzx1p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiEyx1p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiEzx2p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiEyx2p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))

        self.psiHzx1p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiHyx1p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiHzx2p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))
        self.psiHyx2p = np.zeros((self.mzz+ 1, self.myy+ 1, mpml))



        self.psiExy1m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiEzy1m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiExy2m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiEzy2m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))

        self.psiHxy1m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiHzy1m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiHxy2m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiHzy2m = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))



        self.psiExy1p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiEzy1p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiExy2p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiEzy2p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))

        self.psiHxy1p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiHzy1p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiHxy2p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))
        self.psiHzy2p = np.zeros((self.mzz+ 1, mpml, self.mxx+ 1))



        self.psiEyz1m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiExz1m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiEyz2m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiExz2m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))

        self.psiHyz1m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiHxz1m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiHyz2m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiHxz2m = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))



        self.psiEyz1p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiExz1p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiEyz2p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiExz2p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))

        self.psiHyz1p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiHxz1p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiHyz2p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))
        self.psiHxz2p = np.zeros((mpml, self.myy+ 1, self.mxx+ 1))



        self.px2 = np.zeros((self.mxx+ 1, self.myy+ 1, self.mzz+ 1))
        self.py2 = np.zeros((self.mxx+ 1, self.myy+ 1, self.mzz+ 1))
        self.pz2 = np.zeros((self.mxx+ 1, self.myy+ 1, self.mzz+ 1))



        self.SEx1 = np.zeros(self.mzz+1)
        self.SEx2 = np.zeros(self.mzz+1)

        self.SHy1 = np.zeros(self.mzz)
        self.SHy2 = np.zeros(self.mzz)



        self.SpsiExz1m = np.zeros(mpml)
        self.SpsiExz2m = np.zeros(mpml)

        self.SpsiHyz1m = np.zeros(mpml)
        self.SpsiHyz2m = np.zeros(mpml)

        self.SpsiExz1p = np.zeros(mpml)
        self.SpsiExz2p = np.zeros(mpml)

        self.SpsiHyz1p = np.zeros(mpml)
        self.SpsiHyz2p = np.zeros(mpml)

        

        self.spx2 = np.zeros(self.mzz)
        self.spy2 = np.zeros(self.mzz)
        self.spz2 = np.zeros(self.mzz)



        self.esource = np.zeros(self.mt)



    def _set_param(self, courantfac):

        
#----時間ステップの計算----
        self.dt = courantfac/ (self.cc* \

            math.sqrt(1.0/ self.dx/ self.dx + 1.0/ self.dy/ self.dy \

            + 1.0/ self.dz/ self.dz))

        

# coefficients for time developement

        self.ce = self.dt/self.eps0

        self.coefe = self.dt/self.eps0

        self.coefh = self.dt/self.mu0

        self.cex0 = self.dt/self.dx/self.eps0

        self.cey0 = self.dt/self.dy/self.eps0

        self.cez0 = self.dt/self.dz/self.eps0

        self.chx0 = self.dt/self.dx/self.mu0

        self.chy0 = self.dt/self.dy/self.mu0

        self.chz0 = self.dt/self.dz/self.mu0


#----媒質をセッティングするメソッド----
    def _set_materials(self, lambda0):


        self.matermax = 20 # 0:vacuum
        self.diemax = 10 # 1-diemax: for constant permittivity
        self.drumax = 20 # diemax-drumax: for Drude


        self.epsr = np.ones(self.drumax)

        self.sigma = np.zeros(self.drumax)

        self.epsinf = np.ones(self.drumax)

        self.omegap = np.ones(self.drumax)

        self.gamma = np.zeros(self.drumax)

        self.deps = np.zeros(self.drumax)

#媒質の呼び名を決めてる？----
        self.name2mat = {'vacuum':0, 'SiO2':1, 'Ag':11, 'Au':12}


#真空
        self.epsr[self.name2mat['vacuum']] = 1.0
        self.sigma[self.name2mat['vacuum']] = 0.0
        self.epsinf[self.name2mat['vacuum']] = 1.0

#SiO2(silica)
        self.epsr[self.name2mat['SiO2']] = self._eps_sio2(lambda0*1.0e6)
        self.sigma[self.name2mat['SiO2']] = 0.0
        self.epsinf[self.name2mat['SiO2']] = self.epsr[self.name2mat['SiO2']]

# silver J&C (best fit between 400-800nm)
        self.epsr[self.name2mat['Ag']] = 1.0
        self.epsinf[self.name2mat['Ag']] = 4.07669   # epsilon_\infty
        self.omegap[self.name2mat['Ag']] = 1.40052e16  # [rad/s]
        self.gamma[self.name2mat['Ag']] = 4.21776e13  # [rad/s]

# gold J&C (best fit between 521-1937.3nm)
        self.epsr[self.name2mat['Au']] = 1.0
        self.epsinf[self.name2mat['Au']] = 10.3829  # epsilon_\infty
        self.omegap[self.name2mat['Au']] = 1.37498e16  # [rad/s]
        self.gamma[self.name2mat['Au']] = 1.18128e14  # [rad/s]


#シリカの誘電率を波長の関数で定義？
    def _eps_sio2(self, wavelength):

        """ Dielectric constant of SiO2 as a function of wavelength (um)"""

        a0 = 2.087510310
        a1 = 7.18480736e-3
        a2 = 1.44309144e-2
        a3 = 7.20981855e-4
        a4 = 4.85560050e-5
        a5 = 8.92406983e-7

        ee = a0 + a1*wavelength**2 + a2/wavelength**2 - a3/wavelength**4 + a4/wavelength**6 - a5/wavelength**8

        return ee

    
#置く物体の定義
    def _set_objects(self, objs):

        """ setting objects """

        self.bgmater = 0

        for obj in objs:

            objshape = obj.shape

#背景？
            if objshape == 'background':
                self._background(obj)
#球
            elif objshape == 'sphere':
                self._sphere(obj)
#厚板？
            elif objshape == 'slab':
                self._slab(obj)
#平面基板？
            elif objshape == 'substrate':
                self._substrate(obj)
#その他はエラー
            else:
                print('Error: no such shape! ', objshape)
                sys.exit()


#背景のセッティング
    def _background(self, obj):

        """ setting dielectric constant of background """

        

        self.bgmater = self.name2mat[obj.material]

        self.idx[:,:,:] = self.bgmater

        self.idy[:,:,:] = self.bgmater

        self.idz[:,:,:] = self.bgmater

        

        self.isdx[:] = self.bgmater

        self.isdy[:] = self.bgmater

        self.isdz[:] = self.bgmater


#球のセッティング
    def _sphere(self, obj):
        """ setting sphere """

        materialid = self.name2mat[obj.material]

        rr = obj.size*obj.size #半径の2乗？

        for iz in range(self.moz1, self.moz2): #moz1→moz0のこと、moz2→moz1のこと？物体領域の端から端まで
            z = (iz-self.moz1+0.5)*self.dz - self.z0 - obj.position[2] #z座標？

            for iy in range(self.moy1, self.moy2):
                y = (iy-self.moy1+0.5)*self.dy - self.y0 - obj.position[1] #y座標？

                for ix in range(self.mox1, self.mox2):
                    x = (ix-self.mox1+0.5)* self.dx - self.x0-  obj.position[0] #x座標？

                    if x*x + y*y + z*z <= rr: #球の中
                        for jj in [0, 1]:
                            for ii in [0, 1]:
                                iix = ix
                                iiy = iy + ii
                                iiz = iz + jj

                                if iix >= 0 and iix <= self.mxx and iiy >= 0 and iiy <= self.myy and iiz >= 0 and iiz <= self.mzz:
                                    self.idx[iiz,iiy,iix] = materialid
                                iix = ix + ii
                                iiy = iy
                                iiz = iz + jj

#                                if iix >= 0 and iix <= self.mxx and iiy >= 0 and iiy <= self.myy and iiz >= 0 and iiz <= self.mzz:
#                                    self.idy[iiz,iiy,iix] = materialid
#                                iix = ix + ii
#                                iiy = iy + jj
#                                iiz = iz

#                                if iix >= 0 and iix <= self.mxx and iiy >= 0 and iiy <= self.myy and iiz >= 0 and iiz <= self.mzz:
#                                    self.idz[iiz,iiy,iix] = materialid


#slabのセッティング
    def _slab(self, obj):

        """ setting slab """


        materialid = self.name2mat[obj.material]

        izmin = math.ceil((self.z0 + obj.position[2] - object.size[2]/ 2.0)/self.dz + self.moz1 - 0.5)

        izmax = math.floor((self.z0 + obj.position[2] + object.size[2]/ 2.0)/self.dz + self.moz1+ 0.5)


        for iz in range(izmin, izmax+ 1):

            self.isdx[iz] = materialid

            self.isdy[iz] = materialid

            if iz >= 0 and iz <= self.mzz:

                for iy in range(0, self.myy+1):

                    for ix in range(0, self.mxx+1):

                        self.idx[iz,iy,ix] = materialid

                        self.idy[iz,iy,ix] = materialid



        for iz in range(izmin, izmax):

            self.isdz[iz] = materialid

            if iz >= 0 and iz <= self.mzz:

                if iy in range(0, self.myy+ 1):

                    if ix in range(0, self.mxx+ 1):

                        self.idz[iz,iy,iz]= materialid


#平面基板のセッティング
    def _substrate(self, obj):

        """ setting substrate """


        materialid = self.name2mat[obj.material]

        izmin = math.ceil((self.z0 + obj.position[2])/self.dz + self.moz1 - 0.5)


        for iz in range(izmin, self.mzz+ 1):

            if iz >= 0 and iz <= self.mzz:

                self.isdx[iz] = materialid

                self.isdy[iz] = materialid

                for iy in range(0, self.myy+1):

                    for ix in range(0, self.mxx+1):

                        self.idx[iz,iy,ix] = materialid

                        self.idy[iz,iy,ix] = materialid

        for iz in range(izmin, self.mzz):

            if iz >= 0 and iz <= self.mzz:

                self.isdz[iz] = materialid

                for iy in range(0, self.myy+ 1):

                    for ix in range(0, self.mxx+ 1):

                        self.idz[iz,iy,ix] = materialid



    def _set_fieldmon(self, fieldmons):

        

        self.savenum= fieldmons[0]

        self.saveint= fieldmons[1]

        self.ifieldmons= []

        Fmon2= namedtuple('Fmon2', ('ehfield', 'axis', 'position', 'prefix'))

    

        for fieldmon in fieldmons[2:]:

            if fieldmon.axis == 'x':

                if fieldmon.ehfield == 'Ex' or fieldmon.ehfield == 'Hy' or fieldmon.ehfield == 'Hz':

                    posi0 = math.floor((self.x0+fieldmon.position)/self.dx)

                else:

                    posi0 = round((self.x0+fieldmon.position)/self.dx)

                posi = posi0 + self.mox1

                if posi < 0 or posi > self.mxx:

                    print('Error: fieldmon location is out of range !')

                    sys.exit()

            elif fieldmon.axis == 'y':

                if fieldmon.ehfield == 'Ey' or fieldmon.ehfield == 'Hx' or fieldmon.ehfield == 'Hz':

                    posi0 = math.floor((self.y0+fieldmon.position)/self.dy)

                else:

                    posi0 = round((self.y0+fieldmon.position)/self.dy)

                posi = posi0 + self.moz1

                if posi < 0 or posi > self.myy:

                    print('Error: fieldmon location is out of range !')

                    sys.exit()

            else:

                if fieldmon.ehfield == 'Ez' or fieldmon.ehfield == 'Hx' or fieldmon.ehfield == 'Hy':

                    posi0 = round((self.z0+fieldmon.position)/self.dz)

                    posi = posi0 + self.moz1

                else:

                    posi0 = round((self.z0+fieldmon.position)/self.dz)

                posi= posi0 + self.moz1

                if posi < 0 or posi > self.mzz:

                    print('Error: fieldmon location is out of range !')

                    sys.exit()

    

            prefix = './field/' + fieldmon.ehfield + '_' + fieldmon.axis + '{0:0>3}'.format(posi0) + '_'

                

            self.ifieldmons.append( \

                Fmon2(fieldmon.ehfield, fieldmon.axis, posi, prefix))



    def _set_epsmons(self, epsmons):



        self.iepsmons= []

        Epsmon2= namedtuple('Epsmon2', ('pol', 'axis', 'position', 'fname'))

    

        for epsmon in epsmons:

            if epsmon.axis == 'x':

                if epsmon.pol == 'x':

                    posi0 = math.floor((self.x0+epsmon.position)/self.dx)

                    posi = posi0 + self.mox1

                elif epsmon.pol == 'y':

                    posi0 = round((self.y0+epsmon.position)/self.dy)

                    posi = posi0 + self.moy1

                else:

                    posi0 = round((self.z0+epsmon.position)/self.dz)

                    posi = posi0 + self.moz1

                if posi < 0 or posi > self.mxx:

                    print('Error: epsmon location is out of range !')

                    sys.exit()

            elif epsmon.axis == 'y':

                if epsmon.pol == 'x':

                    posi0 = round((self.x0+epsmon.position)/self.dx)

                    posi = posi0 + self.mox1

                elif epsmon.pol == 'y':

                    posi0 = math.floor((self.y0+epsmon.position)/self.dy)

                    posi = posi0 + self.moy1

                else:

                    posi0 = round((self.z0+epsmon.position)/self.dz)

                    posi = posi0 + self.moz1

                if posi < 0 or posi > self.myy:

                    print('Error: epsmon location is out of range !')

                    sys.exit()

            else:

                if epsmon.pol == 'x':

                    posi0 = round((self.x0+epsmon.position)/self.dx)

                    posi = posi0 + self.mox1

                elif epsmon.pol == 'y':

                    posi0 = round((self.y0+epsmon.position)/self.dy)

                    posi= posi0 + self.moy1

                else:

                    posi0 = math.floor((self.z0+epsmon.position)/self.dz)

                    posit = posi0 + self.moz1

                if posi < 0 or posi > self.mzz:

                    print('Error: epsmon location is out of range !')

                    sys.exit()

                

            fname = './field/eps' + epsmon.pol + '_' + epsmon.axis + str(posi0) + '.txt'

                    

            self.iepsmons.append( \

                Epsmon2(epsmon.pol, epsmon.axis, posi, fname))


#========双極子波源のセッティング========
    def _set_dipoles(self, dipoles):


        self.idipoles= []

        Dipole2= namedtuple('Dipole2', ('pol', 'phase', 'ix', 'iy', 'iz'))


        for dipole in dipoles:

#双極子の位置
            if dipole.pol == 'x':
                ix = math.floor((self.x0+dipole.x)/self.dx) + self.mox1
                iy = round((self.y0+dipole.y)/self.dy) + self.moy1
                iz = round((self.z0+dipole.z)/self.dz) + self.moz1

            elif dipole.pol == 'y':
                ix = round((self.x0+dipole.x)/self.dx) + self.mox1
                iy = math.floor((self.y0+dipole.y)/self.dy) + self.moy1
                iz = round((self.z0+dipole.z)/self.dz) + self.moz1

            else:
                ix = round((self.x0+dipole.x)/self.dx) + self.mox1
                iy = round((self.y0+dipole.y)/self.dy) + self.moy1
                iz = math.floor((self.z0+dipole.z)/self.dz) + self.moz1

#双極子の位置がシミュレーション空間の外になってる場合エラー
            if ix < 0 or ix > self.mxx or iy < 0 or iy > self.myy or iz < 0 or iz > self.mzz:
                print('Error: dipole location is out of range !')
                sys.exit()


#電磁波の位相？
            if dipole.phase == 'in':
                phase = 1

            else:
                phase = -1

                

        self.idipoles.append(Dipole2(dipole.pol, phase, ix, iy, iz))



#========detectorのセッティング========
    def _set_detectors(self, detectors):


        self.idetectors= []

        Dtct2= namedtuple('Dtct2', ('pol', 'x', 'y', 'z'))


        for detector in detectors:

#detectorの位置
            if detector.pol == 'x':
                ix = math.floor((self.x0+detector.x)/self.dx) + self.mox1
                iy = round((self.y0+detector.y)/self.dy) + self.moy1
                iz = round((self.z0+detector.z)/self.dz) + self.moz1

            elif detector.pol == 'y':
                ix = round((self.x0+detector.x)/self.dx) + self.mox1
                iy = math.floor((self.y0+detector.y)/self.dy) + self.moy1
                iz = round((self.z0+detector.z)/self.dz) + self.moz1

            else:
                ix = round((self.x0+detector.x)/self.dx) + self.mox1
                iy = round((self.y0+detector.y)/self.dy) + self.moy1
                iz = math.floor((self.z0+detector.z)/self.dz) + self.moz1

#detectorの位置がシミュレーション空間の外になってる場合エラー
            if ix < 0 or ix > self.mxx or iy < 0 or iy > self.myy or iz < 0 or iz > self.mzz:
                print('Error: detector location is out of range !')
                sys.exit()


            self.idetectors.append(Dtct2(detector.pol, ix, iy, iz))


        self.edetect = np.zeros((len(self.idetectors), self.mt))



#========PMLパラメータのセッティング========
    def _cpmlparam(self, mpml, kappamax, amax, mpow):

        """ parameter for CPML """


        self.ckex = np.zeros(self.mxx+1)
        self.ckey = np.zeros(self.myy+1)
        self.ckez = np.zeros(self.mzz+1)

        self.ckhx1 = np.zeros(self.mxx+1)
        self.ckhy1 = np.zeros(self.myy+1)
        self.ckhz1 = np.zeros(self.mzz+1)


        self.cbxe = np.zeros(mpml+1)
        self.cbye = np.zeros(mpml+1)
        self.cbze = np.zeros(mpml+1)

        self.cbxh = np.zeros(mpml)
        self.cbyh = np.zeros(mpml)
        self.cbzh = np.zeros(mpml)


        self.ccxe = np.zeros(mpml+1)
        self.ccye = np.zeros(mpml+1)
        self.ccze = np.zeros(mpml+1)

        self.ccxh = np.zeros(mpml)
        self.ccyh = np.zeros(mpml)
        self.cczh = np.zeros(mpml)


#----x方向----
        sigmamax = -(mpow+1)*self.eps0*self.cc*math.log(1.0e-8) / (2.0*mpml*self.dx)


        for ix in range(mpml+ 1):

            sig = sigmamax * ((mpml-ix)/mpml)**mpow

            kappa = 1.0 + (kappamax-1.0)*((mpml- ix)/ mpml)**mpow

            alpha = amax* ix/mpml

            self.ckex[ix] = 1.0/kappa/self.dx
            self.cbxe[ix] = math.exp(-(alpha+ sig/ kappa)*(self.dt/self.eps0))
            self.ccxe[ix] = -(1.0-self.cbxe[ix])*(sig/kappa) / (sig+alpha*kappa)/self.dx


        for ix in range(mpml):

            sig = sigmamax* ((mpml-ix-0.5)/ mpml)**mpow

            kappa= 1.0 + (kappamax-1.0)*((mpml-ix-0.5)/mpml)**mpow

            alpha = amax*(ix+ 0.5)/mpml

            self.ckhx1[ix] = self.chx0/kappa
            self.cbxh[ix] = math.exp(-(alpha+sig/kappa)*(self.dt/self.eps0))
            self.ccxh[ix] = -(1.0-self.cbxh[ix])* (sig/kappa) / (sig+alpha* kappa)/self.dx


        self.ckex[self.mx2:self.mxx+1] = self.ckex[mpml::-1]
        self.ckhx1[self.mx2:self.mxx] = self.ckhx1[mpml-1::-1]


        self.ckex[self.mx1+1:self.mx2] = 1.0/self.dx
        self.ckhx1[self.mx1:self.mx2] = self.chx0

#----y方向----


        sigmamax= -(mpow+1)*self.eps0*self.cc*math.log(1.0e-8) / (2.0*mpml*self.dy)


        for iy in range(mpml+1):

            sig = sigmamax * ((mpml-iy)/mpml)**mpow

            kappa = 1.0 + (kappamax-1.0)*((mpml-iy)/ mpml)**mpow

            alpha = amax* iy/mpml

            self.ckey[iy]= 1.0/kappa/self.dy
            self.cbye[iy] = math.exp(-(alpha+ sig/kappa)*(self.dt/self.eps0))
            self.ccye[iy]= -(1.0-self.cbye[iy])* (sig/kappa)/(sig+alpha*kappa)/self.dy

        

        for iy in range(mpml):

            sig = sigmamax * ((mpml-iy-0.5)/mpml)**mpow

            kappa = 1.0 + (kappamax-1.0)*((mpml-iy-0.5)/mpml)**mpow

            alpha = amax*(iy+ 0.5)/mpml

            self.ckhy1[iy] = self.chy0/kappa
            self.cbyh[iy] = math.exp(-(alpha+sig/ kappa)*(self.dt/ self.eps0))
            self.ccyh[iy] = -(1.0-self.cbyh[iy]) * (sig/kappa)/(sig+alpha*kappa)/self.dy


        self.ckey[self.my2:self.myy+1] = self.ckey[mpml::-1]
        self.ckhy1[self.my2:self.myy] = self.ckhy1[mpml-1::-1]


        self.ckey[self.my1+1:self.my2] = 1.0/self.dy

        self.ckhy1[self.my1:self.my2] = self.chy0


        # z direction

        sigmamax= -(mpow+1)*self.eps0*self.cc*math.log(1.0e-8) / (2.0* mpml*self.dz)


        for iz in range(mpml+1):

            sig= sigmamax * ((mpml-iz)/ mpml)**mpow

            kappa= 1.0 + (kappamax-1.0)*((mpml-iz)/mpml)**mpow

            alpha= amax* iz/mpml

            self.ckez[iz] = 1.0/kappa/self.dz
            self.cbze[iz] = math.exp(-(alpha+sig/kappa)*(self.dt/self.eps0))
            self.ccze[iz]= -(1.0-self.cbze[iz]) * (sig/kappa)/(sig+alpha*kappa)/self.dz


        for iz in range(mpml):

            sig = sigmamax * ((mpml-iz-0.5)/mpml)**mpow

            kappa = 1.0 + (kappamax-1.0)*((mpml-iz-0.5)/mpml)**mpow

            alpha = amax* (iz+ 0.5)/mpml

            self.ckhz1[iz] = self.chz0/kappa
            self.cbzh[iz] = math.exp(-(alpha+sig/kappa)*(self.dt/self.eps0))
            self.cczh[iz]= -(1.0-self.cbzh[iz]) * (sig/kappa)/(sig+alpha*kappa)/self.dz


        self.ckez[self.mz2:self.mzz+1] = self.ckez[mpml::-1]
        self.ckhz1[self.mz2:self.mzz] = self.ckhz1[mpml-1::-1]


        self.ckez[self.mz1+1:self.mz2] = 1.0/self.dz
        self.ckhz1[self.mz1:self.mz2] = self.chz0


#========分散性媒質の取り扱いに必要な補助微分方程式(ADE)法=======
    def _devparam(self):

        """  parameter for development with ADE """


        self.ce1 = np.zeros(self.drumax)
        self.ce2 = np.zeros(self.drumax)
        self.ce3 = np.zeros(self.drumax)

        self.cj1 = np.zeros(self.drumax)
        self.cj2 = np.zeros(self.drumax)
        self.cj3 = np.zeros(self.drumax)

        self.cex2 = np.zeros(self.drumax)
        self.cey2 = np.zeros(self.drumax)
        self.cez2 = np.zeros(self.drumax)



        for imater in range(self.diemax):

            self.cj1[imater] = 1.0
            self.cj3[imater] = 0.0

            temp1 = self.eps0*self.epsinf[imater]/self.dt - self.sigma[imater]/2.0
            temp2 = self.eps0* self.epsinf[imater]/self.dt + self.sigma[imater]/ 2.0

            self.ce1[imater] = temp1/temp2
            self.ce2[imater] = 1.0/temp2
            self.ce3[imater] = 1.0


        for imater in range(self.diemax, self.drumax):

            self.cj1[imater] = (1.0-self.gamma[imater]*self.dt/ 2.0) / (1.0+self.gamma[imater]*self.dt/2.0)
            self.cj3[imater] = (self.eps0*self.omegap[imater] * self.omegap[imater]*self.dt/2.0) / (1.0+self.gamma[imater]*self.dt/2.0)

            temp1 = self.eps0*self.epsinf[imater]/self.dt - self.cj3[imater]/2.0
            temp2 = self.eps0*self.epsinf[imater]/self.dt + self.cj3[imater]/2.0

            self.ce1[imater] = temp1/temp2
            self.ce2[imater] = 1.0/temp2
            self.ce3[imater] = self.ce2[imater]* (1.0+self.cj1[imater])/2.0

    

        for imater in range(self.drumax):

            self.cex2[imater] = self.ce2[imater]/self.dx
            self.cey2[imater] = self.ce2[imater]/self.dy
            self.cez2[imater] = self.ce2[imater]/self.dz
