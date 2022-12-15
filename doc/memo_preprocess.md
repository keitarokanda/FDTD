### コンストラクタの定義
1. self
2. source
    波源（双極子/平面波）
3. pulse
    入射波（パルス/cw）
4. lambda0
    中心周波数
5. courantfac
    ？？？
6. mt
    時間発展の回数
7. mfft
    ペクトル計算に用いる時間波形のサンプリング数
8. extrapol
    スペクトル計算の0充填をサンプリング数の何倍行うか
9. regionx, regiony, regionz
    物体空間の大きさ
10. dxtarget, dytarget, dztarget
    メッシュサイズ
11. mpml
    PMLの層数
12. msf
    散乱場領域の幅
13. kappamax, amax, mpow
    PMLパラメータ３種類
14. objs
    物体空間に配置する物体の指定
15. fieldmons
    座標軸に垂直な断面の電場分布または磁場分布を一定時間間隔で保存するためのパラメータを指定
16. epsmons
    保存する座標軸に垂直な断面の媒質の分布の位置を指定
17. detectors
    時間発展波形及びスペクトルを保存する電場/磁場、及びその位置を指定
18. dipoles
    波源としての双極子の変更、位相、位置の指定

### いらんやつ
ADE法のセッティング（最後の部分）