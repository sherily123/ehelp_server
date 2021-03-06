#!/usr/python

from tornado.escape import json_decode

import datetime
import xinge
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

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


'''
push message to devices.
@params includes message title, content, operation type, token is optional.
                 operation type as below:
                 0: send to all devices
                 1: sent to a device with specific token
@return True if push messages successfully.
        False otherwise.
'''
def push_message(title, content, event_id, op, token_list, activity='com.example.Near.NearActivity'):
  
  # Construct a Xinge app
  x = xinge.XingeApp(2100133741, '4f4ec6d90516dd970801835bf187dfed')
  # Construct a notification
  msg = xinge.Message()
  msg.type = xinge.Message.TYPE_NOTIFICATION
  # notification content
  msg.title = title
  content.encode('utf-8')
  msg.content = content
  # custom key-value, here is event_id
  msg.custom = {'event_id' : str(event_id)}
  # notification style on devices
  style = xinge.Style()
  style.builderId = 2
  style.ring = 1
  style.vibrate = 1
  msg.style = style
  # click action setting, only for notification
  action = xinge.ClickAction()
  action.actionType = xinge.ClickAction.TYPE_ACTIVITY
  action.activity = activity
  msg.action = action

  # PUSH MESSAGE TO A LIST OF TOKEN!!!!
  # status to get return value of pushing message
  status = {}
  if op == 0:
    #status = x.PushAllDevices(0, msg)
    ret = x.CreateMultipush(msg)
    if ret[0] == 0:
      #print "From push message function:"
      #print ret
      #print "From push message function: Successfully create a push id: %d"%int(ret[2])
      #print "From push message function: Successfully receive a token list:"
      #print token_list
      push_id = int(ret[2])
      status = x.PushDeviceListMultiple(push_id, token_list)
  elif op == 1:
    if token == '':
      return False
    status = x.PushSingleDevice(token, msg)

  if status != {}:
    print "From push message function:"
    print status
    if status[0] == 0:
      return True
    else:
      return False
  else:
    return False




