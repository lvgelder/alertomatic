import feedparser
import models
import logging
from datetime import datetime


def parseFeed(rssUrl):
    d = feedparser.parse(rssUrl)
    count=0
    for item in d['items']:
        count=count+1

        article_url = item.link.split("&url=")[1]
        if(article_url.startswith("http://www.guardian")):
            logging.info(article_url);
            logging.info(models.get_article(article_url));
            if(not models.get_article(article_url)):
                models.store_article(datetime.now(), datetime.strptime(item.date, "%a, %d %b %Y %H:%M:%S %Z"), item.title, article_url, rssUrl, count,  alerted=False)
  