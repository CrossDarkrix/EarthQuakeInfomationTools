# -*- coding: utf-8 -*-

"""
Colorful Getting Earthquake Infomation History from YahooJapan
Version: 1.5b
Author: DarkRix
"""

import bs4, colorama, urllib.request

def main():
    _u = "https://typhoon.yahoo.co.jp/weather/earthquake/"
    _ua = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5'
    _g = urllib.request.urlopen(urllib.request.Request(_u, headers={'User-Agent': _ua}), timeout=1000)
    _h = bs4.BeautifulSoup(_g, features="html5lib")
    _es = [_a.getText().split('  ')[0].split('\n')[0] for _a in _h.select("dd.subText")]
    _et = [_b.getText().split('  ')[0].split('\n')[0] for _b in _h.select("dt.title") if '震源地：' in _b.getText()]
    _esc = [_c.getText().split('    ')[0].split('\n')[0] + _c.getText().split('    ')[1].split('\n')[0].replace('M', ' (M').replace(_c.getText().split('    ')[1].split('\n')[0][-1], _c.getText().split('    ')[1].split('\n')[0][-1] + ')') for _c in _h.select('dd.eqScale')]
    _c = ''
    colorama.init()

    for _p in range(10):
        if _esc[_p].split(' ')[1].split(')')[0] == '1':
            _c = colorama.Fore.WHITE + colorama.Back.BLACK
        if _esc[_p].split(' ')[1].split(')')[0] == '2':
            _c = colorama.Fore.WHITE + colorama.Back.BLUE
        if _esc[_p].split(' ')[1].split(')')[0] == '3':
            _c = colorama.Fore.BLACK + colorama.Back.GREEN
        if _esc[_p].split(' ')[1].split(')')[0] == '4':
            _c = colorama.Fore.BLACK + colorama.Back.YELLOW
        if _esc[_p].split(' ')[1].split(')')[0] == '5弱':
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '5強':
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '6弱':
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '6強':
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '7':
            _c = colorama.Fore.WHITE + colorama.Back.MAGENTA
        if _esc[_p].split(' ')[1].split(')')[0] == '---':
            _esc[_p] = _esc[_p].split(')')[0].replace('---', '不明')
            _c = colorama.Fore.WHITE + colorama.Back.BLACK
        _esc[_p] = _esc[_p].split(' ')[0] + ' ' +_esc[_p].split(' ')[1].split(')')[0] + ' ' + ' '.join(_esc[_p].split(' ')[2:])
        print('{}{}\n{}\n{}{}'.format(_c, _es[_p], _et[_p], _esc[_p],(colorama.Fore.RESET + colorama.Back.RESET)))

if __name__ == '__main__':
    main()