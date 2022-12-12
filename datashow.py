import glob
import os

import cv2
import matplotlib.pyplot as plt
import numpy as np

#----処理したいデータ---
data = 'Ex_y040_'

#----グリッドの作成----
x = np.arange(0, 96, 1)
y = np.arange(0, 97, 1)
x,y = np.meshgrid(x,y)

#----画像の作成パート----
def data2png(x, y, dataname):

    analyze_name = dataname

    new_dir_path = 'fig/'+analyze_name  #画像を保存するフォルダのパス
    os.makedirs(new_dir_path, exist_ok=True) #画像を保存するフォルダを作成

    for i in range(0, 32):
        fill0num = f'{i:03}' #数値を0埋めで3桁の文字列にする
        loaddata = np.loadtxt('field/'+analyze_name+fill0num+'.txt') #データ読み込み

        fig = plt.figure()
        plt.pcolormesh(x, y, loaddata, cmap='hsv')
        pp = plt.colorbar(orientation='vertical') #カラーバー
        pp.set_label('Intensity', fontname='Arial', fontsize=18) #カラーバーラベル

        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)

        fig.savefig(new_dir_path+'/fig'+fill0num+'.jpg') #画像の保存
        plt.close() #作成した画像を閉じる

#画像の出力
data2png(x, y, data)
print('画像変換完了')


#----動画の作成パート----
def img2mov(dataname):
    out = dataname + 'mov' #作成する動画の名前
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') #コーデックの指定
    fps = 5 #フレームレート
    #width, height = 640, 480
    for i in range(0, 32):
        fill0num = f'{i:03}'
        read_fig = cv2.imread('fig/'+dataname+'/fig'+fill0num+'.jpg') #画像の読み込み
        print('読み込み完了')
        #width, height = read_fig.shape[:2] #画像のサイズ
        out = cv2.VideoWriter(out, fourcc, fps, (640, 480)) #videoweiter
        out.write(read_fig)

    out.release()
    print('動画変換完了')

#動画の出力
img2mov(data)