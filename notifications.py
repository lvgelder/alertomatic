from google.appengine.api import mail
import models
import logging


def send_alerts(feed_url, articles):
    for article in articles:
        slug = extract_slug(article.url)
        fid = extract_feed_identifier(feed_url)
        for email in models.get_emails():
            subject =  slug+" : position 1 : Google News "+fid
            if(article.category):
                subject =  subject + " "+ article.category
            message = mail.EmailMessage(sender="sheena.luu@guardian.co.uk",
                                        subject=subject)
            message.to = email.email_address
            message.body = format_message(feed_url, article)
            message.send()
            logging.info("*****sent email alert to "+email.email_address+" with subject "+subject)

def send_death_alert(feed_url, articles):
    for article in articles:
        slug = extract_slug(article.url)
        fid = extract_feed_identifier(feed_url)
        for email in models.get_emails():
            subject =  slug+" : removed from position 1 : Google News "+fid
            if(article.category):
                subject =  subject + " "+ article.category
            message = mail.EmailMessage(sender="sheena.luu@guardian.co.uk",
                                        subject=subject)
            message.to = email.email_address
            message.body = format_headline_death_message(feed_url, article)
            message.send()
            logging.info("*****sent headline-death alert to "+email.email_address+" with subject "+subject)


def format_message(feed_url, article):
    fid = extract_feed_identifier(feed_url)
    body = "This article:  "+ article.url +" has been spotted in top position in cluster " + str(article.position) + " in Google news "+fid+" "+ article.category
    body = body + extract_feed_identifier(feed_url)
    body = body + " at "+str(article.created_at)+": \n"
    body = body + "\n-----------------------------\n"
    body = body + "This is an automatic alert.  Share and enjoy!"
    return body

def format_headline_death_message(feed_url, article):
    fid = extract_feed_identifier(feed_url)
    body = "This article:  "+ article.url +" has been removed from top position in Google news "+fid+" "+ article.category
    body = body + extract_feed_identifier(feed_url)
    body = body + " at "+str(article.created_at)+": \n"
    body = body + "\n-----------------------------\n"
    body = body + "This is an automatic alert.  Share and enjoy!"
    return body

def extract_slug(article_url):
    if("http://www.guardiannews.com" in article_url):
        slug = article_url.split("http://www.guardiannews.com")[1]
    elif("http://www.guardian.co.uk" in article_url):
        slug = article_url.split("http://www.guardian.co.uk")[1]
    return slug

def extract_feed_identifier(feed_url):
    if("ned=uk" in feed_url):
        return "UK"
    elif("ned=us" in feed_url):
        return "US"
    else:
        return feed_url
