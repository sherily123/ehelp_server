#!/usr/python

# baidulbs.py #
# baidu LBS Cloud operation #
# Coded by Zeng Xiaoli, Aug.2015 #

import json
import KEY
import STATUS
import utils

import datetime
import urllib
import urllib2

# Baidu LBS Cloud APP KEY
ak = 'U9gBhjb8y58UEjWok8qzD5rG'
# event location table id
event_table = 116165
# user location table id
user_table = 116164


'''
update location in Baidu LBS Cloud.
@params includes longitude and latitude, content type.
                 content type includes 2 types:
                 0: user's location
                 1: event's location
@return True if successfully updated.
        False otherwise
'''
def update_location(data, type):
  if KEY.LONGITUDE not in data or KEY.LATITUDE not in data:
    return False
  if type > 1 or type < 0:
    return False
  if type == 0 and KEY.ID not in data:
    return False
  if type == 1 and KEY.EVENT_ID not in data:
    return False

  new_url = "http://api.map.baidu.com/geodata/v3/poi/create"
  update_url = "http://api.map.baidu.com/geodata/v3/poi/update"

  # form a list of needed params
  values = {}
  if type == 0:
    geotable_id = user_table
    values[KEY.USER_ID] = data[KEY.ID]
  elif type == 1:
    geotable_id = event_table
    values[KEY.EVENT_ID] = data[KEY.EVENT_ID]
  values[KEY.AK] = ak
  values[KEY.LONGITUDE] = data[KEY.LONGITUDE]
  values[KEY.LATITUDE] = data[KEY.LATITUDE]
  values[KEY.COORD_TYPE] = 3
  values[KEY.GEOTABLE_ID] = geotable_id
  values[KEY.TITLE] = datetime.datetime.now()

  # send params to Baidu LBS Cloud and get a response
  data = urllib.urlencode(values)
  response = urllib2.urlopen(url, data)

  # turn string to json object, check if update successfully
  resp = json.loads(response.read())
  if resp['status'] == 0:
    print "From baidu LBS operation: Successfully update location, geotable: %d, id: %d"%(geotable_id, resp['id'])
    return True
  else:
    print "From baidu LBS operation: Failed, return code: %d"%resp['status']
    return False


'''
get a near user id list from Baidu LBS Cloud.
@params includes event's location.
@return a list of near user id.
        None means failed.
'''
def get_user_location(data):
  if KEY.LONGITUDE not in data or KEY.LATITUDE not in data:
    return None

  # use location info in data to search near user in Cloud table 'user location'
  # send GET request to Cloud
  url = "http://api.map.baidu.com/geosearch/v3/nearby?"
  suffix = "q=&location=%f,%f&radius=%d&ak=%s&geotable_id=%d"
  if KEY.RADIUS in data:
    suffix = suffix%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.RADIUS], ak, user_table)
  else:
    suffix = suffix%(data[KEY.LONGITUDE], data[KEY.LATITUDE], 500, ak, user_table)
  url += suffix
  
  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  data = json.loads(response.read())
  print "From baidu LBS Cloud - get user location: status - %d"%(int(data['status']))

  if 'contents' in data:
    # get location array from response
    contents = data['contents']
    # get user_id from contents
    user_id_list = []
    for each_loc in contents:
      if KEY.USER_ID in each_loc:
        user_id_list.append(each_loc[KEY.USER_ID])
  print "From baidu LBS operation: near user id list:"
  print user_id_list
  return user_id_list


'''
get a near event id list from Baidu LBS Cloud.
@params includes user's location.
@return a list of near 500 meters event id.
        None means failed.
'''
def get_event_location(data):
  if KEY.LONGITUDE not in data or KEY.LATITUDE not in data:
    return None

  # use location info in data to search near events in Cloud table 'event location'
  # send GET request to Cloud
  url = "http://api.map.baidu.com/geosearch/v3/nearby?"
  suffix = "q=&location=%f,%f&radius=%d&ak=%s&geotable_id=%d"
  url += suffix%(data[KEY.LONGITUDE], data[KEY.LATITUDE], 500, ak, event_table)

  req = urllib2.Request(url)
  response = urllib2.urlopen(req)
  data = json.loads(response.read())

  # get location array from response
  contents = data['contents']
  # get event_id from contents
  event_id_list = []
  for each_loc in contents:
    if KEY.EVENT_ID in each_loc:
      event_id_list.append(each_loc[KEY.EVENT_ID])
  print "From baidu LBS operation: near event id list:"
  print event_id_list

  return event_id_list



