#!/usr/python
from tornado.escape import json_decode
import datetime


def decode_params(request):
  params = {}
  try:
    head = request.headers.get("Content-Type")
    headers = head.split(";")
    i = datetime.datetime.now()
    if headers[0] == "application/json":
      params = json_decode(request.body)
      print ("%s, valid json request" % i)
    else:
      print ("%s, invalid json request" % i)
  except:
    pass
  finally:
    return params


