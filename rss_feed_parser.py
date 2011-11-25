import feedparser
import models
import logging
import notifications
from datetime import datetime
from datetime import timedelta
from pprint import pprint
from description_parsing import processDescriptionWithSoup

def parseFeed(rssUrl):

    d = feedparser.parse(rssUrl)
    for itemnumber in range(0, len(d.entries)):

        new_articles= list()
        itemnumber_plus_one = itemnumber +1
        article_title=d.entries[itemnumber].title
        #rssUrl = d.entries[itemnumber].links[0].href
        article_url = parseFeedUrl(d.entries[itemnumber].links[0].href)

        pubtime = datetime.strptime(d.entries[itemnumber].updated, "%a, %d %b %Y %H:%M:%S %Z")
        #pubtime = changeToSummerTime(pubtime)
        polledtime = datetime.now()
        #polledtime = = changeToSummerTime(polledtime)
        category = getCategory(d,rssUrl)
        if(article_url.startswith("http://www.guardian.co.uk") or article_url.startswith("http://www.guardiannews.com")):
            sub_position = 1
            count = itemnumber_plus_one
            ranked_article = [polledtime, pubtime, article_title, article_url, category, rssUrl,  count, sub_position, False]
            addNewArticle(new_articles,ranked_article)
        else:
            description = processDescriptionWithSoup(d.entries[itemnumber].description, 2)
            for entries in description:
                sub_position = entries[0]
                #rssUrl = entries[1]
                article_url = parseUrlFromDescription(entries[1])
                article_title = entries[2]
                count = itemnumber_plus_one
                ranked_article = [polledtime, pubtime, article_title, article_url, category, rssUrl,  count, sub_position, False]
                addNewArticle(new_articles,ranked_article)

        if(len(new_articles)>0):
            logging.info("Found new headlines.  Sending alerts")
            notifications.send_alerts(rssUrl,new_articles)

def getCategory(feed,rssUrl):
    for item in feed['items']:
        my_category = item.tags[0].term
    return my_category

def checkDeath(rssUrl):
    print("Feed" + rssUrl)
    stored_articles = models.get_articles_for_feed(rssUrl)
    print(len(stored_articles))
    for item in stored_articles:
        print(item)

    rss_article_url_list = list()
    d = feedparser.parse(rssUrl)
    for item in d['items']:
        article_url = parseFeedUrl(item.link)
        rss_article_url_list.append(article_url)
        print("rss_article_url" + article_url)

    print("first length")
    print(len(rss_article_url_list))
    for itemnumber in range(0, len(d.entries)):
        description = processDescriptionWithSoup(d.entries[itemnumber].description, 2)
        for entries in description:
            article_url = parseUrlFromDescription(entries[1])
            rss_article_url_list.append(article_url)


    print("second length")
    print(len(rss_article_url_list))
    dead_articles = list()
    for x in rss_article_url_list:
        print('RssArticleUrl' + x)
    for article in stored_articles:
        print("article url in stored articles" + article.url)
        if(not article.url in rss_article_url_list):
            print("Article not in the rss Url list anymore")
            print(' article url:    '+ article.url)
            dead_articles.append(article)
            article.delete()
    print("dead articles length")
    print(len(dead_articles))
    
    if(len(dead_articles)>0):
        logging.info("Headline died.  Sending alerts")
        notifications.send_death_alert(rssUrl,dead_articles)

def parseFeedUrl(rssUrl):
    article_url = rssUrl.split("&url=")[1]
    article_url = article_url.split("?newsfeed")[0]
    return article_url

def changeToSummerTime(my_time):
    plushour = timedelta(hours=1)
    summer_time = my_time + plushour
    return summer_time

def parseUrlFromDescription(Url):
    splitted_array = Url.split("&url=")
    if len(splitted_array) == 2:
        article_url = splitted_array[1]
    else:
        article_url = splitted_array[0]
        article_url = splitted_array.split("?newsfeed")[0]
    return article_url

def addNewArticle(list_of_new_articles, possible_new_article):
    article_url = possible_new_article[3]
    rssUrl = possible_new_article[5]
    logging.info(article_url)
    logging.info(models.get_article(article_url,rssUrl))
    if(not models.get_article(article_url,rssUrl)):
        new_article = models.create_article(possible_new_article[0], possible_new_article[1],possible_new_article[2],possible_new_article[3],possible_new_article[4],possible_new_article[5],possible_new_article[6],possible_new_article[7],possible_new_article[8])
        list_of_new_articles.append(new_article)
        new_article.put()
