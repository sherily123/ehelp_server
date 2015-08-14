#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db

import os, base64

class Upload_Avatar_Handler(RequestHandler):
  def post(self):
    params = utils.decode_params(self.request)
    
    resp = {}
    # upload an avatar
    if params[KEY.OPERATION] == 0:
      if KEY.AVATAR in params:
        # save an avatar to directory
        filepath = 'static/avatar/' + str(params[KEY.ID]) + '.jpg'
        f = open(filepath, 'wb')
        imgdata = base64.b64decode(params[KEY.AVATAR])
        f.write(imgdata)
        f.close()
        if os.path.isfile(filepath):
          params['filepath'] = filepath
          result = db.update_db_avatar(params)
          resp[KEY.STATUS] = STATUS.OK
          resp[KEY.ID] = params[KEY.ID]
        else:
          resp[KEY.STATUS] = STATUS.ERROR
      else:
        resp[KEY.STATUS] = STATUS.ERROR

    # download an avatar
    elif params[KEY.OPERATION] == 1:
      # get file path of the avatar
      filepath = db.get_db_avatar(params)
      if os.path.isfile(filepath):
        # read the avatar file
        f = open(filepath, 'rb')
        # encode to base64 string
        imgdata = base64.b64encode(f.read())
        f.close()
        resp[KEY.ID] = params[KEY.ID]
        resp[KEY.STATUS] = STATUS.OK
        resp[KEY.AVATAR] = imgdata
      else:
        resp[KEY.STATUS] = STATUS.ERROR
    else:
      resp[KEY.STATUS] = STATUS.ERROR
      
    
    self.write(json_encode(resp))

    


