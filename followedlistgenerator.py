#!/usr/bin/python
import argparse
import requests
from lxml import html


def scrape(url):
    response = requests.get(url)
    followhtml = html.fromstring(response.content)
    return followhtml.xpath('//a[@title="Click for Series Info"]/@href')


if __name__ == '__main__':
    def parseArgs():
        prsr = argparse.ArgumentParser()
        prsr.add_argument('-u', '--listurl',
                          help='MU List URL',
                          required=True,
                          type=str)
        return prsr

    def main():
        parser = parseArgs().parse_args()
        listurl = parser.listurl

        series = scrape(listurl)

        for url in series:
            print(url)
    main()
