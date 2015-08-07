#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from utils import baidulbs
from database import db


class Get_All_Events_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    user_loc = db.get_user_current_location(params)
    print "From get all event handler: user location:"
    print user_loc
    print
    # search near event list and get their event_ids
    event_list = baidulbs.get_event_location(user_loc)
    data = {}
    data.update(params)
    data[KEY.EVENT_LIST] = event_list
    # if there are event_ids, then get their information
    resp[KEY.EVENT_LIST] = db.get_events(data, db.get_all_event_list)

    # why increase 1 here???
    #for each_event in resp[KEY.EVENT_LIST]:
    #  each_event[KEY.EVENT_ID] += 1
    # get current user location

    resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))



