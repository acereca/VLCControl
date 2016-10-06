#!/usr/bin/python3

import tkinter as tk
import xml.etree.ElementTree as etree
import html, json, os
from vlcHTTPWrapper import *
from twitch import *

# SETUP
f = open(os.path.join(os.path.dirname(__file__), "settings.json"), "r")
j_settings = json.load(f)

color = j_settings['appearance']['color']

pos_x = int(j_settings['appearance']['pos']['x'])
pos_y = int(j_settings['appearance']['pos']['x'])

http_wrapper = vlcHTTPWrapper(j_settings['security']['user'], j_settings['security']['password'])

## xml-lookup variables
pos_v = ".//volume"
pos_p = ".//*[@name='now_playing']"
pos_t = ".//*[@name='filename']"
pos_a = ".//*[@name='artist']"


def get_stats():

    """
    returns dictionary with displayable values for ui from http-request using the http_wrapper created beforehand
    :return (dict): disctionary with keys responding to xml-lookups (pos_...)
    """

    request = http_wrapper.vlc_req()

    try:
        disp_a = request.findall(pos_a)[0].text
    except:
        disp_a = "artist"

    try:
        disp_t = request.findall(pos_t)[0].text
    except:
        disp_t = "title"

    try:
        disp_v = request.findall(pos_v)[0].text
    except:
        disp_v = "vol"

    if "ttvnw.net" in disp_t:
        channel = disp_t[:100].split("/")[4].split("_")[0]
        d_kraken = fetch_kraken(channel)
        disp_t = d_kraken['stream']['channel']['status']
        disp_a = d_kraken['stream']['channel']['display_name']

    if http_wrapper.muted:
        disp_v = "\uD83D\uDD07"

    return {pos_v: disp_v, pos_a: disp_a, pos_t: disp_t}

#TODO: change update to use cached values

def update_stat(stat: str, v_stat: tk.StringVar, timing = 5000):

    """
    update ui elements via its textvar from generated stat-dictionary

    Args:
        stat(str): xml-lookup representing the entry in stat-dictionary
        v_stat(tk.StringVar): textvar for ui element to update
        timing (int = 5000, optional): update delay time in ms
    """

    stats = get_stats()
    v_stat.set(stats[stat])

    # self-looping
    w_ctrl.after(timing, lambda: update_stat(stat, v_stat))


# MAIN

w_ctrl = tk.Tk()

p_bck = tk.PhotoImage(file="res/previous.png")
p_fwd = tk.PhotoImage(file="res/next.png")
p_ply = tk.PhotoImage(file="res/play.png")
p_pse = tk.PhotoImage(file="res/pause.png")

tk.Button(w_ctrl, image=p_bck, bg=color, border=0,
          command=lambda: http_wrapper.vlc_cmd('previous')).place(x=5, y=30)

tk.Button(w_ctrl, image=p_fwd, bg=color, border=0,
          command=lambda: http_wrapper.vlc_cmd('next')).place(x=95, y=30)

tk.Button(w_ctrl, image=p_ply, bg=color, border=0,
          command=lambda: http_wrapper.vlc_cmd('pause')).place(x=50, y=30)

v_vol = tk.StringVar()
update_stat(pos_v, v_vol, 1000)

tk.Button(w_ctrl, text="+", fg="white", font="DejaVuSans 30", bg=color, border=0,
          command=lambda: http_wrapper.vlc_do('volup', v_vol)).place(x=90, y=80)

tk.Button(w_ctrl, text="-", fg="white", font="DejaVuSans 30", bg=color, border=0,
          command=lambda: http_wrapper.vlc_do('voldown', v_vol)).place(x=10, y=77)

tk.Button(w_ctrl, textvariable=v_vol, fg='white', font="DejaVuSansCondensed 20", bg=color, border=0,
          command=lambda: http_wrapper.vlc_do('mute', v_vol)).place(x=50, y=90)


w_ctrl.geometry("150x150+1945+540")
w_ctrl.configure(background=color)
w_ctrl.overrideredirect(True)

w_info = tk.Toplevel()

v_artist = tk.StringVar()
update_stat(pos_a, v_artist)
l_art = tk.Label(w_info, textvariable=v_artist, fg="#aaa", bg='white', font=('DejaVuSansCondensed', 30))
l_art.place(x=20, y=90)

v_title = tk.StringVar()
update_stat(pos_t, v_title)
l_title = tk.Label(w_info, textvariable=v_title, fg="#999", bg='white', font=('DejaVuSansCondensed', 40))
l_title.place(x=15, y=15)

w_info.geometry("500x150+2095+540")
w_info.configure(background='white')
w_info.overrideredirect(True)


w_ctrl.mainloop()