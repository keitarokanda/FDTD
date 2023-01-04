import numpy as np
import matplotlib.pyplot as plt

#地表面パラメータ
epsilon_r1 = 4.0
epsilon_r2 = 5.0
losstangent = 0.01
RCS = 1.0
#レーダーパラメータ
P_t = 800 #[W]
P_min = 1e-12 #[W]
G_t = 1.64
f = np.arange(0, 1500, 1)
#光速
c = 299792458 #[m/s]
#最大探査深度
R1 = 10
R2 = 15
R3 = 20
R4 = 25
R5 = 30
R6 = 35
R7 = 40


#反射係数・透過係数
reflection = (np.sqrt(epsilon_r1) - np.sqrt(epsilon_r2))**2 / (np.sqrt(epsilon_r1) + np.sqrt(epsilon_r2))**2
through = 1-reflection


#----計算----
#左辺
left1 = f*10**6/10**(-0.091*np.sqrt(epsilon_r1)*losstangent*R1/5*f)
left2 = f*10**6/10**(-0.091*np.sqrt(epsilon_r1)*losstangent*R2/5*f)
left3 = f*10**6/10**(-0.091*np.sqrt(epsilon_r1)*losstangent*R3/5*f)
left4 = f*10**6/10**(-0.091*np.sqrt(epsilon_r1)*losstangent*R4/5*f)
left5 = f*10**6/10**(-0.091*np.sqrt(epsilon_r1)*losstangent*R5/5*f)
left6 = f*10**6/10**(-0.091*np.sqrt(epsilon_r1)*losstangent*R6/5*f)
left7 = f*10**6/10**(-0.091*np.sqrt(epsilon_r1)*losstangent*R7/5*f)

#右辺
right1 = P_t/P_min * (G_t**2 * c * RCS)/((4*np.pi)**3 * R1**4) * through**2 * reflection + f*0
right2 = P_t/P_min * (G_t**2 * c * RCS)/((4*np.pi)**3 * R2**4) * through**2 * reflection + f*0
right3 = P_t/P_min * (G_t**2 * c * RCS)/((4*np.pi)**3 * R3**4) * through**2 * reflection + f*0
right4 = P_t/P_min * (G_t**2 * c * RCS)/((4*np.pi)**3 * R4**4) * through**2 * reflection + f*0
right5 = P_t/P_min * (G_t**2 * c * RCS)/((4*np.pi)**3 * R5**4) * through**2 * reflection + f*0
right6 = P_t/P_min * (G_t**2 * c * RCS)/((4*np.pi)**3 * R6**4) * through**2 * reflection + f*0
right7 = P_t/P_min * (G_t**2 * c * RCS)/((4*np.pi)**3 * R7**4) * through**2 * reflection + f*0



#----描画----
plt.figure(figsize=(8, 8))
plt.plot(f, left1, color='b', label='left side, R=10' )
plt.plot(f, right1, color='b',linestyle='--', label='right side, R=10' )

plt.plot(f, left2, color='r', label='left side, R=15' )
plt.plot(f, right2, color='r',linestyle='--', label='right side, R=15' )

plt.plot(f, left3, color='g', label='left side, R=20' )
plt.plot(f, right3, color='g',linestyle='--', label='right side, R=20' )

plt.plot(f, left4, color='k', label='left side, R=25' )
plt.plot(f, right4, color='k',linestyle='--', label='right side, R=25' )

plt.plot(f, left5, color='orange', label='left side, R=30' )
plt.plot(f, right5, color='orange',linestyle='--', label='right side, R=30' )

plt.plot(f, left6, color='purple', label='left side, R=35' )
plt.plot(f, right6, color='purple',linestyle='--', label='right side, R=35' )

plt.plot(f, left7, color='yellow', label='left side, R=40' )
plt.plot(f, right7, color='yellow',linestyle='--', label='right side, R=40' )

plt.ylim(10**8, 10**15)
plt.yscale('log')
plt.xlabel('frequency[MHz]')
plt.legend(fontsize = 8)

plt.grid()
plt.show()