from google.appengine.api import mail
import models
import logging


def send_alerts(feed_url, articles):
    for article in articles:
        slug = extract_slug(article.url)
        fid = extract_feed_identifier(feed_url)
        for email in models.get_emails():
            message = mail.EmailMessage(sender="sheena.luu@guardian.co.uk",
                                         subject=slug+" : "+str(article.position)+" in "+fid)
            message.to = email.email_address
            message.body = format_message(feed_url, article)
            message.send()
            logging.info("sent email alert to "+email.email_address)

def send_death_alert(feed_url, articles):
    for article in articles:
        slug = extract_slug(article.url)
        fid = extract_feed_identifier(feed_url)
        for email in models.get_emails():
            message = mail.EmailMessage(sender="sheena.luu@guardian.co.uk",
                                        subject=slug+" : removed from "+fid)
            message.to = email.email_address
            message.body = format_headline_death_message(feed_url, article)
            message.send()
            logging.info("sent headline-death alert to "+email.email_address)


def format_message(feed_url, article):
    body = "This article:  "+ article.url +" has been spotted in position " + str(article.position) + " in Google news "
    body = body + extract_feed_identifier(feed_url)
    body = body + " at "+str(article.created_at)+": \n"
    body = body + "\n-----------------------------\n"
    body = body + "This is an automatic alert.  Share and enjoy!"
    return body

def format_headline_death_message(feed_url, article):
    body = "This article:  "+ article.url +" has been removed from Google news "
    body = body + extract_feed_identifier(feed_url)
    body = body + " at "+str(article.created_at)+": \n"
    body = body + "\n-----------------------------\n"
    body = body + "This is an automatic alert.  Share and enjoy!"
    return body

def extract_slug(article_url):
    slug = article_url.lstrip('http://www.guardiannews.com')
    slug = slug.lstrip('http://www.guardian.co.uk')
    return slug

def extract_feed_identifier(feed_url):
    if("ned=uk" in feed_url):
        return "uk"
    elif("ned=us" in feed_url):
        return "us"
    else:
        return feed_url
