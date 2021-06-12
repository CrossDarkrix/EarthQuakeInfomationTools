# -*- coding: utf-8 -*-
"""
Colorful Getting Earthquake Infomation from YahooJapan
Version: 3.0
Author: DarkRix
"""

from colorama import init as Starting
from colorama import Fore, Back
import urllib.request
from bs4 import BeautifulSoup
Starting()

def replace_word(EqData):
    replaceword0 = '発生時刻\n'
    replaceword1 = '震源地\n'
    replaceword2 = '最大震度\n'
    replaceword3 = 'マグニチュード\n'
    replaceword4 = '深さ\n'
    replaceword5 = '緯度/経度\n'
    replaceword6 = '情報\n'
    replaceword7 = '。\n'
    replaceword8 = '                    '
    replaceword9 = '詳細を見る'
    replaceword10 = '         '
    replaceword11 = '       '
    replaceword12 = '\r'
    replaceword13 = '\n\n'
    replaceword14 = '\t\r'
    replaceword15 = '\n\n\n'
    replaceword16 = '\n   '
    replaceword17 = '  '
    replaceword18 = '。'
    replaceword19 = '>>津波情報を見る'
    replaceword20 = '\n \n \n'
    replaceword21 = '\n\n '
    replaceword22 = ':\n'
    replaceword23 = '\n ・'
    replaceword24 = ' ・'
    replaceword25 = ':北'
    replaceword26 = 'M '
    replaceword27 = '  '
    replaceword28 = ' \n'
    replaceword29 = ': '
    replaceword30 = ':'

    replacedword0 = ''
    replacedword1 = '・発生時刻: '
    replacedword2 = '・震源地: '
    replacedword3 = '・最大震度: '
    replacedword4 = '・地震の規模: M'
    replacedword5 = '・深さ: '
    replacedword6 = '・緯度/経度: '
    replacedword7 = '・津波情報: '
    replacedword8 = ': '
    replacedword9 = '\n\n・'
    replacedword10 = '\n\n・'
    replacedword11 = ': 北'
    replacedword12 = 'M'
    replacedword13 = ' '
    replacedword14 = '\n'
    replacedword15 = ':'
    replacedword16 = ': '
    
    reps1 = EqData.replace(replaceword0,replacedword1)
    reps2 = reps1.replace(replaceword1,replacedword2)
    reps3 = reps2.replace(replaceword2,replacedword3)
    reps4 = reps3.replace(replaceword3,replacedword4)
    reps5 = reps4.replace(replaceword4,replacedword5)
    reps6 = reps5.replace(replaceword5,replacedword6)
    reps7 = reps6.replace(replaceword6,replacedword7)
    reps8 = reps7.replace(replaceword7,replacedword0)
    reps9 = reps8.replace(replaceword8,replacedword0)
    reps10 = reps9.replace(replaceword9,replacedword0)
    reps11 = reps10.replace(replaceword10,replacedword0)
    reps12 = reps11.replace(replaceword11,replacedword0)
    reps13 = reps12.replace(replaceword12,replacedword0)
    reps14 = reps13.replace(replaceword13,replacedword0)
    reps15 = reps14.replace(replaceword14,replacedword0)
    reps16 = reps15.replace(replaceword15,replacedword0)
    reps17 = reps16.replace(replaceword16,replacedword0)
    reps18 = reps17.replace(replaceword17,replacedword0)
    reps19 = reps18.replace(replaceword18,replacedword0)
    reps20 = reps19.replace(replaceword19,replacedword0)
    reps21 = reps20.replace(replaceword20,replacedword0)
    reps22 = reps21.replace(replaceword21,replacedword0)
    reps23 = reps22.replace(replaceword22,replacedword8)
    reps24 = reps23.replace(replaceword23,replacedword9)
    reps25 = reps24.replace(replaceword24,replacedword10)
    reps26 = reps25.replace(replaceword25,replacedword11)
    reps27 = reps26.replace(replaceword26,replacedword12)
    reps28 = reps27.replace(replaceword27,replacedword13)
    reps29 = reps28.replace(replaceword28,replacedword14)
    reps30 = reps29.replace(replaceword29,replacedword15)
    reps31 = reps30.replace(replaceword30,replacedword16)
    
    return reps31

def main():
    Yahoo_URL = "https://typhoon.yahoo.co.jp/weather/earthquake/"
    user_agent = 'Mozilla/5.0 (Linux; Android 7.1.2; en-la) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 YJApp-ANDROID jp.co.yahoo.android.yjtop/13.91.1'
    response = urllib.request.urlopen(urllib.request.Request(Yahoo_URL, headers={'User-Agent': user_agent}))
    EqDetail = BeautifulSoup(response,features="html5lib").select("div.eqDetail")
    
    Detect_Shindo = str(EqDetail)
    if '<td>1</td>' in Detect_Shindo:
        print(Fore.WHITE + Back.BLACK)
    if '<td>2</td>' in Detect_Shindo:
        print(Fore.WHITE + Back.BLUE)
    if '<td>3</td>' in Detect_Shindo:
        print(Fore.BLACK + Back.GREEN)
    if '<td>4</td>' in Detect_Shindo:
        print(Fore.BLACK + Back.YELLOW)
    if '<td>5弱</td>' in Detect_Shindo:
        print(Fore.WHITE + Back.RED)
    if '<td>5強</td>' in Detect_Shindo:
        print(Fore.WHITE + Back.RED)
    if '<td>6弱</td>' in Detect_Shindo:
        print(Fore.WHITE + Back.RED)
    if '<td>6強</td>' in Detect_Shindo:
        print(Fore.WHITE + Back.RED)
    if '<td>7</td>' in Detect_Shindo:
        print(Fore.WHITE + Back.MAGENTA)
    
    for EqInfo in EqDetail:
        print(replace_word(EqInfo.getText()), end="")
    print("\n")
    print(Fore.RESET + Back.RESET)

if __name__ == '__main__':
    main()