# 使い方
    
## analysis_wrapper.py 
### 概要
- 解析対象のディレクトリを指定すると、ディレクトリ下にあるcsvファイルを読み取り、論文で用いられているデータ形式に変換(convert)して解析する。
- filename,RPC_x,RPC_y,RPC_z,RPC_u,TSI_arjun,ASI_delta,ASI_IQR,MIPA,SDIPAをまとめた"2022arjun_analysis.csv"ファイルが解析対象のディレクトリ下に出力される。  

解析対象のディレクトリは，[tremor_analysis_python](https://github.com/opensesame-dii/tremor_analysis_python)のmultiple.pyで生成される，data-YYYYMMDDhhmmのディレクトリ(患者名/計測名/ファイル名.csvという構造が格納されたもの)

### 実行方法
- opensesame_diagnosing-tremor-smarthphones-machinelearning ディレクトリのターミナル上で以下のコマンド入力で解析を実行、ファイルを出力   
    - `python analysis_wrapper.py -d 解析対象ディレクトリのpath`  

- --debug をつけるとconvertされたファイルを含むディレクトリ("解析対象ディレクトリのpath-converted")も出力  
    - `python analysis_wrapper.py -d 解析対象ディレクトリのpath --debug`
