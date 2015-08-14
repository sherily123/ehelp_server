#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db


class User_Get_Evaluate_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)

    resp = {}
    evaluate = db.get_user_evaluate(params)
    if evaluate is None:
      resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.VALUE] = evaluate[KEY.VALUE]
      resp[KEY.COMMENT] = evaluate[KEY.COMMENT]
      resp[KEY.STATUS] = STATUS.OK

    self.write(json_encode(resp))


