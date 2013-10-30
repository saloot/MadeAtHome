import webapp2
from utils import valid_hash_cookie
from google.appengine.ext.webapp import template
from google.appengine.ext import db

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        temp = self.request.cookies.get('user_id')
        if temp:
            userid = valid_hash_cookie(temp)
            if userid:
                dashboard_params = {}
                
                d = db.GqlQuery("SELECT * FROM UserPass_User WHERE user_id = '%s' " % userid)
                l = d.get()
                if l:
                    if (l.ischef):
                        chef_flag = 1
                    else:
                        chef_flag = 0
                else:
                    self.display.out.write('Error! No username!')
                    
                dashboard_params['userid'] = userid
                dashboard_params['chef_flag'] = chef_flag
                self.response.out.write(template.render('./html/user_dashboard.html',dashboard_params))
                
                self.response.out.write('<h2> Welcome <b> %s </b> </h2>' %userid)
                self.response.out.write('<br>')
                self.response.out.write('<br>')
                self.response.out.write('<h3>Are you in the mood to <a href= "/newpost"> post a new blog?<a></h3>')
                self.response.out.write('<br>')
                self.response.out.write('<br>')   
                self.response.out.write('<br>')
                self.response.out.write('<br>')
                self.response.out.write('<br>')
                self.response.out.write('<br>')   
                self.response.out.write('<br>')
                self.response.out.write('<br>')                                                
                self.response.out.write('If your are not <b> %s </b> click <a href= "/logout"> here<a>' %userid)
            else:
                self.response.out.write('Cheater!')
        else:
            self.redirect('/login')
