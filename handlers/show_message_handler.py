#=================================FUNCTION DESCRITION================================
# This code is responsible for displaying a particular meal. It reads the meal ID
# from the url, retrieves the meal from the dataset and if found, displays its
# detaiLs.
#====================================================================================


#=================INCLUDING THE NECESSARY LIBRARIES AND OTHER FILES==================
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
import time

from dbs.databases import *
from utils import *
from google.appengine.ext.webapp import template
from datetime import date
from datetime import datetime
#====================================================================================

#===================================THE MAIN CODE====================================
class ShowMessageHandler(webapp2.RequestHandler):

    def get(self):
        message_key = self.request.get('k')
        message_active = self.request.get('r')
        params = {}
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
            params['return_url'] = './_msg?k='+message_key
            self.response.out.write(template.render('./html/login.html',params))
            
        else:
            msg = db.get(message_key) 
            msseg = []
    
            
            messages = []
            msgg = []
            msgg.append(unescape_html(msg.message_body))
            if msg.sender_id == userid:
                msgg.append('You')
            else:
                msgg.append(msg.sender_id)
            msseg_date = msg.created_date
            msseg_date = msseg_date.replace(microsecond=0)
            msseg_date = str(msseg_date.replace(second=0))
            msseg_date = msseg_date[0:16]
            
            msgg.append(msseg_date)
            messages.append(msgg)
            parnt = msg.message_parent
            if parnt:
                end_flag = 0
                while end_flag == 0:
                    msgg = []
                    old_msg = db.get(parnt)
                    parnt = old_msg.message_parent
                    if old_msg:
                        msgg.append(unescape_html(old_msg.message_body))
                        if old_msg.sender_id == userid:
                            msgg.append('You')
                        else:
                            msgg.append(old_msg.sender_id)
                        
                        
                        msseg_date = old_msg.created_date
                        msseg_date = msseg_date.replace(microsecond=0)
                        msseg_date = str(msseg_date.replace(second=0))
                        msseg_date = msseg_date[0:16]
                        msgg.append(msseg_date)
                        
                        messages.append(msgg)
                    else:
                        end_flag = 1
                    if not parnt:
                        end_flag = 1
                    
            
            msseg.append(unescape_html(msg.message_title))
            if userid == msg.sender_id:
                msseg.append(msg.recepient_id)
            else:
                msseg.append(msg.sender_id)
            msseg.append(int(msg.read_status))
            
            
            
            if not message_active:
                message_active = 0;
        
            params['message_active'] = int(message_active)
            params['key'] = message_key
            params['message'] = msseg
            params['messages'] = messages
            
            
            if msg:
                if msg.recepient_id == userid:
                    msg.read_status = 1
                    msg.put()
            self.response.out.write(template.render('./html/display_message.html',params))


    
    def post(self):
        params = {}        
        message_key = self.request.get('k')
        
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
            params['return_url'] = './_msg?k=' + message_key
            self.response.out.write(template.render('./html/login.html',params))
        else:
            params = {}            
            reply_body = escape_html(self.request.get('reply_message'))
            message_title = escape_html(self.request.get('reply_title'))
            recepient_id = self.request.get('recepient')
            success_flag = 1
            
            if not message_title:
                message_title = ""
                success_flag = 0
                params['error_title'] = 'Subject is necessary'
        
            if not reply_body: 
                messg = ""
                success_flag = 0
                params['error_message'] = 'Message should not be empty!'
                
            if not recepient_id:
                success_flag = 0
                params['error_recpient'] = 'Invalid recpient id!'
                
            if success_flag:
                b = Messages_DB(sender_id = userid,recepient_id = recepient_id,message_body = reply_body,created_date = datetime.now(),
                         message_title = message_title,read_status=0,message_parent = message_key,new_conversation = 1)
                b.put()
                
                new_key =b.key();
                msg = db.get(message_key)                 
                end_flag = 0
                while end_flag == 0:
                    parnt = msg.message_parent
                    msg.new_conversation = 0
                    msg.put()
                    if not parnt:
                        end_flag = 1
                    else:
                        msg = db.get(parnt)
                
                params['message_active'] = 0
                self.redirect('./_msg?k=%s'%b.key())
            else:
                self.response.out.write(template.render('./html/display_message.html',params))
            
        