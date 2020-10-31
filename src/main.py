'''
Created on 2020/10/31

@author: gon
'''

from icrawler.builtin import BingImageCrawler
import os
import shutil
import PySimpleGUI as sg
import glob

sg.theme('Dark Blue 3')

layout = [
            [sg.Text('保存先',size=(6,1)),sg.Input(size=(20,1) ,key='folderPath',disabled=True),sg.FolderBrowse('選択',key='inputFolderPath')],
            [sg.Text('取得したい画像の名称を入力',size=(30,1))],
            [sg.InputText('', size=(40,1),key='getSearchName')],
            [sg.Text('画像枚数',size=(8,1)),sg.Combo(('10','20','30','40','50','60','70','80','90','100'),default_value='10', size=(4,1),key='getNum')],
            [sg.Button('画像取得', key='imggetstart'),sg.Button('クリア', key='clear')],
            [sg.Output(size=(50, 10),key='output')]
        ]
window = sg.Window('画像集めくん beta', layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
            break
    if event == 'clear':
            window['getSearchName'].update('')
            window['getNum'].update('10')
    if event == 'imggetstart':
        checkdir = glob.glob(values['inputFolderPath']+"/*")
        #実行前にイメージファルダに画像があれば警告してしょりしない

        if values['folderPath'] == '' or values['getSearchName'] == '':
            print('未入力の項目があります。確認してください。')
            continue

        if len(checkdir) > 0:
            print('保存先にファイルが存在します。空のフォルダを選択してください。')
            continue
        print('処理中')
        #Bing用クローラーの生成
        bing_crawler = BingImageCrawler(
            downloader_threads=4,           #ダウンローダーのスレッド数
            storage={'root_dir': values['inputFolderPath']}) #ダウンロード先のディレクトリ名

        #キーワード検索による画像収集
        bing_crawler.crawl(keyword=values['getSearchName'],max_num=int(values['getNum']))
        print('画像を取得しました。')

window.close()