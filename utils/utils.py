#!/usr/python
from tornado.escape import json_decode



def decode_params(request):
  params = {}
  try:
    head = request.headers.get("Content-Type")
    headers = head.split(";")
    if headers[0] == "application/json":
      params = json_decode(request.body)
      print request.headers.get("Content-Type") + ", this is a json post request"
    else:
      print request.headers.get("Content-Type") + ", invalid json request"
  except:
    pass
  finally:
    return params


