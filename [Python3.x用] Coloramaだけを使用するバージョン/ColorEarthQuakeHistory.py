# -*- coding: utf-8 -*-

"""
Colorful Getting Earthquake Infomation History from YahooJapan
Version: 1.2b
Author: DarkRix
"""

import colorama, re, urllib.request
    
def _tg(source, _tag1, _tag2, _tag3):
    _hd = source.read().decode() # htmlの読み込み
    _ht1 = _tag1.split('.')[0] # 読み込むタグの選択
    _tn1 = '.'.join(_tag1.split('.')[1:]) # 読み込むクラスの選択
    _ht2 = _tag2.split('.')[0] # 読み込むタグの選択
    _tn2 = '.'.join(_tag2.split('.')[1:]) # 読み込むクラスの選択
    _ht3 = _tag3.split('.')[0] # 読み込むタグの選択
    _tn3 = '.'.join(_tag3.split('.')[1:]) # 読み込むクラスの選択
    _tn1 = re.findall('<{} class="{}">(.+)'.format(_ht1, _tn1, _ht1), _hd) # 読み込んだタグとそのクラスを検索しリストにする
    _tn2 = [_t for _t in re.findall('<{} class="{}">(.+)</{}>'.format(_ht2, _tn2, _ht2), _hd) if '震源地：' in _t] # 読み込んだタグとそのクラスを検索し条件に合った場合にのみリストにする
    _ta = ''.join(_hd.split('<{} class="{}">'.format(_ht3, _tn3))[1:]).split('</div>')[0] # 読み込んだタグとそのクラスで分割し、さらにdivの終わりのタグで分割
    _tb = [_y.replace('<em>','').replace('</em>','') for _y in re.findall('-->(.+)<', _ta)] # 条件で検索し、emタグ内の文字列を抽出
    _tt = [re.sub('<em (.+)>', '', _y) for _y in _tb] # 条件で検索し、emタグを整形
    _tc = '#'.join(_tt).replace('#最', '),最') # 「最大震度」の「最」の先頭に＃をつけてから「),最」に整形
    _te = ''.join(_tc.split('#')).replace('M', ' (M').split(',') # ＃で分割し、Mを「 (M」にして「,」で分割
    _tn3 = [_yt.replace(_yt[-1], _yt[-1] + ')').replace(').','.') if not ')' in _yt else _yt for _yt in _te] # 後ろに「)」が付いていない文字列に「)」を付ける
    return _tn1, _tn2, _tn3

def main():
    _u = "https://typhoon.yahoo.co.jp/weather/earthquake/" # YahooJapanの地震情報
    _ua = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5'  # Android端末のYahooアプリに偽装
    _g = urllib.request.urlopen(urllib.request.Request(_u, headers={'User-Agent': _ua}), timeout=1000) # 定義したユーザーエージェントに従いURLへアクセス(念の為１０００秒待機)
    _ht = _tg(_g, 'dd.subText', 'dt.title', 'dd.eqScale') # htmlの受け渡しとddタグの「subText」、dtタグの「title」、ddタグの「eqScale」を選択
    _es = _ht[0] # ddタグのクラス名「subText」の中身をリスト形式で出力
    _et = _ht[1] # dtタグのクラス名「title」の中身をリスト形式で出力
    _esc = _ht[2] # ddタグのクラス名「eqScale」の中身をリスト形式で出力

    colorama.init() # カラーコードの初期化

    for _p in range(10):
        if _esc[_p].split(' ')[1].split(')')[0] == '1': # 震度１なら黒く表示
            _c = colorama.Fore.WHITE + colorama.Back.BLACK
        if _esc[_p].split(' ')[1].split(')')[0] == '2': # 震度２なら青く表示
            _c = colorama.Fore.WHITE + colorama.Back.BLUE
        if _esc[_p].split(' ')[1].split(')')[0] == '3': # 震度３なら緑に表示
            _c = colorama.Fore.BLACK + colorama.Back.GREEN
        if _esc[_p].split(' ')[1].split(')')[0] == '4': # 震度４なら黄色く表示
            _c = colorama.Fore.BLACK + colorama.Back.YELLOW
        if _esc[_p].split(' ')[1].split(')')[0] == '5弱': # 震度５弱なら赤く表示
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '5強': # 震度５強なら赤く表示
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '6弱': # 震度６弱なら赤く表示
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '6強': # 震度６強なら赤く表示
            _c = colorama.Fore.WHITE + colorama.Back.RED
        if _esc[_p].split(' ')[1].split(')')[0] == '7': # 震度７なら紫色に表示
            _c = colorama.Fore.WHITE + colorama.Back.MAGENTA
        if _esc[_p].split(' ')[1].split(')')[0] == '---': # 震度不明なら黒く表示
            _esc[_p] = _esc[_p].replace('---', '不明')
            _c = colorama.Fore.WHITE + colorama.Back.BLACK
        _esc[_p] = _esc[_p].split(' ')[0] + ' ' +_esc[_p].split(' ')[1].split(')')[0] + ' ' + ' '.join(_esc[_p].split(' ')[2:])
        print('{}{}\n{}\n{}{}'.format(_c, _es[_p], _et[_p], _esc[_p],(colorama.Fore.RESET + colorama.Back.RESET))) # 発生時刻、震源地、最大震度を表示しつつ、色情報を元の色に戻す

if __name__ == '__main__':
    main()
