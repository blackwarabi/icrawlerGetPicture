'''
Created on 2020/10/31

@author: gon
'''

from icrawler.builtin import BingImageCrawler
import PySimpleGUI as sg
import glob
import subprocess
import threading
import time

#メイン処理
def main():
    sg.theme('Dark Blue 3')

    layout = [
                [sg.Text('保存先',size=(6,1)),sg.Input(size=(20,1) ,key='folderPath',disabled=True),sg.FolderBrowse('選択',key='inputFolderPath')],
                [sg.Text('取得したい画像の名称を入力',size=(30,1))],
                [sg.InputText('', size=(40,1),key='getSearchName')],
                [sg.Text('画像枚数',size=(8,1)),sg.Combo(('10','20','30','40','50'),default_value='10', size=(4,1),key='getNum')],
                [sg.Button('画像取得', key='imggetstart'),sg.Button('クリア', key='clear')],
                [sg.Output(size=(50, 10),key='output')]
            ]
    window = sg.Window('画像集めくん beta', layout)

    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            break
        if event == 'clear':
            #クリア処理
            window['getSearchName'].update('')
            window['getNum'].update('10')
        if event == 'imggetstart':
            #入力チェック
            if values['folderPath'] == '' or values['getSearchName'] == '':
                print('未入力の項目があります。確認してください。')
                continue

            #実行前にイメージフォルダに画像があれば警告して処理しない
            checkdir = glob.glob(values['inputFolderPath']+"/*")
            if len(checkdir) > 0:
                print('保存先にファイルが存在します。空のフォルダを選択してください。')
                continue

            print('処理開始')
            #表示のタイミングを合わせるため1秒待つ
            time.sleep(1)
            #画像の取得処理を行う
            #処理中の画面の応答なし状態を防ぐため、Threadにする
            thread = threading.Thread(target=bingCrawler, args=(values['inputFolderPath'],values['getSearchName'],values['getNum'],))
            thread.start()

    window.close()

#クローラー作成と実行処理
def bingCrawler(folderPath,getSearchName,getNum):
    #Bing用クローラーの生成
    bing_crawler = BingImageCrawler(
        downloader_threads=4,                  #ダウンローダーのスレッド数
        storage={'root_dir': folderPath})      #ダウンロード先のディレクトリ名

    #キーワード検索による画像収集
    bing_crawler.crawl(keyword=getSearchName,max_num=int(getNum))
    #表示のタイミングを合わせるため2秒待つ
    time.sleep(2)
    print('処理終了')
    #メッセージ表示後に画像をダウンロードしたフォルダを開く
    subprocess.run('explorer {}'.format(folderPath.replace('/','\\')))

if __name__ == '__main__':
    main()