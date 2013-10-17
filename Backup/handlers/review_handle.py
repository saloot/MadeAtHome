import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db
from dbs.databases import Orders_DB

class ReviewHandler(webapp2.RequestHandler):        
    def get(self):
        u = self.request.get('u')
        #b = Orders_DB(rating = 0)
        #b.put()
        #u = make_hashed_cookie('%s' %str(b.key()))
        #943057e9a46648a8d68817518c8196e98575f961bea6309aa77aabba9f725e4b|ahBkZXZ-bWFkZWF0bXlob21lchYLEglPcmRlcnNfREIYgICAgICAgAsM
        order_id = valid_hash_cookie(u)
        if order_id:
            l = db.get(order_id)
            params = {}
            if l:
                if l.reviewed:
                    self.response.out.write('you can edit your rating!')
                else:
                    self.response.out.write(template.render('./html/review_form.html',params))
            else:
                self.response.out.write('Invalid review link!')
        else:
            self.response.out.write('Invalid review link!')

    def post(self): 
        params = {}
        rate = self.request.get('rating_button')
        comments = escape_html(self.request.get('comments'))
        success_flag = 1
        params['comments_value'] = comments
        
        
        if not rate:
            params['error_rating'] = 'Rating is mandatory!'
            success_flag = 0
        
        if success_flag:
            self.response.out.write('Your comments will be UPDATED!')
        else:
            self.response.out.write(template.render('./html/review_form.html',params))
            