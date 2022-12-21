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
savenum : 256 
実行時間 : 