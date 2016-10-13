#!/usr/bin/python3

import tkinter as tk
import xml.etree.ElementTree as etree
import html, json, os, time
from vlcHTTPWrapper import *
from twitch import *

class vlcc:

    # SETUP
    f = open(os.path.join(os.path.dirname(__file__), "settings.json"), "r")
    j_settings = json.load(f)

    color = j_settings['appearance']['color']

    pos_x = int(j_settings['appearance']['pos']['x'])
    pos_y = int(j_settings['appearance']['pos']['x'])

    http_wrapper = vlcHTTPWrapper(j_settings['security']['user'], j_settings['security']['password'], str(j_settings['security']['port']))

    # xml-lookup variables
    pos_v = ".//volume"
    pos_p = ".//*[@name='now_playing']"
    pos_t = ".//*[@name='filename']"
    pos_a = ".//*[@name='artist']"
    stat_dict = {pos_v: 'v', pos_a: 'a', pos_t: 't'}

    w_ctrl = tk.Tk()
    w_info = tk.Toplevel()

    v_vol = tk.StringVar()
    v_artist = tk.StringVar()
    v_title = tk.StringVar()

    def update_stats(self, do_cycle = False):

        """
        returns dictionary with displayable values for ui from http-request using the http_wrapper created beforehand

        Args
            stats(dict): dictionary to be replaced (with keys responding to xml-lookups)
        """

        request = self.http_wrapper.vlc_req()

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

        self.stat_dict = {self.pos_v: d_v, self.pos_a: d_a, self.pos_t: d_t}

        if do_cycle:
            self.w_ctrl.after(20000, lambda: self.update_stats(self.stat_dict))

    def update_ui(self, stat: str, v_stat: tk.StringVar, do_cycle = True, timing = 5000):

        """
        update ui elements via its textvar from generated stat-dictionary

        Args:
            stat(str): xml-lookup representing the entry in stat-dictionary
            v_stat(tk.StringVar): textvar for ui element to update
            timing (int = 5000, optional): update delay time in ms
        """

        v_stat.set(self.stat_dict[stat])

        # self-looping
        if do_cycle:
            self.w_ctrl.after(timing, lambda: self.update_ui(stat, v_stat, timing))

    def on_click(self, cmd):

        print(cmd)
        self.http_wrapper.vlc_cmd(cmd)
        if cmd == 'mute':
            if self.http_wrapper.muted:
                print('unmute')
                self.stat_dict[self.pos_v] = "\uD83D\uDD07"
            else:
                print('mute')
                self.stat_dict[self.pos_v] = "{}%".format(int(int(self.http_wrapper.vlc_req().findall(self.pos_v)[0].text)/2.55))

        self.v_vol.set(self.stat_dict[self.pos_v])


    def __init__(self):
        # MAIN

        self.update_stats(self.stat_dict)

        p_bck = tk.PhotoImage(file="res/previous.png")
        p_fwd = tk.PhotoImage(file="res/next.png")
        p_ply = tk.PhotoImage(file="res/play.png")
        p_pse = tk.PhotoImage(file="res/pause.png")

        tk.Button(self.w_ctrl, image=p_bck, bg=self.color, border=0,
                  command=lambda: self.on_click('previous')).place(x=5, y=30)

        tk.Button(self.w_ctrl, image=p_fwd, bg=self.color, border=0,
                  command=lambda: self.on_click('next')).place(x=95, y=30)

        tk.Button(self.w_ctrl, image=p_ply, bg=self.color, border=0,
                  command=lambda: self.on_click('pause')).place(x=50, y=30)

        self.update_ui(self.pos_v, self.v_vol, timing=100)

        tk.Button(self.w_ctrl, text="+", fg="white", font="Consolas 30", bg=self.color, border=0,
                  command=lambda: self.on_click('volup')).place(x=100, y=75)

        tk.Button(self.w_ctrl, text="-", fg="white", font="Consolas 30", bg=self.color, border=0,
                  command=lambda: self.on_click('voldown')).place(x=0, y=75)

        tk.Button(self.w_ctrl, textvariable=self.v_vol, fg='white', font="Consolas 20", bg=self.color, border=0,
                  command=lambda: self.on_click('mute')).place(x=75, y=115, anchor='center')

        self.w_ctrl.geometry("150x150+{}+{}".format(self.pos_x, self.pos_y))
        self.w_ctrl.configure(background=self.color)
        self.w_ctrl.overrideredirect(True)

        self.update_ui(self.pos_a, self.v_artist)

        l_art = tk.Label(self.w_info, textvariable=self.v_artist, fg="#aaa", bg='white', font=('DejaVuSansCondensed', 30))
        l_art.place(x=20, y=90)

        self.update_ui(self.pos_t, self.v_title)

        l_title = tk.Label(self.w_info, textvariable=self.v_title, fg="#999", bg='white', font=('DejaVuSansCondensed', 40))
        l_title.place(x=15, y=15)

        pos_x = (int(self.pos_x) + 150)
        print(pos_x)
        self.w_info.geometry("500x150+{}+{}".format(self.pos_x, self.pos_y))
        self.w_info.configure(background='white')
        self.w_info.overrideredirect(True)

        self.w_ctrl.mainloop()


vlcc()