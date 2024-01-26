import os
import csv
import argparse
import shutil
from tremor_accelerometerdata_analysis import freq_analysis, timeseries_analysis
from data_conversion import search_csv
from data_conversion import convert_all_in_dir


def analysis(input_file):
    timeseries_result = timeseries_analysis(input_file, False, False)
    freq_result = freq_analysis(input_file)
    analyzed_result = [input_file,freq_result[9][0],freq_result[9][1],freq_result[9][2],freq_result[9][3],timeseries_result[3],timeseries_result[7],timeseries_result[8],timeseries_result[10],timeseries_result[11]]
    return(analyzed_result)


def analysis_all_in_dir(input_dir, output_file):
    
    # input_dirの中にあるディレクトリの一覧を取得する
    files_dir = [
    f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))
    ]
    
    with open(output_file, 'w') as v:
        writer = csv.writer(v)
        writer.writerow(["filename","RPC_x","RPC_y","RPC_z","RPC_u","TSI","ASI_delta","ASI_IQR","MIPA","SDIPA"])
    # ディレクトリの各々に対してループ廻す
        for f in files_dir:
            # {input_dir}/{f} の中のcsvを全て取得する
            csv_files = search_csv(os.path.join(input_dir, f))
             # analyze
            for files in csv_files:
                result = analysis(os.path.join(input_dir,f,files))
                print(*result, sep=",", file = v)
    return

def get_args():
    parser = argparse.ArgumentParser(
                prog='analysis_wrapper.py', 
                description='input_dir指定、convertedファイルを残すかどうか', 
                epilog='end', 
                add_help=True, 
                )
    parser.add_argument("-d","--input_dir")
    parser.add_argument("--debug", action = "store_true", default = False)
    args = parser.parse_args()
    return(args)

if __name__ == "__main__":
    args = get_args()
    input_dir = args.input_dir
    output_dir = f"{input_dir}-converted"
    output_file = os.path.join(input_dir,"2022arjun_analysis.csv")
    convert_all_in_dir(input_dir, output_dir)
    analysis_all_in_dir(output_dir, output_file)
    if args.debug == False :
        shutil.rmtree(output_dir)
