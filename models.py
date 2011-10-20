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

class EmailAddressForm(djangoforms.ModelForm):
      class Meta:
        model = EmailAddress

def store_article(created_at, published_time, title, url, feed_url, position, alerted=False):
    report = Article(created_at=created_at, published_time=published_time, title=title, url=url, feed_url=feed_url, position=position, alerted=alerted)
    report = report.put()
    return report.id()

def store_email(email_address):
    email = EmailAddress(email_address=email_address)
    email = email.put()
    return email.id()

def get_article(url):
    return db.Query(Article).filter('url=',url).get()

def store_url(url):
    url = Url(url=url)
    url = url.put()
    return url.id()


def get_urls(maximum=250):
    return db.Query(Url).fetch(maximum)


def get_url(key):
    return Url.get_by_id(int(key))
