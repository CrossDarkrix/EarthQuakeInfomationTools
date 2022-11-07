#!python3
# -*- coding: utf-8 -*-

"""
Colorful Getting Earthquake Infomation History from YahooJapan
Version: 1.5-pythonista3
Author: DarkRix
"""

import bs4, console, urllib.request

def main():
    _u = "https://typhoon.yahoo.co.jp/weather/earthquake/"
    _ua = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5'
    _g = urllib.request.urlopen(urllib.request.Request(_u, headers={'User-Agent': _ua}), timeout=1000)
    _h = bs4.BeautifulSoup(_g, features="html5lib")
    _es = [_a.getText().split('  ')[0].split('\n')[0] for _a in _h.select("dd.subText")]
    _et = [_b.getText().split('  ')[0].split('\n')[0] for _b in _h.select("dt.title") if '震源地：' in _b.getText()]
    _esc = [_c.getText().split('    ')[0].split('\n')[0] + _c.getText().split('    ')[1].split('\n')[0].replace('M', ' (M').replace(_c.getText().split('    ')[1].split('\n')[0][-1], _c.getText().split('    ')[1].split('\n')[0][-1] + ')') for _c in _h.select('dd.eqScale')]

    console.clear()

    for _p in range(10):
        if _esc[_p].split(' ')[1].split(')')[0] == '1':
            console.set_color(255, 255, 255) # White
        if _esc[_p].split(' ')[1].split(')')[0] == '2':
            console.set_color(0, 10, 255) # Blue
        if _esc[_p].split(' ')[1].split(')')[0] == '3':
            console.set_color(0, 102, 0) # Green
        if _esc[_p].split(' ')[1].split(')')[0] == '4':
            console.set_color(255, 10, 0) # Yellow
        if _esc[_p].split(' ')[1].split(')')[0] == '5弱':
            console.set_color(255, 1, 0) # Orange
        if _esc[_p].split(' ')[1].split(')')[0] == '5強':
            console.set_color(100, 80, 0) # Light Orange
        if _esc[_p].split(' ')[1].split(')')[0] == '6弱':
            console.set_color(255, 1 , 255) # Pink
        if _esc[_p].split(' ')[1].split(')')[0] == '6強':
            console.set_color(255, 0, 0) # Red
        if _esc[_p].split(' ')[1].split(')')[0] == '7':
            console.set_color(255, 0, 255) # Magenta
        if _esc[_p].split(' ')[1].split(')')[0] == '---':
            _esc[_p] = _esc[_p].split(')')[0].replace('---', '不明')
            console.set_color(255, 255, 255) # White
        _esc[_p] = _esc[_p].split(' ')[0] + ' ' +_esc[_p].split(' ')[1].split(')')[0] + ' ' + ' '.join(_esc[_p].split(' ')[2:])
        print('{}\n{}\n{}'.format(_es[_p], _et[_p], _esc[_p]))
        console.set_color()

if __name__ == '__main__':
	main()