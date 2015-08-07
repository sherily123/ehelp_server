#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from utils import baidulbs
from database import db


class Update_Event_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    result = db.update_event(params)
    if KEY.LONGITUDE in params and KEY.LATITUDE in params:
      baiduResult = baidulbs.update_location(params, KEY.EVENT)
    if KEY.EVENT_ID in params:
      resp[KEY.EVENT_ID] = params[KEY.EVENT_ID]
    if result:     
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR
    
    self.write(json_encode(resp))

    

