#!/usr/bin/python
import requests
import rfeed
import feedparser
from datetime import date, datetime, timedelta
import argparse
import itertools
import json
from os import path
from lxml import html


def getFollowedSeries(followlink):
    followpage = requests.get(followlink)
    followhtml = html.fromstring(followpage.content)
    return followhtml.xpath('//a[@title="Series Info"]/@href')


def curateRssFeed(followlink, rssfeed):
    rss = feedparser.parse(rssfeed)
    for i in rss.entries:
        if hasattr(i, 'link') and i.link in getFollowedSeries(followlink):
            yield rfeed.Item(
                title=i.title,
                link=i.link,
                description=i.description
            )


"""
Cache format:
[
    {
        "title":"abc",
        "link":"abc",
        "description":"abc",
        "timestamp":"POSIX Timestamp Format"
    }
]
"""
def getCache(cachefile,seconds):
    cachejson = json.load(open(cachefile, mode='r'))
    relevantcache = []
    for i in cachejson:
        if date.fromtimestamp(i['timestamp']) < \
                datetime.now() - timedelta(seconds=seconds * -1):
            relevantcache.append(i)
    return relevantcache


def parseCache(cache):
    for i in cache:
        yield rfeed.Item(
            title=i.title,
            link=i.link,
            description=i.description
        )


def writeCache(cachefile,cache,feed):
    outfile = open(cachefile, mode='w')
    now = datetime.now()
    out = []
    for i in cache:
        out.append(i)
    for i in feed:
        out.append(
            {
                "title": i.title,
                "link": i.link,
                "description": i.description,
                "timestamp": str(now.timestamp())
            }
        )
    outfile.write(json.dumps(out))


def parseArgs():
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--rssfeed',
                        help='mangaupdates rss feed',
                        required=True,
                        type=str)
    parser.add_argument('-f', '--followlink',
                        help='mangaupdates user following page',
                        required=True,
                        type=str)
    parser.add_argument('-t', '--title',
                        help='RSS Feed Title',
                        required=False,
                        default='RSS Feed Title',
                        type=str)
    parser.add_argument('-l', '--link',
                        help='RSS Feed URL',
                        required=False,
                        default='http://localhost',
                        type=str)
    parser.add_argument('-c', '--cachefile',
                        help='cache filename',
                        required=False,
                        default="",
                        type=str)
    parser.add_argument('-s', '--seconds',
                        help='cache persistance seconds',
                        required=False,
                        default=120,
                        type=int)
    return parser


if __name__ == "__main__":
    parser = parseArgs().parse_args()
    rssfeed = parser.rssfeed
    followlink = parser.rssfeed
    title = parser.title
    link = parser.link
    cachefile = parser.cachefile
    seconds = parser.seconds

    oldrssfeed = []
    currentrssfeed = curateRssFeed(followlink, rssfeed)
    if cachefile != "":
        cache = []
        if path.exists(cachefile):
            cache = getCache(cachefile, seconds)
        writeCache(cachefile, cache, currentrssfeed)
        oldrssfeed = parseCache(cache)

    print(rfeed.Feed(
            title=title,
            link=link,
            description="Curated MU Feed",
            language="en-US",
            lastBuildDate=datetime.now(),
            items=itertools.chain(oldrssfeed, currentrssfeed)
        ).rss()
    )
