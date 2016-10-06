import json, sys, getopt
import urllib.request as ulib

def fetch_kraken(TwitchChannel):
    clientid = 'taf50me5uagadpa70zl5rf8vp0j3d96'
    url = str('https://api.twitch.tv/kraken/streams/'+TwitchChannel+'?client_id='+clientid)
    try:
        response = ulib.urlopen(url)
        data = json.loads(response.read().decode('utf-8'))
    except:
        data = ""

    return data

