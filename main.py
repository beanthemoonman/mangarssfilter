#!/usr/bin/python
import requests
import rfeed
import feedparser
import datetime
import argparse
from lxml import html, etree


def getFollowedSeries(linksfeed):
    linkspage = requests.get(linksfeed)
    linkshtml = html.fromstring(linkspage.content)
    return linkshtml.xpath('//a[@title="Series Info"]/@href')

def curateRssFeed(linksfeed,rssfeed):
    linkstable = getFollowedSeries(linksfeed)
    rss = feedparser.parse(rssfeed)
    for i in rss.entries:
        if hasattr(i,'link') and i.link in linkstable:
            yield rfeed.Item(
                title=i.title,
                link=i.link,
                description=i.description
            )

if __name__ == "__main__":
    rssfeed = 'https://www.mangaupdates.com/rss.php'
    linksfeed = 'https://www.mangaupdates.com/mylist.html?id=598460&list=read'

    feed = rfeed.Feed(
        title="Upmoon Filtered Manga Updates Feed",
        link="https://rss.beanthemoonman.io:8443/manga/rss.xml",
        description="Real degen hours",
        language="en-US",
        lastBuildDate=datetime.datetime.now(),
        items=curateRssFeed(linksfeed,rssfeed)
    )
    print(feed.rss())
    