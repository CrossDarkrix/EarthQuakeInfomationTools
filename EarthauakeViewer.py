# -*- coding: utf-8 -*-


from __future__ import annotations

import traceback
from dataclasses import dataclass
from typing import Dict, List, Optional
import re
import urllib.request
from PySide6.QtCore import QObject, QThread, Signal, Slot, Qt, QTimer
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTabWidget,
    QPlainTextEdit,
    QTableWidget,
    QTableWidgetItem,
    QHeaderView,
    QMessageBox,
    QStatusBar,
)


class Earthquake: # 直近の地震情報単一を出力
    def __init__(self):
        self.URL = "https://typhoon.yahoo.co.jp/weather/earthquake/"
        self.UA = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5' # Android端末のYahooアプリに偽装
        html = self.fetch_html()
        block = self.extract_block(html)
        text = self.clean_text(block)
        self.data = self.extract_data(text)

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

    def fetch(self):
        return self.data

class Earthquake_History: # 過去の情報を一覧で出力
    def __init__(self, max_items: int = 10):
        self.max_items = max_items
        self.URL = "https://typhoon.yahoo.co.jp/weather/earthquake/"
        self.UA = 'Mozilla/5.0 (Linux; U; Android 8.0; en-la; Nexus Build/JPG991) AppleWebKit/511.2 (KHTML, like Gecko) Version/5.0 Mobile/11S444 YJApp-ANDROID jp.co.yahoo.android.yjtop/4.01.1.5'  # Android端末のYahooアプリに偽装

    def remove_comments(self, html):
        return re.sub(r'<!--.*?-->', '', html, flags=re.DOTALL)

    def fetch_html(self):
        req = urllib.request.Request(self.URL, headers={"User-Agent": self.UA})
        with urllib.request.urlopen(req) as res:
            return re.findall(
            r'<li>.*?<dd class="subText">(.*?)</dd>.*?'
            r'<dt class="title">(.*?)</dt>.*?'
            r'<dd class="eqScale">(.*?)</dd>',
            self.remove_comments(res.read().decode("utf-8", errors="ignore")),
            re.DOTALL)

    def parse_entry(self, block):
        clean = lambda x: re.sub(r'<.*?>', '', x).strip()
        time = re.search(r'\d{4}年\d+月\d+日.*\d+時\d+分', clean(block))
        _pl = re.search('震源地：.+\n', clean(block))
        place = _pl.group(0).split('震源地： ')[-1].strip() if _pl else None

        _ins = re.search(r'最大震度[:：]?\s*(\S+)', clean(block))
        intensity = _ins.group(1).split('M')[0] if _ins else None

        _mag = re.search(r'M(\d+\.\d+)', clean(block))
        magnitude = _mag.group(1).split('M')[-1] if _mag else None

        return {
            "time": time.group(0) if time else None,
            "place": place,
            "intensity": intensity,
            "magnitude": magnitude
        }


    def fetch(self):
        count = 0
        out = []
        for block in self.fetch_html():
            data = self.parse_entry('\n'.join(block))
            if data:
                out.append(data)
                count += 1
                if count >= self.max_items:
                    break
        return out


@dataclass
class LatestResult:
    ok: bool
    data: Optional[Dict[str, Optional[str]]] = None
    error: Optional[str] = None


@dataclass
class HistoryResult:
    ok: bool
    items: Optional[List[Dict[str, Optional[str]]]] = None
    error: Optional[str] = None


class FetchWorker(QObject):
    latest_done = Signal(object)   # LatestResult
    history_done = Signal(object)  # HistoryResult

    def __init__(self, max_items: int = 10):
        super().__init__()
        self.max_items = max_items

    @Slot()
    def fetch_latest(self):
        try:
            eq = Earthquake()
            data = eq.fetch()
            self.latest_done.emit(LatestResult(ok=True, data=data))
        except Exception:
            self.latest_done.emit(
                LatestResult(ok=False, error=traceback.format_exc())
            )

    @Slot()
    def fetch_history(self):
        try:
            hist = Earthquake_History(max_items=self.max_items)
            items = hist.fetch()
            self.history_done.emit(HistoryResult(ok=True, items=items))
        except Exception:
            self.history_done.emit(
                HistoryResult(ok=False, error=traceback.format_exc())
            )


class EarthquakeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("eqinfoicon.ico"))
        self.setWindowTitle("Earthquake Viewer v1.0")

        # --- UI ---
        self.tabs = QTabWidget()
        self.setCentralWidget(self.tabs)

        self.latest_tab = QWidget()
        self.history_tab = QWidget()
        self.tabs.addTab(self.latest_tab, "最新(詳細)")
        self.tabs.addTab(self.history_tab, "履歴(一覧)")

        self._build_latest_tab()
        self._build_history_tab()

        # status
        self.setStatusBar(QStatusBar())

        # actions
        refresh_action = QAction("更新", self)
        refresh_action.setShortcut("F5")
        refresh_action.triggered.connect(self.refresh_all)
        self.menuBar().addAction(refresh_action)

        # --- worker thread ---
        self.thread = QThread(self)
        self.worker = FetchWorker(max_items=20)
        self.worker.moveToThread(self.thread)
        self.thread.start()

        self.worker.latest_done.connect(self._on_latest_done)
        self.worker.history_done.connect(self._on_history_done)

        # auto refresh (5分ごと)
        self.timer = QTimer(self)
        self.timer.setInterval(5 * 60 * 1000)
        self.timer.timeout.connect(self.refresh_all)
        self.timer.start()

        self.refresh_all()

    # --- build tabs ---
    def _build_latest_tab(self):
        lay = QVBoxLayout()
        self.latest_tab.setLayout(lay)

        btn_row = QHBoxLayout()
        self.btn_refresh_latest = QPushButton("最新を更新")
        self.btn_refresh_latest.clicked.connect(self.refresh_latest)
        btn_row.addWidget(self.btn_refresh_latest)
        btn_row.addStretch(1)
        lay.addLayout(btn_row)

        self.latest_summary = QLabel("未取得")
        self.latest_summary.setTextInteractionFlags(Qt.TextSelectableByMouse)
        lay.addWidget(self.latest_summary)

        self.latest_text = QPlainTextEdit()
        self.latest_text.setReadOnly(True)
        lay.addWidget(self.latest_text, 1)

    def _build_history_tab(self):
        lay = QVBoxLayout()
        self.history_tab.setLayout(lay)

        btn_row = QHBoxLayout()
        self.btn_refresh_history = QPushButton("履歴を更新")
        self.btn_refresh_history.clicked.connect(self.refresh_history)
        btn_row.addWidget(self.btn_refresh_history)
        btn_row.addStretch(1)
        lay.addLayout(btn_row)

        self.table = QTableWidget(0, 4)
        self.table.setHorizontalHeaderLabels(["発生時刻", "震源地", "最大震度", "M"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.table.itemSelectionChanged.connect(self._on_history_selected)
        lay.addWidget(self.table, 1)

        self.history_detail = QPlainTextEdit()
        self.history_detail.setReadOnly(True)
        lay.addWidget(self.history_detail, 1)

    # --- refresh ---
    @Slot()
    def refresh_all(self):
        self.refresh_latest()
        self.refresh_history()

    @Slot()
    def refresh_latest(self):
        self.statusBar().showMessage("最新情報を取得中...")
        self.btn_refresh_latest.setEnabled(False)
        QTimer.singleShot(0, self.worker.fetch_latest)  # thread側スロットを呼ぶ

    @Slot()
    def refresh_history(self):
        self.statusBar().showMessage("履歴を取得中...")
        self.btn_refresh_history.setEnabled(False)
        QTimer.singleShot(0, self.worker.fetch_history)

    # --- results ---
    @Slot(object)
    def _on_latest_done(self, res: LatestResult):
        self.btn_refresh_latest.setEnabled(True)
        if not res.ok:
            self.statusBar().showMessage("最新情報の取得に失敗")
            self._show_error("最新情報の取得に失敗しました", res.error)
            return

        data = res.data or {}
        # 画面表示
        time = data.get("time") or "(不明)"
        place = data.get("place") or "(不明)"
        intensity = data.get("max_intensity") or "(不明)"
        mag = data.get("magnitude") or "(不明)"
        self.latest_summary.setText(f"発生: {time} / 震源地: {place} / 最大震度: {intensity} / M{mag}")

        # 整形表示は Earthquake.format_output を利用
        eq = Earthquake()
        self.latest_text.setPlainText(eq.format_output(data))
        self.statusBar().showMessage("最新情報を更新しました")

    @Slot(object)
    def _on_history_done(self, res: HistoryResult):
        self.btn_refresh_history.setEnabled(True)
        if not res.ok:
            self.statusBar().showMessage("履歴の取得に失敗")
            self._show_error("履歴の取得に失敗しました", res.error)
            return

        items = res.items or []
        self.table.setRowCount(len(items))
        for r, d in enumerate(items):
            self.table.setItem(r, 0, QTableWidgetItem(d.get("time") or ""))
            self.table.setItem(r, 1, QTableWidgetItem(d.get("place") or ""))
            self.table.setItem(r, 2, QTableWidgetItem(d.get("intensity") or ""))
            self.table.setItem(r, 3, QTableWidgetItem(d.get("magnitude") or ""))
        self.statusBar().showMessage(f"履歴を更新しました ({len(items)}件)")

        if items:
            self.table.selectRow(0)

    def _on_history_selected(self):
        rows = self.table.selectionModel().selectedRows()
        if not rows:
            return
        r = rows[0].row()
        time = self.table.item(r, 0).text() if self.table.item(r, 0) else ""
        place = self.table.item(r, 1).text() if self.table.item(r, 1) else ""
        intensity = self.table.item(r, 2).text() if self.table.item(r, 2) else ""
        mag = self.table.item(r, 3).text() if self.table.item(r, 3) else ""
        self.history_detail.setPlainText("".join(
                [
                    f"発生時刻: {time}\n",
                    f"震源地: {place}\n",
                    f"最大震度: {intensity}\n",
                    f"マグニチュード: M{mag}\n",
                ]
            )
        )

    def _show_error(self, title: str, detail: Optional[str]):
        mb = QMessageBox(self)
        mb.setIcon(QMessageBox.Critical)
        mb.setWindowTitle(title)
        mb.setText(title)
        if detail:
            mb.setDetailedText(detail)
        mb.exec()

    def closeEvent(self, event):
        try:
            self.timer.stop()
            self.thread.quit()
            self.thread.wait(1000)
        finally:
            super().closeEvent(event)


def main():
    app = QApplication([])
    w = EarthquakeWindow()
    w.resize(900, 600)
    w.show()
    app.exec()


if __name__ == "__main__":
    main()
