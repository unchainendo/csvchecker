# coding: utf-8
#!/usr/bin/env python
# Python2.X encoding wrapper (Windows dedicated processing)
"""
＊説明＊
指定したフォルダ、サブフォルダ内のCSVファイルを探索し、指定した列の分散値を表示する
RicecookerRecorderから出力された圧力ファイルに操作があるかを、圧力の合計値の分散があるかどうかで調べるためのもの
＊使い方＊
コマンドプロンプトからこのファイルを指定
探索したいフォルダのパスを要求されるので入力してエンター
＊必要ライブラリ＊
numpy
＊＊
列の指定：L71 read_column_indexの値を変える。デフォルトでは５列目
"""
import codecs
import sys
import os
import os.path
import csv
import numpy
#Import　re          # 正規表現：変数の中には数字しか入ってない事を確認したい
#import xlrd        # excelファイルの読み書き
#import glob
#import Tkinter
sys.stdout = codecs.getwriter('cp932')(sys.stdout)


def main():
    press_threshold = 0          # 圧力分散の閾値
    directoryPath = raw_input('directoryPath>>')
    print directoryPath
    os.chdir(directoryPath)
    for file in search_csv(directoryPath):
        if csv_checker(file):          # csvファイルであるなら出力。 !=Noneは省略可能
            #print csv_checker(file),    # これはreturnの値のファイル名じゃなくて、直接path出力してる
            if pressed_checker(file) > press_threshold:
                print csv_checker(file),
                print int(pressed_checker(file))


#全探索
def search_csv(directory):
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)
            csv_checker(file)


#csv抽出して出力
def csv_checker(csv_file):
    root, ext = os.path.splitext(csv_file)
    if ext == ".csv":
        #pressed_checker(csv_file)
        #print csv_file
        return csv_file
    else:
        return None


#csvに圧力操作があるかチェックして出力
def pressed_checker(csv_file):
    reader = csv.reader(open(csv_file, 'rb'))
    # ファイルの行数を数えて末尾の改行２行を無視する,何故か空改行があると読み込めない
    lines = open(csv_file).readlines()
    lines_max = len(lines)
    #print lines_max,               # 行数表示
    #分散表示
    stdev = []
    read_column_index = 5           # ファイルに指定の列数がないとout of rangeになる。
    for i, row in enumerate(reader):
        #print row
        joined_row = ','.join(row)                      # カンマ（区切り）の個数を調べるために、,で文字列を結合
        comma_count_num = joined_row.count(',')         # ,の数をカウント
        if i == 0 and comma_count_num != 5:             # ５列以外のファイルは圧力ファイルじゃないので無視
            return 0
            break
        elif i == 0 or i == lines_max or i == lines_max-1 or i == lines_max-2:
            pass
        else:
            stdev.append(float(row[read_column_index]))
    #print numpy.std(numpy.array(stdev))
    return numpy.std(numpy.array(stdev))


if __name__ == '__main__':
        main()
