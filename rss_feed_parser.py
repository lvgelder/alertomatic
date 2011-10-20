import feedparser
import models
import datetime


def parseFeed(rssUrl):
    d = feedparser.parse("http://news.google.com/news?ned=uk&topic=h&output=rss")
    count=0
    for item in d['items']:
        count=count+1

        articleUrl = item.link.split("&url=")[1]
        if(articleUrl.startswith("http://www.guardian")):
            articleTitle = item.title
            articlePosition = count
            articleCategory = item.category
            #articlePubDate = item.pubDate
            models.store_article(datetime.datetime.now(), datetime.datetime.now(), articleTitle, articleUrl, articlePosition,  alerted=False)
  