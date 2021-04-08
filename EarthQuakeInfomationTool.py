# -*- coding: utf-8 -*-
"""
Getting Earthquake Infomation from YahooJapan
"""

from colorama import init as Starting
from colorama import Fore, Back
import urllib.request
from bs4 import BeautifulSoup
Starting() # Initing Colorcodes

def init():
	version = 2.5
	print("Version: {}".format(version))

def main():
	LINK = "https://typhoon.yahoo.co.jp/weather/earthquake/"  # YahooJapan Weather Link
	user_agent = 'Mozilla/5.0 (Linux; Android 7.1.2; en-la; AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 YJApp-ANDROID jp.co.yahoo.android.yjtop/13.91.1' # UserAgent(Android8.0 YahooApp)
	response = urllib.request.urlopen(urllib.request.Request(LINK, headers={'User-Agent': user_agent})) # Get HTML from YahooJapan
	URL = BeautifulSoup(response,features="html5lib")
	RAW = URL.select("div.eqDetail") # Selecting div Tag

	# Replace Words
	replaceword0 = '       '
	replaceword1 = '                    '
	replaceword2 = '         '
	replaceword3 = '  '
	replaceword4 = '\r'
	replaceword5 = '\n\n'
	replaceword6 = '\t\r'
	replaceword7 = '\n\n\n'
	replaceword8 = '\n   '
	replaceword9 = '。'
	replaceword11 = '発生時刻\n'
	replaceword12 = '震源地\n'
	replaceword13 = '最大震度\n'
	replaceword14 = 'マグニチュード\n'
	replaceword15 = '深さ\n'
	replaceword16 = '緯度/経度\n'
	replaceword17 = '情報\n'
	replaceword18 = '。\n'
	replaceword19 = '詳細を見る'
	replaceword20 = '・発生時刻: '
	replaceword21 = '・震源地: '
	replaceword22 = '・最大震度: '
	replaceword23 = '・地震の規模: M'
	replaceword24 = '・深さ: '
	replaceword25 = '・緯度/経度: '
	replaceword26 = '・津波情報: '
	replaceword27 = '\r'
	replaceword28 = '\n'
	replaceword29 = '。\n\n'
	replaceword30 = ''
	replaceword31 = '>>津波情報を見る'
	replaceword32 = '\n \n \n'
	replaceword33 = '\n\n '
	replaceword34 = ':\n'
	replaceword35 = ': '
	replaceword36 = '\n ・'
	replaceword37 = '\n\n・'
	replaceword38 = ' ・'
	replaceword39 = '\n\n・'
	replaceword40 = ':北'
	replaceword41 = ': 北'
	replaceword42 = 'M '
	replaceword43 = 'M'
	replaceword44 = '  '
	replaceword45 = ' '
	replaceword46 = ' \n'
	replaceword47 = '\n'
	
	source = str(RAW)
	if '<td>1</td>' in source:
		print(Fore.WHITE + Back.BLACK)
	if '<td>2</td>' in source:
		print(Fore.WHITE + Back.BLUE)
	if '<td>3</td>' in source:
		print(Fore.BLACK + Back.GREEN)
	if '<td>4</td>' in source:
		print(Fore.BLACK + Back.YELLOW)
	if '<td>5弱</td>' in source:
		print(Fore.WHITE + Back.RED)
	if '<td>5強</td>' in source:
		print(Fore.WHITE + Back.RED)
	if '<td>6弱</td>' in source:
		print(Fore.WHITE + Back.RED)
	if '<td>6強</td>' in source:
		print(Fore.WHITE + Back.RED)
	if '<td>7</td>' in source:
		print(Fore.WHITE + Back.MAGENTA)
	
	for EEW in RAW:
		print(EEW.getText().replace(replaceword11,replaceword20).replace(replaceword12,replaceword21).replace(replaceword13,replaceword22).replace(replaceword14,replaceword23).replace(replaceword15,replaceword24).replace(replaceword16,replaceword25).replace(replaceword17,replaceword26).replace(replaceword18,replaceword30).replace(replaceword1,replaceword30).replace(replaceword19,replaceword27).replace(replaceword2,replaceword30).replace(replaceword0,replaceword30).replace(replaceword4,replaceword30).replace(replaceword5,replaceword28).replace(replaceword6,replaceword30).replace(replaceword7,replaceword30).replace(replaceword8,replaceword30).replace(replaceword3,replaceword30).replace(replaceword9,replaceword29).replace(replaceword31,replaceword30).replace(replaceword32, replaceword30).replace(replaceword33, replaceword30).replace(replaceword34, replaceword35).replace(replaceword36, replaceword37).replace(replaceword38, replaceword39).replace(replaceword40, replaceword41).replace(replaceword42, replaceword43).replace(replaceword44, replaceword45).replace(replaceword46, replaceword47), end="")
	print("\n")
	print(Fore.RESET + Back.RESET)

if __name__ == '__main__':
	main()
