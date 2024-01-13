import pandas as pd
import glob
import os
import datetime


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
    empty_row = pd.DataFrame([['']*len(df3.columns)],columns = df3.columns)
    for i in range(1,11):
        df3 = pd.concat([empty_row,df3],ignore_index=True)

    #csv ファイル出力
    df3.to_csv(converted_file, float_format = "",header = True, index = False, encoding = "utf-8")


def convert_all_in_dir(input_dir, output_dir):
    # output_dirを作る
    os.mkdir(output_dir)
    # input_dirの中にあるディレクトリの一覧を取得する
    files_dir = [
        f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))
    ]
    print(files_dir)
    # ディレクトリの各々に対してループ廻す
    for f in files_dir:
        # output_dirの中に，ディレクトリを作る
        new_dir = os.path.join(output_dir,f)
        os.mkdir(new_dir)

        # {input_dir}/{f} の中のcsvを全て取得する
        csv_files = glob.glob('*.csv', root_dir = os.path.join(input_dir, f))
        print(csv_files)
        # ↑のそれぞれをconvertする
        for files in csv_files:
            convert(os.path.join(input_dir,f,files), os.path.join(new_dir, files))

    return

if __name__ == "__main__":
    input_dir = os.path.join("var", "data-YYYYMMDDhhmm")
    output_dir = os.path.join("var", f"data-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-converted")

    convert_all_in_dir(input_dir, output_dir)
