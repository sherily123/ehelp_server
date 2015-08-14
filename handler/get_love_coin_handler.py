#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode

from utils import utils
from utils import KEY
from utils import STATUS
from database import db

class Get_Love_Coin_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    resp[KEY.LOVE_COIN] = db.get_love_coin(params)
    if resp[KEY.LOVE_COIN] != -1:
      resp[KEY.STATUS] = STATUS.OK
    else:
      resp = {}
      resp[KEY.STATUS] = STATUS.ERROR

    print 
    print resp
    print 
    self.write(json_encode(resp))



