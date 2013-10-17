import webapp2
from google.appengine.ext import db
from dbs.databases import *
from time import gmtime, strftime
from collections import namedtuple
from utils import *

GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false"

class DisplayMapHandler(webapp2.RequestHandler):    
    def get(self): 
        style_css = "<html> <style> .map_static{ position:absolute; right:100; top = 1512 px;  }   </style>"
        Point = namedtuple('Point', ["lat", "lon"])          
        coords_url_maps = GMAPS_URL
        coords = db.GqlQuery("SELECT * FROM UserPass")
        for c in coords:
            if c.user_latitude:
                p = namedtuple('Point', ["lat", "lon"])          
                Point.lat = c.user_latitude
                Point.lon = c.user_longitude            
                coords_url_maps = coords_url_maps + gmaps_img(Point)
    
        if (coords_url_maps):
            self.response.out.write(style_css)
            self.response.out.write("<img class= \"map_static\" src = %s>" %coords_url_maps)
