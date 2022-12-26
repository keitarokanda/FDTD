import glob
import os
from locale import normalize

import cv2
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

#----処理したいデータ---
data = 'Ex_y200_'
setting = '_(221225)'

#----グリッドの作成----
x = np.arange(0, 416, 1)
y = np.arange(0, 417, 1)
x,y = np.meshgrid(x,y)

#----画像の作成パート----
def data2fig(x, y, dataname):

    analyze_name = dataname

    new_dir_path = 'fig/fig'+setting+'/'+analyze_name  #画像を保存するフォルダのパス
    os.makedirs(new_dir_path, exist_ok=True) #画像を保存するフォルダを作成

    for i in range(0, 512):
        fill0num = f'{i:03}' #数値を0埋めで3桁の文字列にする
        loaddata = np.loadtxt('field_/field'+setting+'/'+analyze_name+fill0num+'.txt') #データ読み込み
        max_value = max(loaddata[2])

        fig = plt.figure()
        plt.pcolormesh(x, y, loaddata, cmap='coolwarm', shading='auto', norm=colors.LogNorm(vmin=1e-5, vmax=1e0)) #カラーメッシュの作成、カラーバーは対数表示にしている
        pp = plt.colorbar(orientation='vertical') #カラーバー
        pp.set_label('Intensity', fontname='Arial', fontsize=18) #カラーバーラベル

        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)

        fig.savefig(new_dir_path+'/fig'+fill0num+'.jpg') #画像の保存
        plt.close() #作成した画像を閉じる
#画像の出力
data2fig(x, y, data)
print('画像変換完了')


#----動画の作成パート----
def img2mov(dataname):
    outfilename = 'fig/fig'+setting+'/'+dataname+'/'+dataname+'.mp4' #作成する動画の名前
    fourcc = cv2.VideoWriter_fourcc('M','P','4','V') #コーデックの指定
    fps = 30 #フレームレート
    width, height = 640, 480 #動画のサイズ
    outfile = cv2.VideoWriter(outfilename, fourcc, fps, (width, height)) #videoweiter
    for i in range(0, 512):
        fill0num = f'{i:03}'
        read_fig = cv2.imread('fig/fig'+setting+'/'+dataname+'/fig'+fill0num+'.jpg') #画像の読み込み
        outfile.write(read_fig)

    outfile.release()
    print('動画変換完了')

#動画の出力
img2mov(data)

#aiueo


