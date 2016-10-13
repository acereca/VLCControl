from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from vlcHTTPWrapper import *
from twitch import *

import os, json, time

class vlcc(QWidget):

    def __init__(self, parent=None):
        super(vlcc, self).__init__(parent)

        # SETUP
        f = open(os.path.join(os.path.dirname(__file__), "settings.json"), "r")
        self.j_settings = json.load(f)

        self.color = self.j_settings['appearance']['color']
        self.http_wrapper = vlcHTTPWrapper(self.j_settings['security']['user'], self.j_settings['security']['password'],
                                      str(self.j_settings['security']['port']))

        self.pos_v = ".//volume"
        self.pos_p = ".//*[@name='now_playing']"
        self.pos_t = ".//*[@name='filename']"
        self.pos_a = ".//*[@name='artist']"
        self.stat_dict = {self.pos_v: 'vol%', self.pos_a: 'artist', self.pos_t: 'title', self.pos_p: 'playing'}

        p_bck = QIcon("res/previous.png")
        p_fwd = QIcon("res/next.png")
        p_ply = QIcon("res/play.png")

        f_text = QFrame(self)
        f_text.setGeometry(0, 0, 150, 150)
        f_text.setStyleSheet('background-color: {};'.format(self.color))

        def setup_b_ctrlrow(btn, btn_i, i):
            btn.setIconSize(QSize(50, 50))
            btn.setIcon(btn_i)
            btn.setFlat(True)
            btn.move(50 + 45*i - btn.width()/2, 20)

        self.b_bck = QPushButton(f_text)
        setup_b_ctrlrow(self.b_bck, p_bck, 0)

        self.b_fwd = QPushButton(f_text)
        setup_b_ctrlrow(self.b_fwd, p_fwd, 2)

        self.b_ply = QPushButton(f_text)
        setup_b_ctrlrow(self.b_ply, p_ply, 1)

        font = QFont()
        font.setStyleStrategy(QFont.PreferAntialias)
        font.setPointSize(25)
        font.setFamily('consolas')

        def setup_b_volrow(btn, i, cmd):
            btn.setFont(font)
            btn.setFlat(True)
            btn.setFixedWidth(QFontMetrics(font).width(btn.text())+10)
            btn.move(20 + 55*i - btn.width()/2, 90)
            btn.setStyleSheet('color: white;')
            btn.clicked.connect(lambda: self.on_click(cmd))

        self.b_vd = QPushButton("-", f_text)
        setup_b_volrow(self.b_vd, 0, 'voldown')

        self.b_vu = QPushButton("+", f_text)
        setup_b_volrow(self.b_vu, 2, 'volup')

        self.b_vm = QPushButton("100%", f_text)
        setup_b_volrow(self.b_vm, 1, 'mute')
        #self.b_vm.setCheckable(True)

        self.l_t = QLabel('title', self)
        self.l_t.move(160, 5)
        self.l_t.setStyleSheet('font-size: 70px;')

        self.l_a = QLabel('artist', self)
        self.l_a.move(160, 90)
        self.l_a.setStyleSheet('font-size: 40px;')

        # self.setLayout(mainLayout)
        self.setWindowTitle("Hello Qt")
        self.setGeometry(self.j_settings['appearance']['pos']['x'], self.j_settings['appearance']['pos']['y'], 600, 150)
        self.setMaximumWidth(960)
        self.setAutoFillBackground(True)

        self.setWindowFlags(Qt.SplashScreen)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("""
            QWidget {
                background-color: rgba(100,100,100,255);
            }
            QLabel {
                background-color: rgba(0,0,0,0);
                color: #ffffff;
                font-family: DejaVuCondensed;
            }
        """)

    def update_stats(self, cmd = None):

        if cmd == None:
            print('{} std-req'.format(time.strftime("%Y.%m.%d %H:%M:%S")))
            request = self.http_wrapper.vlc_req()
        else:
            print('{} cstm-req'.format(time.strftime("%Y.%m.%d %H:%M:%S")))
            request = self.http_wrapper.vlc_cmd(cmd)

        try:
            d_a = request.findall(self.pos_a)[0].text
        except:
            d_a = "artist"

        try:
            d_t = request.findall(self.pos_t)[0].text
        except:
            d_t = "title"

        try:
            d_v = request.findall(self.pos_v)[0].text
        except:
            d_v = "vol"

        try:
            d_p = request.findall(self.pos_p)[0].text
        except:
            d_p = "playing"

        if "ttvnw.net" in d_t:
            channel = d_t[:100].split("/")[4].split("_")[0]
            v_kraken = fetch_kraken(channel)
            d_t = v_kraken['stream']['channel']['status']
            d_a = v_kraken['stream']['channel']['display_name']

        if self.http_wrapper.muted:
            d_v = "\uD83D\uDD07"
        else :
            try:
                d_v = str(int(int(d_v)/2.55)) + "%"
            except:
                print('')

        self.stat_dict = {self.pos_v: d_v, self.pos_a: d_a, self.pos_t: d_t, self.pos_p: d_p}

    def update_ui(self):

        self.l_a.setText(self.stat_dict[self.pos_a])
        self.l_a.adjustSize()

        self.l_t.setText(self.stat_dict[self.pos_t])
        self.l_t.adjustSize()

        self.b_vm.setText(self.stat_dict[self.pos_v])

        self.adjustSize()

        QApplication.processEvents()

    def on_click(self, cmd):

        self.update_ui()
        self.update_stats(cmd)

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    screen = vlcc()
    screen.show()
    screen.update_stats()

    ui_timer = QTimer(screen)
    ui_timer.timeout.connect(screen.update_ui)
    ui_timer.start(500)

    stat_timer = QTimer(screen)
    stat_timer.timeout.connect(screen.update_stats)
    stat_timer.start(10000)

    sys.exit(app.exec_())
