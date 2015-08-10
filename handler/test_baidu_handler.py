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

    result = baidulbs.update_location(params, KEY.EVENT)
    resp = {}
    resp[KEY.STATUS] = STATUS.OK
    self.write(json_encode(resp))

'''
    # get current user location
    user_loc = db.get_user_current_location(params)
    # search near event list and get their event_ids
    event_list = baidulbs.get_event_location(user_loc)
    data = {}
    data.update(params)
    data[KEY.EVENT_LIST] = event_list
    print "From test baidu handler: data to database is below:"
    print data
    print
    # if there are event_ids, then get their information
    resp = {}
    resp[KEY.EVENT_LIST] = db.get_events(data, db.get_all_event_list)
    resp[KEY.STATUS] = STATUS.OK
'''


