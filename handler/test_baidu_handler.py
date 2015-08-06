#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from utils import baidulbs
from database import db


class Test_Baidu_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    result = baidulbs.get_user_location(params)
    if result is None:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))

