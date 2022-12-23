### 22/12/19  
* 空間設定
*region : $40 \times 40 \times 40$  
セルサイズ : $0.4 \times 0.4 \times 0.4$
lambda0 : 0.75  
* 時間設定
Courant factor : $S = 0.98$  
$ \delta t = S \frac{\delta x}{c} = 0.1306...\times 10^{-8} \mathrm{sec}$
mt : $2 ^{15}$
総計算時間 $= \delta t \times mt$
* その他
媒質 : 全てvacuum   
r1 : 8.0  
savenum : 50 
実行時間 : 6700秒くらいだったような...

### 22/12/20
* 空間設定
wave source : dipole  
type : cw  
region : $40 \times 40 \times 40$  
セルサイズ : $0.4 \times 0.4 \times 0.4$
lambda0 : 0.75  
* 時間設定
Courant factor : 0.98 
$ \delta t = S \frac{\delta x}{c} = 0.1306...\times 10^{-8} \mathrm{sec}$
mt : $2 ^{15}$
総計算時間 $= \delta t \times mt$
* その他
媒質 : 全てvacuum  
r1 : 8.0
savenum : 250 
実行時間 : 14142秒


### 22/12/21
* 空間設定
region : $10 \times 10 \times 10$  
セルサイズ : $0.01 \times 0.01 \times 0.01$
lambda0 : 1.0
* 時間設定
Courant factor : 0.98 
$ \delta t = S \frac{\delta x}{c} = 0.1306...\times 10^{-8} \mathrm{sec}$
mt : $2 ^{15}$
総計算時間 $= \delta t \times mt$
* その他
媒質 : 全てvacuum  
r1 : 1.0
savenum : 250 
実行時間 : 途中でクラッシュ 

### 22/12/21_2
* 空間設定
region : $10 \times 10 \times 10$  
セルサイズ : $0.1 \times 0.1 \times 0.1$
lambda0 : 1.0
* 時間設定
Courant factor : 0.98 
$ \delta t = S \frac{\delta x}{c} = 0.1306...\times 10^{-8} \mathrm{sec}$
mt : $2 ^{15}$
総計算時間 $= \delta t \times mt$
* その他
媒質 : 全てvacuum  
r1 : 1.0
savenum : 50 
実行時間 : 13927.5 sec  

### 22/12/21_3
* 空間設定
region : $40 \times 40 \times 40$  
セルサイズ : $0.4 \times 0.4 \times 0.4$
lambda0 : 1.0
* 時間設定
Courant factor : 0.5 
$ \delta t = S \frac{\delta x}{c} = 6.67...\times 10^{-10} \mathrm{sec}$
mt : $256 (=2 ^{8})$
mfft : 32
総計算時間 $= \delta t \times mt = 1.71 \times 10^{-5} \mathrm{sec}$
* その他
媒質 : 全てvacuum  
r1 : 1.0
dipoleの位置：(0,0,0)
savenum : 256 
実行時間 : 124.1秒  

### 22/12/21_4
* 波源設定
dipole  
pulse
* 空間設定
region : $40 \times 40 \times 40$  
セルサイズ : $0.4 \times 0.4 \times 0.4$
lambda0 : 1.0
* 時間設定
Courant factor : 0.5 
$ \delta t = S \frac{\delta x}{c} = 6.67...\times 10^{-10} \mathrm{sec}$
mt : $256 (=2 ^{8})$
mfft : 32
総計算時間 $= \delta t \times mt = 1.71 \times 10^{-5} \mathrm{sec}$
* その他
媒質 : 全てvacuum  
r1 : 5.0
dipoleの位置：(0,0,0)
savenum : 256 
実行時間 : 124秒くらい？

### 22/12/21_5　　
* 波源設定
dipole  
pulse
* 空間設定
region : $40 \times 40 \times 40$  
セルサイズ : $0.1 \times 0.1 \times 0.1$
lambda0 : 1.0
* 時間設定
Courant factor : 0.5 
$ \delta t = S \frac{\delta x}{c} = 1.67...\times 10^{-10} \mathrm{sec}$
mt : $256 (=2 ^{8})$
mfft : 32
総計算時間 $= \delta t \times mt = 4.27 \times 10^{-8} \mathrm{sec}$
進むはずの距離 $4.27 \times 10^{-8} \times 3.0 \times 10^{8} = 12.8 \mathrm{m}$
* その他
媒質 : 全てvacuum  
r1 : 5.0
dipoleの位置：(0,0,0)
savenum : 256 
実行時間 : 9197.6秒　　

### 22/12/22
* 波源設定
dipole  
pulse
* 空間設定
region : $30 \times 30 \times 30$  
セルサイズ : $0.075 \times 0.075 \times 0.075 \\ (400 \times 400 \times 400 \mathrm{grid})$
lambda0 : $0.75$
* 時間設定
Courant factor : 0.5  
Coutant条件 $\leq 1.46 \times 10^{-10}$
$ \delta t = S \frac{\delta x}{c} = 1.25...\times 10^{-10} \mathrm{sec}$
mt : $512 (=2 ^{9})$
mfft : 32
総計算時間 $= \delta t \times mt = 6.40 \times 10^{-8} \mathrm{sec}$
進むはずの距離 $6.40 \times 10^{-8} \times 3.0 \times 10^{8} = 19.2 \mathrm{m}$
* その他
媒質 : 全てvacuum  
r1 : 5.0
dipoleの位置：(0,0,0)
savenum : 512 
実行時間 : 18182.2秒