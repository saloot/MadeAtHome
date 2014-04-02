#=================================FUNCTION DESCRITION================================
# This code is responsible for displaying the chefs' profiles, namely, all the food
# they offer, their favourite recipes, their rating, etc.
#====================================================================================


#=================INCLUDING THE NECESSARY LIBRARIES AND OTHER FILES==================
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from dbs.databases import *
from utils import *
import time
#====================================================================================


#===================================THE MAIN CODE====================================
class MessageInboxHandler(webapp2.RequestHandler):
    
    #---------------------Display the HTML Template Upon Loading---------------------    
    def get(self):
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
            params['return_url'] = './message_inbox'
            self.response.out.write(template.render('./html/login.html',params))
    
        #--------------------------If the USER ID Is Correct-------------------------
        else:            

            #--------------------Find the Messages for this user---------------------
            messages = db.GqlQuery("SELECT * FROM Messages_DB WHERE recepient_id = '%s'" %userid)            
            message_list = []
            
            if messages:                
                for message in messages:
                    if message.new_conversation:
                        message_specifications = []
                    
                        message_specifications.append(unescape_html(message.message_title))
                        m_body = unescape_html(message.message_body)
                        if (len(m_body) > 50):
                            m_body = m_body[0:50]
                            m_body = m_body + '...'
                        message_specifications.append(m_body)
                        message_specifications.append((message.sender_id))
                        message_specifications.append(int(message.read_status))
                        message_specifications.append((message.message_parent))
                        message_specifications.append((message.created_date))
                        message_specifications.append((message.key()))
                    
                        message_list.append(message_specifications)
                        
            messages = db.GqlQuery("SELECT * FROM Messages_DB WHERE sender_id = '%s'" %userid)            
            
            if messages:                
                for message in messages:
                    if message.new_conversation and message.message_parent:
                        message_specifications = []
                    
                        message_specifications.append(unescape_html(message.message_title))
                        m_body = unescape_html(message.message_body)
                        if (len(m_body) > 50):
                            m_body = m_body[0:50]
                            m_body = m_body + '...'
                        message_specifications.append(m_body)
                        message_specifications.append((message.recepient_id))
                        message_specifications.append(int(1))
                        message_specifications.append((message.message_parent))
                        message_specifications.append((message.created_date))
                        message_specifications.append((message.key()))
                    
                        message_list.append(message_specifications)
            #------------------------------------------------------------------------
            
            #-------------------Assign the HTML Template Parameters------------------
            params['message_list'] = message_list             
            #------------------------------------------------------------------------
            
            #----------------------Display the Final HTML File-----------------------
            self.response.out.write(template.render('./html/message_inbox.html',params))
            #------------------------------------------------------------------------
        
        #----------------------------------------------------------------------------        
            
        
    #--------------------------------------------------------------------------------

#====================================================================================