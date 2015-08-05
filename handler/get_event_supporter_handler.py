#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from utils import utils
from utils import KEY
from utils import STATUS
from database import db

class Get_Event_Supporter_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    resp[KEY.USER_ACCOUNT] = db.get_event_supporter(params)
    resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))
