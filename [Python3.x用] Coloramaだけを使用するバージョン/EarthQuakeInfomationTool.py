import colorama
import re
import urllib.request

class Earthquake:
    def __init__(self):
        self.URL = "https://typhoon.yahoo.co.jp/weather/earthquake/"
        self.UA = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5' # Android端末のYahooアプリに偽装
        html = self.fetch_html()
        block = self.extract_block(html)
        text = self.clean_text(block)
        self.data = self.extract_data(text)
        self.colored()

    def fetch_html(self):
        req = urllib.request.Request(self.URL, headers={"User-Agent": self.UA})
        with urllib.request.urlopen(req) as res:
            html = res.read().decode("utf-8", errors="ignore")
        return html

    def extract_block(self, html: str):
        m = re.search(r'<div class="eqDetail[^"]*">(.*?)</div>', html, re.DOTALL)
        return m.group(1) if m else None

    def clean_text(self, html_fragment: str):
        text = re.sub(r'<.*?>', '', html_fragment)
        text = re.sub(r'[ \t]+', ' ', text)
        text = re.sub(r'\n+', '\n', text)

        return text.strip()

    def extract_data(self, text):
        pairs = re.findall(r'(\S+?)\s*\n\s*(.+)', text)
        data_map = {}

        for k, v in pairs:
            k = k.strip()
            v = v.strip()

            if "発生時刻" in k:
                data_map["time"] = v
            elif "震源地" in k:
                data_map["place"] = v
            elif "最大震度" in k:
                data_map["max_intensity"] = v
            elif "マグニチュード" in k:
                m = re.search(r'(\d+\.\d+)', v)
                data_map["magnitude"] = m.group(1) if m else None
            elif "深さ" in k:
                data_map["depth"] = v
            elif "緯度" in k:
                data_map["latlon"] = v
            if "津波" in k:
                data_map["tsunami"] = v
            else:
                data_map["tsunami"] = "この地震による津波の心配はありません"
        return data_map

    def validate(self, data: dict):
        required = ["time", "place", "magnitude"]

        return all(data.get(k) for k in required)

    def format_output(self, data: dict):
        return "\n\n".join([
            f"・発生時刻: {data['time']}",
            f"・震源地: {data['place']}",
            f"・最大震度: {data['max_intensity']}",
            f"・地震の規模: M{data['magnitude']}",
            f"・深さ: {data['depth']}",
            f"・緯度/経度: {data['latlon']}",
            f"・津波情報: {data['tsunami']}",
        ])

    def color_formatted_output(self, data: dict):
        def _text(data):
            return "\n\n".join([
            f"・発生時刻: {data['time']}",
            f"・震源地: {data['place']}",
            f"・最大震度: {data['max_intensity']}",
            f"・地震の規模: M{data['magnitude']}",
            f"・深さ: {data['depth']}",
            f"・緯度/経度: {data['latlon']}",
            f"・津波情報: {data['tsunami']}",
        ])
        colorama.init()
        if '1' == data['max_intensity']:
            return f'{colorama.Fore.WHITE + colorama.Back.BLACK}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '2' == data['max_intensity']:
            return f'{colorama.Fore.WHITE + colorama.Back.BLUE}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '3' == data['max_intensity']:
            return f'{colorama.Fore.BLACK + colorama.Back.GREEN}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '4' == data['max_intensity']:
            return f'{colorama.Fore.BLACK + colorama.Back.YELLOW}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '5弱' == data['max_intensity']:
            return f'{colorama.Fore.WHITE + colorama.Back.RED}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '5強' == data['max_intensity']:
            return f'{colorama.Fore.WHITE + colorama.Back.RED}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '6弱' == data['max_intensity']:
            return f'{colorama.Fore.WHITE + colorama.Back.RED}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '6強' == data['max_intensity']:
            return f'{colorama.Fore.WHITE + colorama.Back.RED}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'
        if '7' == data['max_intensity']:
            return f'{colorama.Fore.WHITE + colorama.Back.MAGENTA}{_text(data)}{colorama.Fore.RESET + colorama.Back.RESET}'

    def normal(self):
        print(self.format_output(self.data))

    def colored(self):
        print(self.color_formatted_output(self.data))

def main():
    Earthquake()


if __name__ == "__main__":
    main()