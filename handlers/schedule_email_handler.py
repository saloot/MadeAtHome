import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db
from dbs.databases import Orders_DB
from google.appengine.api import mail

class EmailScheduleHandler(webapp2.RequestHandler):        
    def post(self):
        order_id = self.request.get('order_id')
        e = self.request.get('user_email')
        user_email_add  = e.replace("%40","@")
        #b = Orders_DB(rating = 0)
        #b.put()
        u = make_hashed_cookie('%s' %order_id )
        #943057e9a46648a8d68817518c8196e98575f961bea6309aa77aabba9f725e4b|ahBkZXZ-bWFkZWF0bXlob21lchYLEglPcmRlcnNfREIYgICAgICAgAsM
        #self.response.out.write(user_email_add)
        
        #==============SEND THE REVIEW EMAIL TO THE USER=============
        str0 = '<html> <head><style> td{text-align:center;}</style></head> <body>'
        email_body = '<table cellpadding="0" cellspacing="0" border="0" align="center"> '
        email_body = email_body + '<td width="600" valign="top"><h3><span style="color:#888888">A while ago, you ordered from our site.</span></h3><h4><span style="color:#888888">We really appreciate it if you could take a moment to share your opinion about the quality of the whole service with us by clicking over <a href="%s/_review?u=%s">this link</a></span></h4></tr></tbody></table>'%(home_site,u)
        str3 = '</body></html>'
        msg_content = str0 + email_body  + str3
        message = mail.EmailMessage(sender="Amir Hesam Salavati <saloot@gmail.com>",
        subject="Order confirmation")
        message.to = "%s" %str(user_email_add)
        message.html = """%s""" %msg_content
                    
   
        message.send()
        #==================================================================
