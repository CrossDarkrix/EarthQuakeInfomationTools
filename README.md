# Earthquake Infomation Tools
*Yahoo JAPANの地震情報を色分けして見やすくしてみました。*

## 使い方
`python3 EarthQuakeInfomationTool.py`

`python3 ColorEarthQuakeHistory.py`

*「EarthQuakeInfomationTool」は地震情報だけで、*

*「ColorEarthQuakeHistory」は地震情報と過去の地震情報を色分けをしています*

## 開発秘話
*当初は軽い気持ちで「地震情報を文字列化できたらいいや」と作り始めました。*

*しかし、載せたい機能を追加していくうちに開発に2年近く費やしてしまいました。*

*そして、作り始めて改めて思いました「ああ、HTMLとCSS読めて良かった」と。*

*それくらいhtmlから抽出するのが地味に面倒でした。*

*なのでreplace多様かつゴリ押しなところが目立つコードとなっています。*

*(うまい人だともっと綺麗に書きそう…)*

*個人的に苦労したのはUserAgentでした。*

*下手にPythonっぽくアクセスするとHTMLが修正された時に修正が面倒です。*

*(実際にPythonからアクセスするとHTMLを変えてくるサイトも存在しました)*

*なので、無難にAndroid版YahooJAPANアプリに偽装しています。*

*(※UserAgentの偽装自体は問題ないようです。)*
