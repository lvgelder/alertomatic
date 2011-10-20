import feedparser
import models
import datetime
import logging


def parseFeed(rssUrl):
    d = feedparser.parse(rssUrl)
    count=0
    for item in d['items']:
        count=count+1

        articleUrl = item.link.split("&url=")[1]
        if(articleUrl.startswith("http://www.guardian")):
            logging.info(articleUrl);
            logging.info(models.get_article(articleUrl));
            if(not models.get_article(articleUrl)):
                models.store_article(datetime.datetime.now(), datetime.datetime.now(), item.title, articleUrl, rssUrl, count,  alerted=False)
  