### 初期設定
region: 200e-9  
dx: 2.5e-9

source: dipole (変更済み)  
pulse: cw (変更済み？)

lambda0: 0.561e-6  
Courant factor: 0.98

mt: 2**15  
mfft:2**9  
extrapol: 4  

msf = 3

mpml = 8   
kappamax = 100.0  
amax = 10.0  
mpow = 3

r1 = 25.0e-9  
Obj('background', 'vacuum', 0, 0),  
Obj('substrate', 'vacuum', (0, 0, r1), 0),  
Obj('sphere', 'vacuum', (0, 0, 0), r1)  

dipoles= (Dipole('z', 'in', 0, 0, -30e-9),)  

savenum = 32  
fieldmons = (savenum, saveint,
        Fmon('Ex', 'y', 0),
        Fmon('Ex', 'z', 0),
        Fmon('Ez', 'y', 0),
        Fmon('Hy', 'x', 0))  
epsmons = (
        Epsmon('x', 'z', 0), \
        Epsmon('x', 'y', 0), \
        Epsmon('z', 'z', 0))  

detectors = (
        Dtct('x', 0, 0, 0),
        Dtct('x', r1 + 5.0e-9, 0, 0),
        Dtct('z', r1 + 5.0e-9, 0, 0),
        Dtct('x', r1, 0, r1),
        Dtct('z', r1, 0, r1),)  


        