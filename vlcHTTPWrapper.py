#!/usr/bin/python3

import urllib.request as req
import xml.etree.ElementTree as etree
import tkinter as tk

pwd_mgr = req.HTTPPasswordMgrWithDefaultRealm()
pwd_mgr.add_password(None,
                     'https://localhost:8080/',
                     '',
                     'abcde')
auth_handler = req.HTTPBasicAuthHandler(pwd_mgr)
opener = req.build_opener(auth_handler)
req.install_opener(opener)

url = str('http://localhost:8080/requests/status.xml')


def vlc_req(requrl=url) -> etree:
    try:
        resp = opener.open(requrl)
        resp_str = resp.read().decode('utf-8').strip()
        data = etree.fromstring(resp_str)
    except:
        data = etree.fromstring("<volume>vol</volume>")

    return data


def vlc_cmd(cmd: str) -> etree:
    if cmd == 'pause':
        cmdurl = 'pl_pause'
    elif cmd == 'next':
        cmdurl = 'pl_next'
    elif cmd == 'back':
        cmdurl = 'pl_previous'
    else:
        cmdurl = ''

    return vlc_req(requrl=(url + "?command=" + cmdurl))


def vlc_do(cmd: str, v_vol: tk.StringVar) -> etree:
    volume = int(vlc_req().findall(".//volume")[0].text)

    if cmd == 'volup':
        vol_chg = volume + 5

    elif cmd == 'voldown':
        vol_chg = volume - 5

    v_vol.set(str(vol_chg))

    return vlc_req(requrl=(url + "?command=volume&val=" + str(vol_chg)))
