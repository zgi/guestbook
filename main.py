#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Vnos

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")


class VnosHandler(BaseHandler):
    def get(self):
        return self.render_template("vnos.html")
    def post(self):
        ime = self.request.get("ime").replace('<script>', '').replace('</script>', '')
        priimek = self.request.get("priimek").replace('<script>', '').replace('</script>', '')

        if ime == '':
            ime = 'neznanec'
        if priimek == '':
            priimek = 'neznanec'

        email = self.request.get("email").replace('<script>', '').replace('</script>', '')
        sporocilo = self.request.get("sporocilo").replace('<script>', '').replace('</script>', '')

        data = Vnos(ime=ime, priimek=priimek, email=email, sporocilo=sporocilo)
        data.put()
        return self.redirect('/')

class SeznamSporocilHandler(BaseHandler):
    def get(self):
        seznam = Vnos.query().fetch()
        params = {'seznam': seznam}
        return self.render_template("seznam_sporocil.html", params=params)

app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/vnos', VnosHandler),
    webapp2.Route('/seznam-sporocil', SeznamSporocilHandler),
], debug=True)