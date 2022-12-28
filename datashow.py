import datetime
import os
from turtle import Turtle

import cv2
import matplotlib.colors as colors
import matplotlib.pyplot as plt
import numpy as np

#----処理したいデータ----
data_axis = 'Ex_z'  #x_y, x_z, z_y
data_number = '100_'
data = str(data_axis+data_number)
setting = '_test7'
field = 'epsx_z100'  #x_y, x_z, z_z
data_num = 2**9 #データの数

#----グリッドの作成----
x = np.arange(0, 217, 1)
y = np.arange(0, 217, 1)
x,y = np.meshgrid(x,y)

#----現在自国の取得----
now_time = datetime.datetime.now()

#----画像の作成パート----
def data2fig(x, y, dataname):

    analyze_name = dataname

    new_dir_path = 'test/fig'+setting+'/'+analyze_name  #画像を保存するフォルダのパス
    os.makedirs(new_dir_path, exist_ok=True) #画像を保存するフォルダを作成

    for i in range(0, data_num):
        fill0num = f'{i:03}' #数値を0埋めで3桁の文字列にする
        loaddata = np.abs(np.loadtxt('test/field'+setting+'/'+analyze_name+fill0num+'.txt')) #データ読み込み

        fig = plt.figure()
        plt.pcolormesh(x, y, loaddata, cmap='viridis', shading='auto', norm=colors.LogNorm(vmin=1e-5, vmax=1e1)) #カラーメッシュの作成、カラーバーは対数表示にしている
        pp = plt.colorbar(orientation='vertical') #カラーバー
        pp.set_label('Intensity', fontname='Arial', fontsize=18) #カラーバーラベル


#軸のプロット
        if data_axis == 'Ex_y':
            plt.xlabel('x', fontsize=12)
            plt.ylabel('y', fontsize=12)

        elif data_axis == 'Ex_z':
            plt.xlabel('x', fontsize=12)
            plt.ylabel('z', fontsize=12)

        elif data_axis == 'Ez_y':
            plt.xlabel('z', fontsize=12)
            plt.ylabel('y', fontsize=12)

        plt.title(data+setting+'_'+fill0num)

        fig.savefig(new_dir_path+'/fig'+fill0num+'.jpg') #画像の保存
        plt.close() #作成した画像を閉じる
#画像の出力
data2fig(x, y, data)
print('画像変換完了')


#----動画の作成パート----
def img2mov(dataname):
    outfilename = 'test/fig'+setting+'/'+dataname+'/'+str(now_time)+'.mp4' #作成する動画の名前
    fourcc = cv2.VideoWriter_fourcc('M','P','4','V') #コーデックの指定
    fps = 30 #フレームレート
    width, height = 640, 480 #動画のサイズ
    outfile = cv2.VideoWriter(outfilename, fourcc, fps, (width, height)) #videoweiter
    for i in range(0, data_num):
        fill0num = f'{i:03}'
        read_fig = cv2.imread('test/fig'+setting+'/'+dataname+'/fig'+fill0num+'.jpg') #画像の読み込み
        outfile.write(read_fig)

    outfile.release()
    print('動画変換完了')

#動画の出力
img2mov(data)


#fieldのプロット作成
def field2fig(field_name):
    loaddata = np.loadtxt('test/field'+setting+'/'+field_name+'.txt')

    fig = plt.figure()
    plt.pcolormesh(x, y, loaddata, cmap='Greys', shading='auto', vmin=0, vmax=15.0) 

    pp = plt.colorbar(orientation='vertical') #カラーバー
    pp.set_label('Dielectric Constant', fontname='Arial', fontsize=18) #カラーバーラベル

#軸のプロット
    if data_axis == 'Ex_y':
        plt.xlabel('x', fontsize=12)
        plt.ylabel('y', fontsize=12)

    elif data_axis == 'Ex_z':
        plt.xlabel('x', fontsize=12)
        plt.ylabel('z', fontsize=12)

    elif data_axis == 'Ez_y':
        plt.xlabel('z', fontsize=12)
        plt.ylabel('y', fontsize=12)

    fig.savefig('test/fig'+setting+'/'+field_name+'.jpg') #画像の保存
    plt.close() #作成した画像を閉じる
#画像の出力
field2fig(field)
print('field画像作成完了')
#aiueo


