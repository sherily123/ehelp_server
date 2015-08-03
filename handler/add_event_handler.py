#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db

import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Add_Event_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    event_id = db.add_event(params)
    print "event id: %d"%event_id
    if event_id > 0:
      event_info = {}
      event_info[KEY.EVENT_ID] = event_id
      resp = db.get_event_information(event_info)
      if resp is None:
        resp = {}
      else:
        print resp
        if resp[KEY.TYPE] == 0:
          title = "New Question"
          activity = ""
        elif resp[KEY.TYPE] == 1:
          title = "New Help"
          activity = ""
        elif resp[KEY.TYPE] == 2:
          title = "New SOS"
          activity = ""
        content = resp[KEY.CONTENT]
        utils.push_message(title, content, KEY.SENDALL)
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

