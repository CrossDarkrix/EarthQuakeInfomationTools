# -*- coding: utf-8 -*-

from colorama import init as Starting
from colorama import Fore, Back
import urllib.request
from bs4 import BeautifulSoup
Starting() # Initing Colorcode

EQColor = ''

def main():
	YahooLINK = "https://typhoon.yahoo.co.jp/weather/earthquake/"
	user_agent = 'Mozilla/5.0 (Linux; Android 7.1.2; en-la; AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/52.0.2743.100 Mobile Safari/537.36 YJApp-ANDROID jp.co.yahoo.android.yjtop/13.91.1' 
	GetHTML = urllib.request.urlopen(urllib.request.Request(YahooLINK, headers={'User-Agent': user_agent}), timeout=1000)
	FULLHTML = BeautifulSoup(GetHTML,features="html5lib") 
	eqsubtext = FULLHTML.select("dd.subText")
	eqtitle = FULLHTML.select("dt.title")
	eqscale = FULLHTML.select('dd.eqScale')
	
	replacewd20 = '['
	replacewd21 = ']'
	replacewd22 = '地震から身を守る'
	replacewd23 = '災害用伝言ダイヤル（171）'
	replacewd24 = 'SoftBank'
	replacewd25 = 'docomo'
	replacewd26 = 'au'
	replacewd27 = 'ワイモバイル'
	replacewd28 = ', '
	replacewd29 = '<em>'
	replacewd30 = '</em>'
	replacewd31 = '<!--\\\\n'
	replacewd32 = '-->'
	replacewd33 = '\\\\n '
	replacewd34 = '       '
	replacewd35 = 'M'
	replacewd36 = '(M'
	replacewd37 = '<!--\n'
	replacewd38 = '       \n '
	replacewd39 = '\n    '
	replacewd40 = '                '
	replacewd41 = '分\n                  '
	replacewd42 = '      '
	replacewd43 = '  '
	replacewd44 = '---'
	replacewd45 = '不明'
	replacewd46 = ' <em class="red">'
	replacewd47 = ' ('
	replacewd48 = '('
	
	EQSubText = str(eqsubtext).replace(replacewd20,'').replace(replacewd21,'').replace('</dd>','').replace(', ','').replace(replacewd41,'分').split('<dd class="subText">')
	del EQSubText[0]

	EQTilte = str(eqtitle).replace(replacewd20,'').replace(replacewd21,'').replace('</dt>','').replace(replacewd22,'').replace(replacewd23,'').replace(replacewd24,'').replace(replacewd25,'').replace(replacewd26,'').replace(replacewd27,'').replace(replacewd28,'').split('<dt class="title">')
	for i in range(6):
		del EQTilte[-1]
	del EQTilte[0]
	
	EQScale = str(eqscale).replace(replacewd20,'').replace(replacewd21,'').replace(replacewd28,'').replace(replacewd29,'').replace(replacewd30,'').replace(replacewd31,'').replace(replacewd32,'').replace(replacewd33,'').replace(replacewd34,'').replace(replacewd35,replacewd36).replace('</dd>','').replace(replacewd37,'').replace(replacewd38,'').replace(replacewd39,'').replace(replacewd40,'').replace(replacewd42,'').replace(replacewd43,' ').replace(replacewd46,'').replace(replacewd44,replacewd45).replace(replacewd47,replacewd48).split('<dd class="eqScale">')
	del EQScale[0]
	
	for r in range(10):
		if '最大震度： 1' in EQScale[r]:
			EQColor = Fore.WHITE + Back.BLACK
		
		if '最大震度： 2' in EQScale[r]:
			EQColor = Fore.WHITE + Back.BLUE
		
		if '最大震度： 3' in EQScale[r]:
			EQColor = Fore.BLACK + Back.GREEN
			
		if '最大震度： 4' in EQScale[r]:
			EQColor = Fore.BLACK + Back.YELLOW
		
		if '最大震度： 5弱' in EQScale[r]:
			EQColor = Fore.WHITE + Back.RED
		
		if '最大震度： 5強' in EQScale[r]:
			EQColor = Fore.WHITE + Back.RED
		
		if '最大震度： 6弱' in EQScale[r]:
			EQColor = Fore.WHITE + Back.RED
		
		if '最大震度： 6強' in EQScale[r]:
			EQColor = Fore.WHITE + Back.RED
		
		if '最大震度： 7' in EQScale[r]:
			EQColor = Fore.WHITE + Back.MAGENTA
		
		if '最大震度： 不明' in EQScale[r]:
			EQColor = Fore.WHITE + Back.BLACK

		print(EQColor + EQSubText[r])
		print(EQColor + EQTilte[r])
		print(EQColor + EQScale[r] + ')')
	print(Fore.RESET + Back.RESET)

if __name__ == '__main__':
	main()
