import pandas as pd
import glob
import os
import datetime
import numpy as np
import numpy.fft as fft

def convert(input_file,converted_file):

    df = pd.read_csv(input_file, header = 9, encoding = "shift-jis")

    #余分な列（地磁気、角速度）削除
    df.drop(df.columns[[1,2,3,7,8,9]], axis = 1, inplace = True)

    #シーケンス番号 をtimeに置き換え→　実際のファイルでは'index' かな
    df2 = df.rename({"シーケンス番号":"time"},axis = 1)
    df2["time"] = (df2["time"]-1)*0.005

    #4行ずつとりだし
    df3 = df2[::4]

    #上に10行追加←これだとヘッダーの下に追加される
    empty_row = pd.DataFrame([['a']*len(df3.columns)],columns = df3.columns)
    for i in range(1,11):
        df3 = pd.concat([empty_row,df3],ignore_index=True)

    #csv ファイル出力
    df3.to_csv(converted_file, float_format = "",header = True, index = False, encoding = "utf-8")

    f = open(converted_file)

    for i in range(10):
        line = f.readline()

    sample_rate = 50

    line = f.readline()

    t = []
    x = []
    y = []
    z = []

    while line != "":
        line = f.readline()
        line = line.strip()
        line_list = line.strip().split(",")
        line_len = len(line_list)
        if line == "" or line_len < 4:
            break

        #Obtains the current time and position and stores them in the corresponding arrays
        t_cur = float(line_list[0])
        x_cur = float(line_list[1])
        y_cur = float(line_list[2])
        z_cur = float(line_list[3])
        t.append(t_cur)
        x.append(x_cur)
        y.append(y_cur)
        z.append(z_cur)
    f.close()

    x = np.array(x)
    y = np.array(y)
    z = np.array(z)
    x_trend_removed = x - np.mean(x)
    y_trend_removed = y - np.mean(y)
    z_trend_removed = z - np.mean(z)

    x_fft = fft.fft(x_trend_removed * np.hamming(len(x)))
    y_fft = fft.fft(y_trend_removed * np.hamming(len(x)))
    z_fft = fft.fft(z_trend_removed * np.hamming(len(x)))
    x_fft = np.abs(x_fft)
    y_fft = np.abs(y_fft)
    z_fft = np.abs(z_fft)
    freq_fft = fft.fftfreq(len(x_fft), 1/sample_rate)

    with open(converted_file,"a") as f:
        f.write("\n\nfrequency, x_fft, y_fft, z_fft \n")
        for i in range(len(x_fft)//2):
            f.write(f"{freq_fft[i]}, {x_fft[i]}, {y_fft[i]}, {z_fft[i]}\n")


def convert_all_in_dir(input_dir, output_dir):
    # ディレクトリが存在しない場合output_dirを作ってconvert
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

        # input_dirの中にあるディレクトリの一覧を取得する
        files_dir = [
            f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))
        ]
        #print(files_dir)
        # ディレクトリの各々に対してループ廻す
        for f in files_dir:
            # output_dirの中に，ディレクトリを作る
            new_dir = os.path.join(output_dir,f)
            os.mkdir(new_dir)

            # {input_dir}/{f} の中のcsvを全て取得する
            csv_files = search_csv(os.path.join(input_dir, f))
            #print(csv_files)
            # ↑のそれぞれをconvertする
            for files in csv_files:
                convert(os.path.join(input_dir,f,files), os.path.join(new_dir, files))
    else:
        print(f"{output_dir}already exist")

    return

def search_csv(rootdir):
    file_list = []
    for root, directories, files in os.walk(rootdir):
        for file in files:
            if(file.endswith(".csv")):
                file_list.append(file)
    return file_list

if __name__ == "__main__":
    input_dir = os.path.join("var", "data-YYYYMMDDhhmm")
    output_dir = os.path.join("var", f"data-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-converted")

    convert_all_in_dir(input_dir, output_dir)
