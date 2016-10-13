#!/usr/bin/python3

import urllib.request as req
import xml.etree.ElementTree as etree
import tkinter as tk


class vlcHTTPWrapper:

    # status vars
    volume = 0
    muted = False
    url = "http://localhost:8080/requests/status.xml"
    opener = ""

    def __init__(self, usr: str, pwd: str, port: str):

        """
        SETUP: setting HTTP Auth ond creating the opener for HTTP requests

        Args:
            usr(str): user for http-request
            pwd(str): password for http-request
            port(int): port for vlc http server
        """

        if port != "8080":
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

        Args:
            requrl(str): custom url to use for vlc_req()

        Returns:
            (xml.etree.ElementTree)
        """
        try:
            resp = self.opener.open(requrl)
            resp_str = resp.read().decode('utf-8').strip()
            data = etree.fromstring(resp_str)
        except:
            data = etree.fromstring("<volume>vol</volume>")

        return data

    def vlc_cmd(self, cmd: str) -> etree:

        if cmd == 'pause':
            cmdurl = 'pl_pause'

        elif cmd == 'next':
            cmdurl = 'pl_next'

        elif cmd == 'back':
            cmdurl = 'pl_previous'

        elif cmd == 'volup':
            volume = int(self.vlc_req().findall(".//volume")[0].text)

            cmdurl = 'volume&val=' + str(volume + 5)

        elif cmd == 'mute':
            volume = int(self.vlc_req().findall(".//volume")[0].text)

            if not self.muted:
                cmdurl = 'volume&val=0'
                self.volume = volume

            else:
                cmdurl = 'volume&val=' + str(self.volume)

            self.muted = not self.muted

        elif cmd == 'voldown':
            volume = int(self.vlc_req().findall(".//volume")[0].text)

            cmdurl = 'volume&val=' + str(volume - 5)
        else:
            cmdurl = ''

        return self.vlc_req(requrl=str(self.url + "?command=" + cmdurl))