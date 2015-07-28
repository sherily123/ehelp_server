#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from utils import xinge
from database import db


class Add_Event_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    event_id = db.add_event(params)
    if event_id > 0:
      event_info = {}
      event_info[KEY.EVENT_ID] = event_id
      resp = db.get_event_information(event_info)
      if resp is None:
        resp = {}
      content = "something here" + ", LONGITUDE: %f, LATITUDE: %f"
      content = content%(resp[KEY.LONGITUDE], resp[KEY.LATITUDE])
      #print xinge.PushTokenAndroid(2100133741, '4f4ec6d90516dd970801835bf187dfed', 'New Event', content, 'ddf2cfba00f7f4fa42628a8d170829ee9d4ff476')
      #print xinge.PushAllAndroid(2100133741, '4f4ec6d90516dd970801835bf187dfed', 'New Event', content)
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

