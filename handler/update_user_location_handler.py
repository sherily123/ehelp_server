#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from utils import baidulbs
from database import db


class Update_User_Location_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    result = db.update_location(params)
    baiduResult = baidulbs.update_location(params, KEY.USER)
    if result and baiduResult:
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp[KEY.STATUS] = STATUS.ERROR

    self.write(json_encode(resp))

