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

  #POST
  new_url = "http://api.map.baidu.com/geodata/v3/poi/create"
  #POST
  update_url = "http://api.map.baidu.com/geodata/v3/poi/update"
  #GET
  search_url = "http://api.map.baidu.com/geodata/v3/poi/list?ak=%s&geotable_id=%d"

  # form a list of needed params
  values = {}
  if type == 0:
    geotable_id = user_table
    values[KEY.USER_ID] = data[KEY.ID]
    search_url += "&user_id=%d,%d"
    search_url = search_url%(ak, geotable_id, values[KEY.USER_ID], values[KEY.USER_ID]+1)
  elif type == 1:
    geotable_id = event_table
    values[KEY.EVENT_ID] = data[KEY.EVENT_ID]
    search_url += "&event_id=%d,%d"
    search_url = search_url%(ak, geotable_id, values[KEY.EVENT_ID], values[KEY.EVENT_ID]+1)
  values[KEY.AK] = ak
  values[KEY.LONGITUDE] = data[KEY.LONGITUDE]
  values[KEY.LATITUDE] = data[KEY.LATITUDE]
  values[KEY.COORD_TYPE] = 3
  values[KEY.GEOTABLE_ID] = geotable_id
  values[KEY.TITLE] = datetime.datetime.now()

  # search whether this event/user is existed.
  isExist = urllib.urlopen(search_url)
  existance = json.loads(isExist.read())
  
  # Yes, update loaction
  if existance['size'] > 0:
    values[KEY.ID] = existance['pois'][0]['id']
    data = urllib.urlencode(values)
    response = urllib.urlopen(update_url, data)
  # No, create location
  else:
    data = urllib.urlencode(values)
    response = urllib.urlopen(new_url, data)

  # turn string to json object, check if update successfully
  resp = json.loads(response.read())
  if resp['status'] == 0:
    print "From baidu LBS operation: Successfully update location, geotable: %d, id: %d"%(geotable_id, resp['id'])
    print values[KEY.LONGITUDE], values[KEY.LATITUDE]
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
  page_index = 0
  actual = 0
  url = "http://api.map.baidu.com/geosearch/v3/nearby?"
  suffix = "q=&location=%f,%f&radius=%d&ak=%s&geotable_id=%d&page_size=50&page_index=%d"
  user_id_list = []

  while True:
    if KEY.RADIUS in data:
      final_url = url + suffix%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.RADIUS], ak, user_table, page_index)
    else:
      final_url = url + suffix%(data[KEY.LONGITUDE], data[KEY.LATITUDE], 10000, ak, user_table, page_index)
  
    req = urllib2.Request(final_url)
    response = urllib2.urlopen(req)
    resp = json.loads(response.read())
    print "From baidu LBS Cloud - get user location: status - ", resp['status']
    print resp

    # get location array from response
    contents = resp['contents']
    size = resp['size']
    actual += size
    total = resp['total']
    # get user_id from contents
    for each_loc in contents:
      if KEY.USER_ID in each_loc:
        user_id_list.append(each_loc[KEY.USER_ID])
    if size != 0 and actual < total:
      page_index += 1
    else:
      break

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
  page_index = 0
  url = "http://api.map.baidu.com/geosearch/v3/nearby?q=&location=%f,%f&radius=%d&ak=%s&geotable_id=%d&page_size=50&page_index=%d"
  actual = 0
  event_id_list = []

  while True:
    final_url = url%(data[KEY.LONGITUDE], data[KEY.LATITUDE], 1000000, ak, event_table, page_index)
    req = urllib2.Request(final_url)
    response = urllib2.urlopen(req)
    resp = json.loads(response.read())

    # get location array from response
    contents = resp['contents']
    size = resp['size']
    actual += size
    total = resp['total']
    # get event_id from contents
    for each_loc in contents:
      if KEY.EVENT_ID in each_loc:
        event_id_list.append(each_loc[KEY.EVENT_ID])

    if size != 0 and actual < total:
      page_index += 1
      print "page_index = %d, actual total = %d"%(page_index, actual)
    else:
      break

  print "From baidu LBS operation: near event id list:"
  print event_id_list

  return event_id_list



