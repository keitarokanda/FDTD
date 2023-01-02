import numpy as np
import matplotlib.pyplot as plt

#地表面パラメータ
epsilon_r1 = 4.0
epsilon_r2 = 5.0
losstangent = 0.01
RCS = 1.0

#最大探査深度
R_max = 30.0

#レーダーパラメータ
P_t = 800 #[W]
P_min = 1e-12 #[W]
G_t = 1.64
f = np.arange(0, 500, 1)

#光速
c = 299792458 #[m/s]

#反射係数・透過係数
reflection = (np.sqrt(epsilon_r1) - np.sqrt(epsilon_r2))**2 / (np.sqrt(epsilon_r1) + np.sqrt(epsilon_r2))**2
throw = 1-reflection



#----計算----
#左辺
beta = -0.091*np.sqrt(epsilon_r1)*losstangent*R_max/5
y1 = f*10**6/10**(beta*f)

#右辺
y2 = \
     P_t/P_min * \
    (G_t**2 * c * RCS)/((4*np.pi)**3 * R_max**4) * \
    throw**2 * reflection + f*0


#delta_y = np.abs(y1[f] - y2[f])
#print(min(delta_y))

#交点の座標を取得
idx = np.argwhere(np.sign(np.round(y1 - y2)) == 0)


print(f[idx])
#交点をプロット
plt.plot(f[idx], y1[idx], 'ms', ms=5, label='Intersection', color='green')

#交点の座標をグラフに追記
#for i in idx.ravel():
#    plt.text(f[i], y1[i], '({x}, {y})'.format(x=f[i], y=y1[i]), fontsize=10)


plt.plot(f, y1, color='red', label='left hand')
plt.plot(f, y2, color='blue', label='right hand' )


plt.yscale('log')


plt.xlabel('frequency[MHz]')
plt.legend()
plt.show()