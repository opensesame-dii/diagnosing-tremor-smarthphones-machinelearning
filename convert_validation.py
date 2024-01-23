import pandas as pd
import data_conversion
import matplotlib.pyplot as plt
import numpy as np
import csv

filepath = "var\\accelerometerRecording\\july 22 2015\\AYG\\bat\VibrationData 2015-07-22 at 16 04 02-email.csv"
original_csv = pd.read_csv(filepath, nrows = 1024, skiprows = [0,1,2,3,4,5,6,7,8])

#角速度、地磁気の列追加
original_csv["角速度x"] = 0.1
original_csv["角速度y"] = 0.1
original_csv["角速度z"] = 0.1
original_csv.insert(0,"シーケンス番号", range(1,len(original_csv.index) + 1))
original_csv.insert(1,"地磁気x", 0.1)
original_csv.insert(2,"地磁気y", 0.1)
original_csv.insert(3,"地磁気z", 0.1)
original_csv.drop(original_csv.columns[4], axis = 1, inplace = True)

original_csv.to_csv("formatted.csv",header = True, index = False, encoding = "") 

#上に9行追加
formatted_csv = pd.read_csv('formatted.csv', header = None)
empty_row = pd.DataFrame([['']*len(formatted_csv.columns)],columns = formatted_csv.columns)
for i in range(1,10):
    formatted_csv = pd.concat([empty_row,formatted_csv],ignore_index=True)

#formatted.csv
formatted_csv.to_csv("formatted.csv",header = False,  index = False, encoding = "shift-jis")

#convert 一旦、'4行ごとに読み込み'をコメントアウトしてtimeの計算を*0.005→*0.02にしてます．
data_conversion.convert("formatted.csv", "converted.csv")

#ファイル読み込み
df_ori = pd.read_csv(filepath, header = 0, skiprows = 1037)
df_conv = pd.read_csv("converted.csv", header = 0, skiprows = 1036)

#値格納
original_content = [df_ori['Frequency'].values, df_ori[' X'].values, df_ori['Y'].values, df_ori['Z'].values]
converted_content = [df_conv['frequency'].values, df_conv[' x_fft'].values, df_conv[' y_fft'].values, df_conv[' z_fft '].values]


figure = plt.figure()
axs = []
for i in range(3):
    axs.append(figure.add_subplot(2,2,i+1))
for i in range(3):
    axs[i].plot(original_content[0], original_content[i+1] / np.max(original_content[i+1]), label="original")
    axs[i].plot(converted_content[0], converted_content[i+1] / np.max(converted_content[i+1]), label="converted")
    axs[i].legend()
plt.show()