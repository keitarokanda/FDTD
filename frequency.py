import numpy as np
import matplotlib.pyplot as plt
from scipy import optimize

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
f = np.arange(100, 501, 1)

#光速
c = 299792458 #[m/s]




#反射係数・透過係数
reflection = (np.sqrt(epsilon_r1) - np.sqrt(epsilon_r2))**2 / (np.sqrt(epsilon_r1) + np.sqrt(epsilon_r2))**2
throw = 1-reflection

#右辺
right_hand = \
    P_t/P_min * \
    (G_t**2 * c * RCS)/((4*np.pi)**3 * R_max**4) * \
    throw**2 * reflection

#左辺
beta = -0.091 * np.sqrt(epsilon_r1) * losstangent *R_max / 5

y1 = f*10**6/10**(beta*f)
y2 = right_hand

#交点の座標を取得
idx = np.argwhere(np.sign(y1 - y2) == 0)

#交点をプロット
plt.plot(f[idx], y1[idx], 'ms', ms=5, label='Intersection', color='green')
plt.xlabel('f')

#交点の座標をグラフに追記
for i in idx.ravel():
    plt.text(x[i], y1[i], '({x}, {y})'.format(x=x[i], y=y1[i]), fontsize=10)

plt.plot(f, y1, color='red', label='y1')
plt.axhline(y=y2, xmin=0, xmax=6, )


plt.yscale('log')

plt.xlabel('frequency[MHz]')
plt.legend()
plt.show()