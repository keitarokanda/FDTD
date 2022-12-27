## dipoleの設定
#### コード
Dipole = namedtuple('Dipole', ('pol', 'phase', 'x', 'y', 'z'))
dipoles= (Dipole('z', 'in', 0, 0, 2.0),) # phase: 'in' in-phase, 'anti' antiphase
#### 位置の設定
第１引数：pol→
第２引数：phase→位相
第３引数x→x  
第４引数y→z座標のセッティング？
第５引数z→y座標のセッティング？