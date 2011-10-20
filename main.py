#!/usr/bin/env python

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import memcache
import helpers
import logging
import rss_feed_parser
import datetime


class MainHandler(webapp.RequestHandler):
    @helpers.write_response
    #@helpers.cached('main')
    def get(self):
        return helpers.render_template(self, 'webviews/front.html', {'person': 'me'})

class PollHandler(webapp.RequestHandler):
    def get(self):
        logging.info("********** task worked")
        rss_feed_parser.parseFeed("http://news.google.com/news?ned=uk&topic=h&output=rss")

    #@helpers.cached('main')
    def post(self):
        logging.info("********** task worked")
        #return helpers.render_template(self, 'webviews/front.html', {'person': 'me'})



def main():
  application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/services/poll', PollHandler),

        ],    debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
