#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class Get_All_Events_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    resp[KEY.EVENT_LIST] = db.get_events(params, db.get_all_event_list)
    # why increase 1 here???
    for each_event in resp[KEY.EVENT_LIST]:
      each_event[KEY.EVENT_ID] += 1
      if each_event[KEY.EVENT_ID] == 500:
        print each_event
    resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))



