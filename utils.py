import random
import string
import hashlib
import datetime
import time
import Cookie
import json
import urllib2
import urllib

import re

SECRET = "soghrat"
home_site = "http://madeatmyhome.appspot.com"
#home_site = "http://localhost:8083"
COOKIE_RE = re.compile(r'.+=;\s+Path=/')
def valid_cookie(cookie):
    return cookie and COOKIE_RE.match(cookie)
    

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
Address_RE = re.compile(r"^.{3,200}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
PHONE_RE = re.compile(r"^[0-9]{10,16}$")

def valid_name(username):
    return USER_RE.match(username)

def valid_address(user_address):
    return Address_RE.match(user_address)

def valid_pass(password):
    return PASSWORD_RE.match(password)

def valid_email(email):
    return EMAIL_RE.match(email)

def valid_phone(phone):
    return PHONE_RE.match(phone)

          
def escape_html(s):
    s = s.replace('&',"&amp;")
    s = s.replace(">","&gt;")     
    s = s.replace("<","&lt;")
    s = s.replace('"',"&quot;")
    s = s.replace('%20',"&nbsp")
    s = s.replace('&#xA0',"&nbsp")
    s = s.replace(' ',"&nbsp")
    return s

def unescape_html(s):
    s = s.replace("&amp;",'&')
    s = s.replace("&gt;",">")
    s = s.replace("&lt;","<")
    s = s.replace("&quot;",'"')
    s = s.replace("&nbsp",' ')
    s = s.replace("&nbsp",'&#xA0')
    return s    




def print_json(self,blog_post):
    time_str = time.strftime("%a %b %d %H:%M:%S %Y", 
                time.gmtime(time.mktime(time.strptime(blog_post.created_date.strftime("%Y-%m-%d %H:%M:%S"), 
                                                    "%Y-%m-%d %H:%M:%S"))))
    post_dictionary = {}
    
    post_dictionary['content'] = blog_post.content  
    post_dictionary['subject'] = blog_post.title  
    post_dictionary['created'] = time_str  
    
    return post_dictionary


def make_salt():
    output = []
    for i in range(0,5):
        output.append(random.choice(string.letters))
    return(string.join(output,""))


def valid_hash_cookie(h):        
    temp = h.split('|',3)
    hashed_val = temp[0]
    user = temp[1]    
    if (hashed_val == hashlib.sha256(user+SECRET).hexdigest()):
        return user
    else:
        return ""


def make_hashed_pw(name, pw):
    salt = make_salt()
    return hashlib.sha256(name + pw + salt).hexdigest() + '|' + salt

def make_hashed_cookie(username):    
    return hashlib.sha256(str(username)+SECRET).hexdigest() + '|' + str(username)


def valid_hash_pw(name, pw, h):        
    temp = h.split('|',3)
    hashed_val = temp[0]
    salt = temp[1]    
    if (hashed_val == hashlib.sha256(name + pw + salt).hexdigest()):
        return hashed_val
    else:
        return hashed_val

def print_json(self,blog_post):
    self.response.out.write("{")
    self.response.out.write("\"content\": \"")
    self.response.out.write(blog_post.content)
    self.response.out.write("\",")

    self.response.out.write("\"created\": \"")
        
    time_str = time.strftime("%a %b %d %H:%M:%S %Y", 
          time.gmtime(time.mktime(time.strptime(blog_post.created_date.strftime("%Y-%m-%d %H:%M:%S"), 
                                                    "%Y-%m-%d %H:%M:%S"))))
    self.response.out.write(time_str)
    self.response.out.write("\",")
        
    self.response.out.write("\"subject\": \"")
    self.response.out.write(blog_post.title)
    self.response.out.write("\"")
    self.response.out.write("}")


def get_geolocation(postal_address):
    
    if postal_address:
        postal_address2 = urllib.quote_plus(postal_address)
        url_geo = "http://maps.googleapis.com/maps/api/geocode/json?address=%s&sensor=false" % postal_address2
        try:
            geo_content = urllib2.urlopen(url_geo).read()
        except URLError:
            return            
        if geo_content:
            q = json.loads(geo_content)
            if q['status'] == 'OK':
                lat = str(q['results'][0]['geometry']['location']['lat'])
                lng = str(q['results'][0]['geometry']['location']['lng'])
            else:
                return q['status'] 
                     
    return q['status'] 

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false"

def gmaps_img(point):    
    temp = ""
    if point:
        temp = temp + '&markers=%s,%s' %(point.lat,point.lon)
    return temp

def remove_duplicate(input_list):
    output_list = []
    for item in input_list:
        if item.lower() not in output_list:
            output_list.append(item.lower())
            
    return output_list        
    
