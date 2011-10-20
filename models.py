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


def store_article(created_at, published_time, title, url, position, alerted=False):
    report = Article(created_at=created_at, published_time=published_time, title=title, url=url, position=position, alerted=alerted)
    report = report.put()
    return report.id()
