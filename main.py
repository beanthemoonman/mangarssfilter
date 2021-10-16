import requests
import rfeed
import feedparser
from lxml import html, etree


rssfeed = 'https://www.mangaupdates.com/rss.php'
linksfeed = 'https://www.mangaupdates.com/mylist.html?id=598460&list=read'

if __name__ == "__main__":
    linkspage = requests.get(linksfeed)

    linkshtml = html.fromstring(linkspage.content)

    linkstable = linkshtml.xpath('//a[@title="Series Info"]/@href')

    print(linkstable)


    