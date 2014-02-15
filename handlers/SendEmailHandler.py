#=================INCLUDING THE NECESSARY LIBRARIES AND OTHER FILES==================
import webapp2
from google.appengine.api import memcache
from google.appengine.ext import db
from google.appengine.api import mail

import time
from dbs.databases import *
from utils import *
from google.appengine.ext.webapp import template
from datetime import date
import urllib
#====================================================================================


class MailDigestHandler(webapp2.RequestHandler):
    def get(self):
        users = db.GqlQuery("SELECT * FROM UserPass")        
        for user in users:          
            userid = str(user.user_id)  
            if (user.preferences == 'on'):                
                quotes = UserQuotes.gql("Where user = :1", userid)
                quote_list = list(quotes)
                if quote_list:                    
                    leng = len(quote_list)                
                    r = random.randrange(leng)
                    quote = quote_list[r]   
                    str0 = '<html> <head></head> <body>'
                    str1 = ' <table cellpadding="0" cellspacing="0" border="0">	<tbody><tr>	<td> <table cellpadding="0" cellspacing="0" border="0" align="center"> <tbody><tr> <td width="600" valign="top"><h3><span style="color:#888888">%s</span></h3> <p><span style="color:#999999">' %(quote.content.encode('utf-8'))
                    str2 = '%s</span></p><br><br><hr></td> </tr></tbody></table></td></tr></tbody></table> ' %str(quote.whosaid)
                    str3 = '</body></html>'
                    msg_content = str0 + str1 + str2 + str3
                    message = mail.EmailMessage(sender="Amir Hesam Salavati <saloot@gmail.com>",
                            subject="Daily Digest of Personal Quotes")
                    message.to = "%s" %str(user.user_email)
                    message.html = """%s""" %msg_content
                    
   
                    message.send()
                else:
                    self.response.out.write('Sorry!<br>')