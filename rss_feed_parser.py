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

        new_articles= list()
        article_url = item.link.split("&url=")[1]
        article_url = article_url.split("?newsfeed")[0]
        if(article_url.startswith("http://www.guardian.co.uk") or article_url.startswith("http://www.guardiannews.com")):
            logging.info(article_url)
            logging.info(models.get_article(article_url))
            if(not models.get_article(article_url)):
                new_article = models.create_article(datetime.now(), datetime.strptime(item.date, "%a, %d %b %Y %H:%M:%S %Z"), item.title, article_url, item.category, rssUrl, count,  alerted=False)
                new_articles.append(new_article)
                new_article.put()

        if(len(new_articles)>0):
            logging.info("Found new headlines.  Sending alerts")
            notifications.send_alerts(rssUrl,new_articles)


def checkDeath(rssUrl):
    stored_articles = models.get_articles_for_feed(rssUrl)

    rss_article_url_list = list()
    d = feedparser.parse(rssUrl)
    for item in d['items']:
        article_url = item.link.split("&url=")[1]
        article_url = article_url.split("?newsfeed")[0]
        rss_article_url_list.append(article_url)

    dead_articles = list()
    for article in stored_articles:
        if(not article.url in rss_article_url_list):
            dead_articles.append(article)
            article.delete()


    if(len(dead_articles)>0):
        logging.info("Headline died.  Sending alerts")
        notifications.send_death_alert(rssUrl,dead_articles)



  