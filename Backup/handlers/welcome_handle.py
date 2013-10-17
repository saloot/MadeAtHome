import webapp2
from utils import valid_hash_cookie
from google.appengine.ext.webapp import template

class WelcomeHandler(webapp2.RequestHandler):
    def get(self):
        cu_param = self.request.get('u')
        
        if (cu_param == 'chef'):
            temp = self.request.cookies.get('user_id')
            if temp:
                userid = valid_hash_cookie(temp)
                if userid:
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
        elif (cu_param == 'user'):
            temp = self.request.cookies.get('user_id')
            params = {}
            if temp:
                userid = valid_hash_cookie(temp)
                if userid:
                    params['userid'] = userid 
                    self.response.out.write(template.render('./html/welcome_page_user.html',params))
                else:
                    self.response.out.write('Cheater!')
            else:
                self.redirect('/login')
        else:
            self.redirect('/404')