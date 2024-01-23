import os
import datetime
import csv
from tremor_accelerometerdata_analysis import freq_analysis, timeseries_analysis
from data_conversion import search_csv


    #freq_analysis(os.path.join("var", "data-20240115101744-converted", "sample1", "Sample1a.csv"))
def analysis(input_file):
    timeseries_result = timeseries_analysis(input_file, False, False)
    freq_result = freq_analysis(input_file)
    analyzed_result = [input_file,freq_result[9][0],freq_result[9][1],freq_result[9][2],freq_result[9][3],timeseries_result[3],timeseries_result[7],timeseries_result[9],timeseries_result[10]]
    return(analyzed_result)


def analysis_all_in_dir(input_dir, output_file):
    # input_dirの中にあるディレクトリの一覧を取得する
    files_dir = [
    f for f in os.listdir(input_dir) if os.path.isdir(os.path.join(input_dir, f))
    ]
    
    with open(output_file, 'w') as v:
        writer = csv.writer(v)
        writer.writerow(["filename","RPC_x","RPC_y","RPC_z","RPC_u","TSI","ASI","MIPA","SDIPA"])
    # ディレクトリの各々に対してループ廻す
        for f in files_dir:
            # {input_dir}/{f} の中のcsvを全て取得する
            csv_files = search_csv(os.path.join(input_dir, f))
             # analyze
            for files in csv_files:
                result = analysis(os.path.join(input_dir,f,files))
                print(result, file = v)
    return


if __name__ == "__main__":
    input_dir = os.path.join("var", "data-20240117154134-converted")
    output_dir = os.path.join("var", f"data-{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}-analyzed")

    analysis_all_in_dir(input_dir, output_dir)
