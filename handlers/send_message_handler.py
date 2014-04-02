import webapp2
from madeathome_forms import form_login
from utils import *
from google.appengine.ext.webapp import template
from google.appengine.api import memcache
from google.appengine.ext import db
from dbs.databases import *
from datetime import datetime

class SendMessageHandler(webapp2.RequestHandler):        
    def get(self):
        params = {}            
        recepient_id = self.request.get('u')
        par = self.request.get('p')
        #----------------------Check If a User Has Signed In-------------------------
        temp = self.request.cookies.get('user_id')        
        login_necessary = 0
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params['userid'] = userid
                user = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s'" %userid)
                user = user.get()
                params['chef_flag'] = user.ischef
            else:
                login_necessary = 1
        else:
            login_necessary = 1
        #----------------------------------------------------------------------------
        
        if login_necessary:
            params['return_url'] = './message_send?u='+recepient_id
            self.response.out.write(template.render('./html/login.html',params))
        else:
            self.response.out.write(template.render('./html/message_send.html',params))

    def post(self):
        params = {}
        recepient_id = self.request.get('u')
        par = self.request.get('p')
        #----------------------Check If a User Has Signed In-------------------------
        temp = self.request.cookies.get('user_id')
        login_necessary = 0
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                params['userid'] = userid
                user = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s'" %userid)
                user = user.get()
                params['chef_flag'] = user.ischef
            else:
                login_necessary = 1
        else:
            login_necessary = 1
        #----------------------------------------------------------------------------
        
        
        if login_necessary:
            params['return_url'] = './message_send'
            self.response.out.write(template.render('./html/login.html',params))
        else:
            params = {}            
            messg = escape_html(self.request.get('message'))
            message_title = escape_html(self.request.get('message_title'))
            success_flag = 1
            params['message_value'] = messg
            params['submitted'] = 0
            params['title_value'] = unescape_html(message_title)
        
            if not message_title:
                message_title = ""
                success_flag = 0
                params['error_title'] = 'Subject is necessary'
        
            if not messg: 
                messg = ""
                success_flag = 0
                params['error_message'] = 'Message should not be empty!'
                
            if not recepient_id:
                success_flag = 0
                params['error_chef'] = 'Invalid chef id!'
            if success_flag:

                b = Messages_DB(sender_id = userid,recepient_id = recepient_id,message_body = messg,created_date = datetime.now(),
                         message_title = message_title,read_status=0,message_parent = par)
                b.put()
                params['submitted'] = 1
                
            
            self.response.out.write(template.render('./html/message_send.html',params))
            