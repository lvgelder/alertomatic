import wsgiref.handlers
from google.appengine.ext import webapp
from google.appengine.ext import db
import logging
import models
import helpers


class IndexHandler(webapp.RequestHandler):
    @helpers.write_uncached_response
    def get(self):
        return helpers.render_template(self, 'adminviews/index.html', {})

class ViewUrls(webapp.RequestHandler):
    @helpers.write_uncached_response
    def get(self):
        return helpers.render_template(self, 'adminviews/urls.html', {'urls': models.get_urls(), 'form':models.UrlForm()})


class AddUrl(webapp.RequestHandler):
    @helpers.write_uncached_response
    def post(self):
        form = models.UrlForm(data=self.request.POST)
        if form.is_valid():
            url = form.clean_data["url"]
            newurl = models.store_url(url)
            self.redirect("/admin/view/urls")
        else:
            return helpers.render_template(self, 'adminviews/urls.html', {'urls': models.get_urls(), 'form': form})


class DeleteUrl(webapp.RequestHandler):
    @helpers.write_uncached_response
    def get(self):
        key = self.request.get('key')
        url = models.get_url(key)
        url.delete()
        self.redirect("/admin/view/urls")



def main():
    application = webapp.WSGIApplication([
    ('/admin/', IndexHandler),
    ('/admin/view/urls', ViewUrls),
    ('/admin/delete/url', DeleteUrl),
    ('/admin/add/url', AddUrl),
    ], debug=True)
    wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()