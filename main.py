#!/usr/bin/env python

import os
import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.api import memcache
import helpers
import logging
import rss_feed_parser
import models


class MainHandler(webapp.RequestHandler):
    @helpers.write_response
    #@helpers.cached('main')
    def get(self):
        return helpers.render_template(self, 'webviews/front.html', {'person': 'me'})

class PollHandler(webapp.RequestHandler):
    def get(self):
        for feed_url in models.get_urls():
            logging.info("********** parsing feed from " + feed_url.url)
            rss_feed_parser.parseFeed(feed_url.url)

    def post(self):
        logging.info("********** task worked")
        for feed_url in models.get_urls():
            logging.info("********** parsing feed from " + feed_url.url)
            rss_feed_parser.parseFeed(feed_url.url)



def main():
  application = webapp.WSGIApplication([
        ('/', MainHandler),
        ('/services/poll', PollHandler),

        ],    debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
