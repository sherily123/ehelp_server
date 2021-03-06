#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_Single_Events_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    resp = db.get_event_information(params)
    if resp is None:
      print "resp is None"
      resp = {}
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))
