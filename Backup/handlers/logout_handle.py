import webapp2
from utils import *

class LogoutHandler(webapp2.RequestHandler):    
    def get(self):        
        hashed_val = make_hashed_cookie("")
        cookie=str('user_id='';Path=/;expires=-1')
        self.response.headers.add_header('Set-Cookie',cookie)  
        self.redirect('/login')  
