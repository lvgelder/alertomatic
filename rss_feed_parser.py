import feedparser
import models
import logging
import notifications
from datetime import datetime


def parseFeed(rssUrl):
    d = feedparser.parse(rssUrl)
    count=0
    for item in d['items']:
        count=count+1

        new_articles= list();
        article_url = item.link.split("&url=")[1]
        if(article_url.startswith("http://www.guardian")):
            logging.info(article_url);
            logging.info(models.get_article(article_url))
            if(not models.get_article(article_url)):
                new_article = models.create_article(datetime.now(), datetime.strptime(item.date, "%a, %d %b %Y %H:%M:%S %Z"), item.title, article_url, rssUrl, count,  alerted=False)
                new_articles.append(new_article)
                models.store_article(new_article)
        if(len(new_articles)>0):
            logging.info("Found new headlines.  Sending alerts")
            notifications.send_alerts(rssUrl,new_articles)

  