from google.appengine.ext import db
from google.appengine.ext import search
from google.appengine.ext.webapp import template
from google.appengine.ext.db import djangoforms
import logging


class Article(search.SearchableModel):
    created_at = db.DateTimeProperty()
    published_time = db.DateTimeProperty()
    title = db.StringProperty(required=True)
    url = db.StringProperty(required=True)
    category = db.StringProperty(required=False)
    alerted = db.BooleanProperty(default=False)
    position = db.IntegerProperty(required=True)
    feed_url = db.StringProperty(required=True)


class Url(search.SearchableModel):
    url = db.StringProperty(required=True)

class EmailAddress(search.SearchableModel):
    email_address = db.StringProperty(required=True)


class UrlForm(djangoforms.ModelForm):
      class Meta:
        model = Url

class EmailForm(djangoforms.ModelForm):
      class Meta:
        model = EmailAddress

def create_article(created_at, published_time, title, url, category, feed_url, position, alerted=False):
    report = Article(created_at=created_at, published_time=published_time, title=title, url=url, category=category, feed_url=feed_url, position=position, alerted=alerted)
    return report


def store_email(email_address):
    email = EmailAddress(email_address=email_address)
    email = email.put()
    return email.id()

def get_article(url):
    logging.info("querying for url: "+url)
    query = db.Query(Article).filter('url =', url)
    return query.get()

def get_articles_for_feed(feedurl, maximum=250):
    query = db.Query(Article).filter('feed_url =', feedurl)
    return query.fetch(maximum)


def store_url(url):
    url = Url(url=url)
    url = url.put()
    return url.id()


def get_urls(maximum=250):
    return db.Query(Url).fetch(maximum)

def get_emails(maximum=250):
    return db.Query(EmailAddress).fetch(maximum)


def get_url(key):
    return Url.get_by_id(int(key))

def get_email(key):
    return EmailAddress.get_by_id(int(key))

def get_articles(maximum=250):
    return db.Query(Article).order('position').fetch(maximum)

def get_latest_articles(maximum=5):
    return db.Query(Article).order('-created_at').fetch(maximum)
