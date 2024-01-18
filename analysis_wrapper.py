import os
import pandas as pd
import datetime
from tremor_accelerometerdata_analysis import freq_analysis, timeseries_analysis
from data_conversion import search_csv
import csv


    #freq_analysis(os.path.join("var", "data-20240115101744-converted", "sample1", "Sample1a.csv"))
def analysis(input_file, analyzed_file):
    with open(f'{input_file}_timeseries_analysis', 'w') as f_a:
        timeseries_result = timeseries_analysis(input_file, False, False)
        print(timeseries_result, file = f_a)
    
    with open(f'{input_file}_freq_analysis', 'w') as f_f:
        freq_result = freq_analysis(input_file)
        print(freq_result, file = f_f)
    #値をcsvに書き出し
    with open(analyzed_file ,"w") as v:
        writer = csv.writer(v)
        writer.writerow(["filename","RPC","TSI","ASI","MIPA","SDIPA"])
        writer.writerow([input_file,freq_result[9],timeseries_result[3],timeseries_result[7],timeseries_result[9],timeseries_result[10]])
        #print("filename",input_file,"\nTSI", timeseries_result[3],"\nASI", timeseries_result[7],"\nMIPA", timeseries_result[9],"\nSDIPA", timeseries_result[10],"\nRPC", freq_result[9])
    return


def analysis_all_in_dir(input_dir, output_dir):
    # input_dirの中にあるディレクトリの一覧を取得する
    files_dir = [
    f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))
    ]
    print(files_dir)
    # output_dirを作る
    os.mkdir(output_dir)
    # ディレクトリの各々に対してループ廻す
    for f in files_dir:
        # output_dirの中に，ディレクトリを作る
        new_dir = os.path.join(output_dir,f)
        os.mkdir(new_dir)

        # {input_dir}/{f} の中のcsvを全て取得する
        csv_files = search_csv(os.path.join(input_dir, f))
        print(csv_files)
        # analyze
        for files in csv_files:
            analysis(os.path.join(input_dir,f,files), os.path.join(new_dir, files))
    return

if __name__ == "__main__":
    input_dir = os.path.join("var", "data-20240117154134-converted")
    output_dir = os.path.join("var", f"data-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-analyzed")

    analysis_all_in_dir(input_dir, output_dir)
