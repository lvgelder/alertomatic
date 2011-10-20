from google.appengine.api import mail
import models
import logging


def send_alerts(feed_url, articles):
    for email in models.get_emails():
        message = mail.EmailMessage(sender="sheena.luu@guardian.co.uk",
                                    subject="Alertomatic!  Headline alert!")
        message.to = email.email_address
        message.body = format_message(feed_url, articles)
        message.send()
        logging.info("sent email alert to "+email.email_address)

def send_death_alert(feed_url, articles):
    for email in models.get_emails():
        message = mail.EmailMessage(sender="sheena.luu@guardian.co.uk",
                                    subject="Alertomatic!  Headline Removed alert!")
        message.to = email.email_address
        message.body = format_headline_death_message(feed_url, articles)
        message.send()
        logging.info("sent headline-death alert to "+email.email_address)


def format_message(feed_url, articles):
    body = "Guardian News Headline Alert for "+ feed_url
    for article in articles:
        body = body + "\n-----------------------------\n"
        body = body + str(article.created_at)+": \n"
        body = body + article.title +" \n"
        body = body + article.url +" \n"
        body = body + "in position " + str(article.position)
    return body

def format_headline_death_message(feed_url, articles):
    body = "Guardian News Headline Removed Alert for "+ feed_url
    for article in articles:
        body = body + "\n-----------------------------\n"
        body = body + str(article.created_at)+": \n"
        body = body + article.title +" \n"
        body = body + article.url +" \n"
    return body
