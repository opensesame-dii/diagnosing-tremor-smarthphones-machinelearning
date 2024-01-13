import pandas as pd

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

input_file = "sample/Tsuboi_Tremor_Sample2"
converted_file = "sample/Tsuboi_Tremor_Sample2_conv.csv"
convert(input_file,converted_file)