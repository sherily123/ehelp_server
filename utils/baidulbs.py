#!/usr/python

from tornado.escape import json_decode

import 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



'''
update location in Baidu LBS Cloud.
@params includes longitude and latitude, content type.
                 content type includes 2 types:
                 0: user's location
                 1: event's location
@return True if successfully updated.
        False otherwise
'''
def update_location(data, type):
  return False


'''
get a near user id list from Baidu LBS Cloud.
@params includes event's location.
@return a list of near user id.
        None means failed.
'''
def get_user_location(data):
  return None;


'''
get a near event id list from Baidu LBS Cloud.
@params includes user's location.
@return a list of near event id.
        None means failed.
'''
def get_event_location(data):
  return None
