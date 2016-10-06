#!/usr/bin/python3

import urllib.request as req
import xml.etree.ElementTree as etree
import tkinter as tk


class vlcHTTPWrapper:

    # status vars
    volume = 0
    muted = False
    url = ""
    opener = ""

    def __init__(self, usr: str, pwd: str, port: int):

        """
        SETUP: setting HTTP Auth ond creating the opener for HTTP requests
        :param usr(str): user for http-request
        :param pwd(str): password for http-request
        :param port(int): port for vlc http server
        """
        self.url = str('http://localhost:' + port + '/requests/status.xml')

        pwd_mgr = req.HTTPPasswordMgrWithDefaultRealm()
        pwd_mgr.add_password(None,
                             'https://localhost:8080/',
                             usr,
                             pwd)
        auth_handler = req.HTTPBasicAuthHandler(pwd_mgr)
        self.opener = req.build_opener(auth_handler)
        req.install_opener(self.opener)

    def vlc_req(self, requrl = url) -> etree:

        """
        REQUEST: return xml.ElementTree that vlc HTTP privides
        :param requrl(str): custom url to use for vlc_req()
        :return (xml.etree.ElementTree)
        """

        try:
            resp = self.opener.open(requrl)
            resp_str = resp.read().decode('utf-8').strip()
            data = etree.fromstring(resp_str)
        except:
            data = etree.fromstring("<volume>vol</volume>")

        return data

    def vlc_cmd(self, cmd: str) -> etree:

        """
        REQUEST + CMD: send http-request via vlc_req() with custom url
        :param cmd(str): 'pause', 'next', 'back'
        :return (xml.etree.ElementTree):
        """

        if cmd == 'pause':
            cmdurl = 'pl_pause'
        elif cmd == 'next':
            cmdurl = 'pl_next'
        elif cmd == 'back':
            cmdurl = 'pl_previous'
        else:
            cmdurl = ''

        return self.vlc_req(requrl = str(self.url + "?command=" + cmdurl))


    def vlc_do(self, cmd: str, v_vol: tk.StringVar) -> etree:

        """
        REQUEST + CMD: send http-request via vlc_req() with custom url and setting specified textvar to setr
        :param cmd:
        :param v_vol:
        :return:
        """
        volume = int(self.vlc_req().findall(".//volume")[0].text)

        if cmd == 'volup':
            vol_chg = volume + 5

        elif cmd == 'mute':
            if not self.muted:
                vol_chg = 0
                self.volume = volume

            else:
                vol_chg = self.volume

            self.muted =  not self.muted

        elif cmd == 'voldown':
            vol_chg = volume - 5

        v_vol.set(str(vol_chg) if not self.muted else "\uD83D\uDD07")

        return self.vlc_req(requrl=(self.url + "?command=volume&val=" + str(vol_chg)))
