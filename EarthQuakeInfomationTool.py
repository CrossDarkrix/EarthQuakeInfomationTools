# -*- coding: utf-8 -*-
"""
Colorful Getting Earthquake Infomation from YahooJapan
Version: 3.5b
Author: DarkRix
"""

import bs4, colorama, re, urllib.request

def _r(d):
    _r0 = '\n発生時刻'
    _r1 = '震源地\n'
    _r2 = '最大震度\n'
    _r3 = 'マグニチュード\n'
    _r4 = '深さ\n'
    _r5 = '緯度/経度\n'
    _r6 = '情報\n'
    _rd0 = '・発生時刻: '
    _rd1 = '\n・震源地: '
    _rd2 = '\n・最大震度: '
    _rd3 = '・地震の規模: M'
    _rd4 = '・深さ: '
    _rd5 = '・緯度/経度: '
    _rd6 = '・津波情報: '
    _sw = '。'
    _eq = re.sub('([ ])', '', d)
    _eq1 = re.sub('(\n\n)','', _eq)
    _eq2 = _eq1.replace(_r0, _rd0)
    _eq3 = _eq2.replace(_r1, _rd1)
    _eq4 = _eq3.replace(_r2, _rd2)
    _eq5 = _eq4.replace(_r3, _rd3)
    _eq6 = _eq5.replace(_r4, _rd4)
    _eq7 = _eq6.replace(_r5, _rd5)
    _eq8 = _eq7.replace(_r6, _rd6).split(_sw)[0]

    return _eq8.split('\n')

def main():
    _u = "https://typhoon.yahoo.co.jp/weather/earthquake/"
    _ua = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5'
    _d = urllib.request.urlopen(urllib.request.Request(_u, headers={'User-Agent': _ua}))
    _t = bs4.BeautifulSoup(_d, features="html5lib").select("div.eqDetail")[0]
    colorama.init()

    _dq = str(_t)
    if '<td>1</td>' in _dq:
        print(colorama.Fore.WHITE + colorama.Back.BLACK)
    if '<td>2</td>' in _dq:
        print(colorama.Fore.WHITE + colorama.Back.BLUE)
    if '<td>3</td>' in _dq:
        print(colorama.Fore.BLACK + colorama.Back.GREEN)
    if '<td>4</td>' in _dq:
        print(colorama.Fore.BLACK + colorama.Back.YELLOW)
    if '<td>5弱</td>' in _dq:
        print(colorama.Fore.WHITE + colorama.Back.RED)
    if '<td>5強</td>' in _dq:
        print(colorama.Fore.WHITE + colorama.Back.RED)
    if '<td>6弱</td>' in _dq:
        print(colorama.Fore.WHITE + colorama.Back.RED)
    if '<td>6強</td>' in _dq:
        print(colorama.Fore.WHITE + colorama.Back.RED)
    if '<td>7</td>' in _dq:
        print(colorama.Fore.WHITE + colorama.Back.MAGENTA)

    print('\n\n'.join(_r(_t.getText())))
    print(colorama.Fore.RESET + colorama.Back.RESET)

if __name__ == '__main__':
    main()
