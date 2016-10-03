#!/usr/bin/python3

import tkinter as tk
import xml.etree.ElementTree as etree
import html
from vlcHTTPWrapper import *

pos_v = ".//volume"
pos_p = ".//*[@name='now_playing']"
pos_t = ".//*[@name='filename']"
pos_a = ".//*[@name='artist']"


def update_stat(stat: str, v_stat: tk.StringVar) -> str:

    """Get the requested status value from vlc
    kwargs:
    stat -- xpath to enclosing tag
            e.g:    <volume>:               './/volume'
                    <* name='filename'>:    './/*[@name='filename']'
    """
    try:
        request = vlc_req()

        if (stat == pos_a or stat == pos_t) and len(request.findall(pos_p)) > 0:

            status = request.findall(pos_p)[0].text.split(" | ")[0].split(" - ")

            if stat == pos_t:
                status = status[1]
            elif stat == pos_a:
                status = status[0]

            status = html.unescape(status)

        elif stat == pos_t and "monstercat" in request.findall(pos_t)[0].text[:100]:

            status = "monstercatFM"

        elif stat == pos_a and "monstercat" in request.findall(pos_t)[0].text[:100]:

            status = "-"

        else:

            status = request.findall(stat)[0].text

    except:
        if stat == pos_v:
            status = "vol"
        elif stat == pos_a:
            status = "Artist"
        elif stat == pos_t:
            status = "Title"
        elif stat == pos_p:
            status = "-"
        else:
            status = "-"

    v_stat.set(status)

    w_ctrl.after(5000, lambda: update_stat(stat, v_stat))



w_ctrl = tk.Tk()

color1 = "#00A0B1"

p_bck = tk.PhotoImage(file="res/previous.png")
p_fwd = tk.PhotoImage(file="res/next.png")
p_ply = tk.PhotoImage(file="res/play.png")
p_pse = tk.PhotoImage(file="res/pause.png")

tk.Button(w_ctrl, image=p_bck,bg=color1,border=0,command=lambda: vlc_cmd('previous'))\
    .place(x=5, y=30)

tk.Button(w_ctrl, image=p_fwd, bg=color1, border=0, command=lambda: vlc_cmd('next'))\
    .place(x=95, y=30)

tk.Button(w_ctrl, image=p_ply, bg=color1, border=0, command=lambda: vlc_cmd('pause'))\
    .place(x=50, y=30)

v_vol = tk.StringVar()
update_stat(pos_v, v_vol)

tk.Label(w_ctrl, textvariable=v_vol, fg='white', bg=color1, font="DejaVuSansCondensed 20")\
    .place(x=55, y=95)

tk.Button(w_ctrl, text="+", fg="white", font="DejaVuSans 30", bg=color1, border=0, command=lambda: vlc_do('volup', v_vol))\
    .place(x=90, y=80)

tk.Button(w_ctrl, text="-", fg="white", font="DejaVuSans 30", bg=color1, border=0, command=lambda: vlc_do('voldown', v_vol))\
    .place(x=10, y=77)


w_ctrl.geometry("150x150+1945+540")
w_ctrl.configure(background=color1)
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
#w_info.attributes("-alpha", '0.2')
w_info.overrideredirect(True)


w_ctrl.mainloop()