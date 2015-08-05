#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
#from utils import baidulbs
from database import db

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Add_Event_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    event_id = db.add_event(params)
    print "From add_event_handler: event id: %d"%event_id
    if event_id > 0:
      # update location in Baidu LBS Cloud
      #baiduResult = baidulbs.update_location(params, KEY.EVENT)
      event_info = {}
      event_info[KEY.EVENT_ID] = event_id
      resp = db.get_event_information(event_info)
      if resp is None:
        resp = {}
      else:
        print resp
        # get a near users' id list of current event
        #near_list = []
        #near_list = baidulbs.get_user_location(params)
        # get correspond push_token to user id
        #token_list = db.get_push_token(near_list)

        #if resp[KEY.TYPE] == 1:
        #  title = "New Help"
        #  activity = ""
        #elif resp[KEY.TYPE] == 2:
        #  title = "New SOS"
        #  activity = ""
        #content = resp[KEY.CONTENT]
        # push to those user
        #utils.push_message(title, content, KEY.SENDALL, token_list)
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

