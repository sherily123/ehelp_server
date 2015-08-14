#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db

import os

class Upload_File_Handler(RequestHandler):
  def post(self):
    resp = {}
    flag = True

    print
    print
    print
    #print self.request.header
    print
    print
    print
    print

    # Check if there is an operation type
    ####################if self.get_argument(KEY.TYPE):
    if int(self.request.headers[KEY.TYPE]) == 0:
      upload_path = 'static/test/audio/' + self.request.headers[KEY.ID]
    elif int(self.request.headers[KEY.TYPE]) == 1:
      upload_path = 'static/test/video/' + self.request.headers[KEY.ID]
    elif int(self.request.headers[KEY.TYPE]) == 2:
      upload_path = 'static/test/pic/' + self.request.headers[KEY.ID]
    else:
      flag = False

    # upload a file
    if flag:
      # Check if directory exists, if not create it
      if not os.path.exists(upload_path):
        os.makedirs(upload_path)

      if 'file' in self.request.files:
        # get a list of files
        file_metas = self.request.files['file']
        # save files in request
        for meta in file_metas:
          filename = meta['filename']
          filepath = os.path.join(upload_path, filename)
          with open(filepath, 'wb') as up:
            up.write(meta['body'])

        if os.path.isfile(filepath):
          resp[KEY.STATUS] = STATUS.OK
          resp[KEY.ID] = int(self.request.headers[KEY.ID])
          resp[KEY.FILEPATH] = filepath
        else:
          resp[KEY.STATUS] = STATUS.ERROR
          print "Error from upload file handler: files not saved"
      else:
        resp[KEY.STATUS] = STATUS.ERROR
        print "Error from upload file handler: 'file' not in request", self.request.files

    else:
      resp[KEY.STATUS] = STATUS.ERROR
      print "Error from upload file handler: no operation type."


    self.write(json_encode(resp))



