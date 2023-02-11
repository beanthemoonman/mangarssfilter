#!/usr/bin/python
import argparse
import requests
from lxml import html


LOGIN_URL = 'https://www.mangaupdates.com/login.html'
VALID_CONFIG_ITEMS = [
    'username',
    'password'
]


def loginAndScrape(conf, url):
    sesh = requests.session()
    sesh.post(url=LOGIN_URL, data={
        'act': 'login',
        'username': conf['username'],
        'password': conf['password']
    })
    response = sesh.get(url)
    followhtml = html.fromstring(response.content)
    return followhtml.xpath('//a[@title="Series Info"]/@href')


def getConfig(conffile):
    configfile = open(conffile, mode='r')
    configobject = {}

    for i in configfile:
        items = i.replace('\n', '').split('=')
        if len(items) == 2 and items[0] in VALID_CONFIG_ITEMS:
            configobject[items[0]] = items[1]

    return configobject


if __name__ == '__main__':
    def parseArgs():
        prsr = argparse.ArgumentParser()
        prsr.add_argument('-c', '--configfile',
                          help='Config file location',
                          required=True,
                          type=str)
        prsr.add_argument('-u', '--listurl',
                          help='MU List URL',
                          required=True,
                          type=str)
        return prsr

    def main():
        parser = parseArgs().parse_args()
        cfgfile = parser.configfile
        listurl = parser.listurl

        configobject = getConfig(cfgfile)

        series = loginAndScrape(configobject, listurl)

        for url in series:
            print(url)
    main()
