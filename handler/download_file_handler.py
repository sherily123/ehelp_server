#!/usr/python

from tornado.web import RequestHandler
from tornado.escape import json_encode


from utils import utils
from utils import KEY
from utils import STATUS
from database import db

import os

class Download_File_Handler(RequestHandler):

  def get(self):
    # need to change to GET
    # need to judge whether there is a 'path' argument
    filepath = self.get_argument('path')
    filename = filepath.split('/')[-1]

    self.set_header('Content-Type', 'applicatioin/octet-stream')
    self.set_header('Content-Disposition', 'attachment; filename='+filename)

    with open(filepath, 'rb') as f:
      data = f.read()
      self.write(data)

    self.finish()



