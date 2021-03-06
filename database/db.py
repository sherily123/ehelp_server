#!/usr/python

# db.py #
# database operation #
# Coded by William Deng & Zeng Xiaoli, Aug.2015 #

import sys
import random
import string
import hashlib
import MySQLdb
import ast


from dbhelper import dbhelper
from  utils import KEY



'''
add a new account to database.
@params a dict data:
        includes account and password.
@return -1 indicates params are not complete. Or account is not unique that leads to database fails.
        other number indicates success and the number is the id of the new account.
'''
def add_account(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data or KEY.NAME not in data or KEY.NICKNAME not in data:
    return -1
  salt = ''.join(random.sample(string.ascii_letters, 8))
  md5_encode = hashlib.md5()
  md5_encode.update(data[KEY.PASSWORD]+salt)
  password = md5_encode.hexdigest()
  sql_account = "insert into account (account, password, salt, nickname, name) values (%d, '%s', '%s', '%s', '%s')"
  sql_user = "insert into user (id, name, nickname, phone) values (%d, '%s', '%s', %d)"
  try:
    insert_id = dbhelper.insert(sql_account%(data[KEY.ACCOUNT], password, salt, data[KEY.NICKNAME], data[KEY.NAME]))
    dbhelper.insert(sql_user%(insert_id, data[KEY.NAME], data[KEY.NICKNAME], data[KEY.ACCOUNT]))
    return insert_id
  except:
    return -1


'''
update information of an account.
@params a dict data:
        includes id and chat_token:
@return True if successfully modify chat_token
        False modification fails.
'''
def update_account(data):
  if KEY.ID in data and KEY.CHAT_TOKEN in data:
    sql = "update account set chat_token = '%s' where id = %d"
    try:
      if dbhelper.execute(sql%(data[KEY.CHAT_TOKEN], data[KEY.ID])) > 0:
        return True
    except:
      return False
  else:
    return False


'''
modify user's information.
@params a dict data:
        options include user's name, nickname, gender, age, phone, location,
        (longitude and latitude), occupation, identity_id.
@return True if successfully modify
        False modification fails.
'''
def update_user(data):
  if KEY.ID not in data:
    return False
  result = True
  
  sql = ""
  if KEY.NAME in data:
    data[KEY.NAME] = MySQLdb.escape_string(data[KEY.NAME].encode("utf8"))
    sql = "update user set name = '%s' where id = %d"
    account_sql = "update account set name = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.NAME], data[KEY.ID]))
      dbhelper.execute(account_sql%(data[KEY.NAME], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.NICKNAME in data:
    data[KEY.NICKNAME] = MySQLdb.escape_string(data[KEY.NICKNAME].encode("utf8"))
    sql = "update user set nickname = '%s' where id = %d"
    account_sql = "update account set nickname = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.NICKNAME], data[KEY.ID]))
      dbhelper.execute(account_sql%(data[KEY.NICKNAME], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.GENDER in data:
    sql = "update user set gender = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.GENDER], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.AGE in data:
    sql = "update user set age = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.AGE], data[KEY.ID]))
      result &= True
    except:
      result &= False
   
  if KEY.PHONE in data:
    sql = "update user set phone = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.PHONE], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.LOCATION in data:
    data[KEY.LOCATION] = MySQLdb.escape_string(data[KEY.LOCATION].encode("utf8"))
    sql = "update user set location = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LOCATION], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.LONGITUDE in data and KEY.LATITUDE in data:
    sql = "update user set longitude = %f, latitude = %f where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.ID]))
      result &= True
    except:
      result &= False
  elif not (KEY.LONGITUDE not in data and KEY.LATITUDE not in data):
    result &= False

  if KEY.OCCUPATION in data:
    sql = "update user set occupation = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.OCCUPATION], data[KEY.ID]))
      result &= True
    except:
      result &= False

  if KEY.IDENTITY_ID in data:
    sql = "update user set identity_id = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.IDENTITY_ID], data[KEY.ID]))
      result &= True
    except:
      result &= False

  return result


'''
get salt of an account.
@params include user's account.
@return salt of an account.
  None if account not exists or database query error.
'''
def get_salt(data):
  if KEY.ACCOUNT not in data:
    return None
  sql = "select salt from account where account = '%s'"
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ACCOUNT]))
    if res is None:
      return None
    else:
      return res[0]
  except:
    return None


'''
validate whether password is correct.
@params includes user's account and password.
                      password need to be md5 encode.
@return user's id if password is correct.
         -1 otherwise.
'''
def validate_password(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data or KEY.SALT not in data:
    return -1
  sql = "select id, password from account where account = '%s' and salt = '%s'"
  user_id = -1
  password = None
  try:
    res = dbhelper.execute_fetchone(sql%(data[KEY.ACCOUNT], data[KEY.SALT]))
    if res is not None:
      user_id = res[0]
      password = res[1]
      print password
      print data[KEY.PASSWORD]
  except:
    pass
  finally:
    if password is None or data[KEY.PASSWORD] is None:
      print "something none"
      return -1
    elif password == data[KEY.PASSWORD]:
      return user_id
    else:
      print "not equal"
      return -1


'''
modify user's password to a new one, but not modify its salt value.
@params include user's account. 
                      new password that encode with salt by md5.
@return true if successfully modify.
           false otherwise.
'''
def modify_password(data):
  if KEY.ACCOUNT not in data or KEY.PASSWORD not in data:
    return False
  sql = "update account set password = '%s' where account = %d" 
  try:
    n = dbhelper.execute(sql%(data[KEY.PASSWORD], data[KEY.ACCOUNT]))
    if n > 0:
      return True
    else:
      return False
  except:
      return False
  
  
'''
get user's information, which includes user's name, nickname, gender ...... .
@params include user's id.
@return a json includes user's concrete information.
           None if params error or database query error.
'''
def get_user_information(data):
  if KEY.ACCOUNT not in data:
    return None
  find_id = "select id from account where account = %d"
  user_id = dbhelper.execute_fetchone(find_id%(data[KEY.ACCOUNT]))
  sql = "select * from user where id = %d"
  try:
    res = dbhelper.execute_fetchone(sql%(user_id[0]))
    if res is None:
      return None
    else:
      user = {}
      user[KEY.ID] = res[0]
      user[KEY.NAME] = res[1]
      user[KEY.NICKNAME] = res[2]
      user[KEY.GENDER] = res[3]
      user[KEY.AGE] = res[4]
      user[KEY.PHONE] = res[5]
      user[KEY.LOCATION] = res[6]
      user[KEY.LONGITUDE] = float(res[7])
      user[KEY.LATITUDE] = float(res[8])
      user[KEY.OCCUPATION] = res[9]
      user[KEY.REPUTATION] = float(res[10])
      #user[KEY.AVATAR] = res[11]
      user[KEY.IDENTITY_ID] = res[12]
      user[KEY.IS_VERIFY] = res[14]
      return user
  except:
    return None


'''
launch a help event by launcher.
@params includes user's id and type of help event.
        help event types:
                         0 represents normal question.
                         1 represents normal help.
                         2 represents emergency.
       other option params includes content of event, max helpers needed for helping, longitude and latitude of event.
@return event_id if successfully launches.
        -1 if fails.
'''
def add_event(data): 
  if KEY.ID not in data or KEY.TYPE not in data:
    return -1
  if data[KEY.TYPE] == 1 and KEY.MAX_PEOPLE not in data:
    return -1

  sql = "insert into event (launcher, type, time) values (%d, %d, now())"
  help_sql = "insert into event (launcher, type, time, help_max) values (%d, %d, now(), %d)"
  event_id = -1
  try:
    if data[KEY.TYPE] == 1:
      event_id = dbhelper.insert(help_sql%(data[KEY.ID], data[KEY.TYPE], data[KEY.MAX_PEOPLE]))
    else:
      event_id = dbhelper.insert(sql%(data[KEY.ID], data[KEY.TYPE]))
    #event_id = dbhelper.insert(sql%(data[KEY.ID], data[KEY.TYPE]))
    print "From add_event_handler: database event id: %d"%event_id
    if event_id > 0:
      data[KEY.EVENT_ID] = event_id
      update_event(data)
      # consume love_coins when adding events
      if data[KEY.TYPE] == 0:
        minus = "update loving_bank set coin = coin-1 where user_id = %d"
      elif data[KEY.TYPE] == 1:
        minus = "update loving_bank set coin = coin-2 where user_id = %d"
      elif data[KEY.TYPE] == 2:
        minus = "update loving_bank set coin = coin-3 where user_id = %d"
      dbhelper.execute(minus%(data[KEY.ID]))
    return event_id
  except:
    return -1


'''
modify information of a help event.
@params  includes event_id, which is id of the event to be modified.
         option params includes: content of event, longitude and latitude of event, state of event.
@return True if successfully modifies.
        False otherwise.
'''
def update_event(data):
  result = True
  sql = ""
  if KEY.CONTENT in data:
    data[KEY.CONTENT] = MySQLdb.escape_string(data[KEY.CONTENT].encode("utf8"))
    sql = "update event set content = '%s' where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.CONTENT], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False
  
  if KEY.LONGITUDE in data and KEY.LATITUDE in data:
    sql = "update event set longitude = %f, latitude = %f where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  if KEY.TYPE in data:
    print "From database - update event: data[KEY.TYPE] is %d"%(data[KEY.TYPE])
    if data[KEY.TYPE] == 1 and KEY.MAX_PEOPLE in data:
      sql = "update event set help_max = %d where id = %d"
      try:
        dbhelper.execute(sql%(data[KEY.MAX_PEOPLE], data[KEY.EVENT_ID]))
        result &= True
      except:
        result &= False

  if KEY.STATE in data:
    if data[KEY.STATE] == 0:
      data[KEY.STATE] = 1
    sql = "update event set state = %d where id = %d"
    try:
      dbhelper.execute(sql%(data[KEY.STATE], data[KEY.EVENT_ID]))
      result &= True
    except:
      result &= False

  return result


'''
remove a help event by event launcher.
@params includes user's id, which is remover. Actually, only the launcher can remove his/her event.
                 event's id, which represents the event to be removed.
@return True if successfully removes, or remover is not the launcher, actually nothing happens.
        False if fails.
'''
def remove_event(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return False
  sql = "delete from event where id = %d and launcher = %d"
  try:
    dbhelper.execute(sql%(data[KEY.EVENT_ID], data[KEY.ID]))
    return True
  except:
    return False


'''
get information of a help event.
@params includes id of the event to get.
@return concrete information of the event:
        event_id, launcher's id and his/her nickname, content, type, time, longitude and latitude, state, number of followers, number of supporters and group points.
        None indicates fail query.
'''
def get_event_information(data):
  if KEY.EVENT_ID not in data:
    return None
  event_info = None
  sql = "select * from event where id = %d"
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.EVENT_ID]))
    if data[KEY.EVENT_ID] == 526:
      print "search for EVENT_ID = 526"
    if sql_result is not None:
      event_info = {}
      event_info[KEY.EVENT_ID] = sql_result[0]
      event_info[KEY.LAUNCHER_ID] = sql_result[1]
      event_info[KEY.CONTENT] = sql_result[2]
      event_info[KEY.TYPE] = sql_result[3]
      event_info[KEY.TIME] = str(sql_result[4])
      event_info[KEY.LONGITUDE] = float(sql_result[5])
      event_info[KEY.LATITUDE] = float(sql_result[6])
      event_info[KEY.STATE] = sql_result[7]
      event_info[KEY.FOLLOW_NUMBER] = sql_result[8]
      event_info[KEY.SUPPORT_NUMBER] = sql_result[9]
      event_info[KEY.GROUP_PTS] = float(sql_result[10])
      event_info[KEY.MAX_PEOPLE] = sql_result[11]
      user = {}
      user[KEY.ID] = event_info[KEY.LAUNCHER_ID]
      user = get_user_information(user)
      if user is not None:
        event_info[KEY.LAUNCHER] = user[KEY.NICKNAME]
  except:
    pass
  finally:
    return event_info


'''
get information of a collection of events.
@params includes data, a json that contains user's id and type of events to get.
                 get_event_id_list a method of getting event id list.
@return a array of events. each element is information of an event in json form.
'''
def get_events(data, get_event_id_list):
  event_id_list = get_event_id_list(data)
  event_list = []
  sql = "select nickname from user where id = %d"
  for event_id in event_id_list:
    event_info = {}
    event_info[KEY.EVENT_ID] = event_id
    event_info = get_event_information(event_info)
    if event_info is not None:
      # find nickname of id
      launcher_nickname = dbhelper.execute_fetchone(sql%(event_info[KEY.LAUNCHER_ID]))
      event_info[KEY.LAUNCHER] = launcher_nickname[0]
      event_list.append(event_info)
  return event_list



'''
get near events.
@params includes option params includes state indicates near events or those starting or ended.
                 type indicates type of events.
@return an array of result event ids.
'''
def get_all_event_list(data):
  event_id_list = []
  sql = "select id from event where id = %d"
  if KEY.STATE in data:
    if data[KEY.STATE] == 0 or data[KEY.STATE] == 1:
      sql += " and state = %d"%data[KEY.STATE]
  if KEY.TYPE in data:
    if data[KEY.TYPE] >= 0 and data[KEY.TYPE] <= 2:
      sql += " and type = %d"%data[KEY.TYPE]
  sql += " order by time DESC"
  for event_id in data[KEY.EVENT_LIST]:
    result = dbhelper.execute_fetchone(sql%event_id)
    if result is not None:
      event_id_list.append(result[0])
  event_id_list = event_id_list[::-1]
  print "From database - get all events function: id list:"
  print event_id_list
  return event_id_list



'''
get events that launch by user.
@params includes user's id, 
                 option params includes state indicates all events or those starting or ended.
                 type indicates type of events.
@return an array of result event ids.
'''
def get_launch_event_list(data):
  event_id_list = []
  if KEY.ID not in data:
    return event_id_list
  sql = "select id from event where launcher = %d"%data[KEY.ID]
  if KEY.STATE in data:
    if data[KEY.STATE] == 0 or data[KEY.STATE] == 1:      
      sql += " and state = %d"%data[KEY.STATE]
  if KEY.TYPE in data:
    if data[KEY.TYPE] >= 0 and data[KEY.TYPE] <= 2:
      sql += " and type = %d"%data[KEY.TYPE]
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      event_id_list.append(each_id)

  return event_id_list


'''
get user's follow or support events.
@params includes user's id and type of user's state in event.
                 user's state 0 indicates follow, and 1 indicates support.
@return an array of result event ids.
'''
def get_join_event_list(data):
  event_id_list = []
  if KEY.ID not in data:
    return event_id_list
  sql = "select event_id from support_relation where supporter = %d"%data[KEY.ID]
  if KEY.TYPE in data:
    if data[KEY.TYPE] == 1 or data[KEY.TYPE] == 2:
      sql += " and type = %d"%data[KEY.TYPE]
  sql += " order by time DESC"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      event_id_list.append(each_id)

  return event_id_list


'''
manage relation of user and event.
@params
@return
'''
def user_event_manage(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return False
  if KEY.OPERATION not in data:
    return True
  if data[KEY.OPERATION] < 0 or data[KEY.OPERATION] > 2:
    return False
  sql = "select launcher from event where id = %d"
  launcher_id = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.EVENT_ID]))
    if sql_result is not None:
      launcher_id = sql_result[0]
  except:
    pass

  if launcher_id is None:
    return False
  if data[KEY.OPERATION] == 0:
    sql = "delete from support_relation where event_id = %d and supporter = %d"%(data[KEY.EVENT_ID], data[KEY.ID])
    update_event_sql = "update event set support_number = support_number-1 where id = %d"%(data[KEY.EVENT_ID])
  else:
    sql = "insert into support_relation (event_id, supportee, supporter, type, time) values (%d, %d, %d, %d, now())"%(data[KEY.EVENT_ID], launcher_id, data[KEY.ID], data[KEY.OPERATION])
    update_event_sql = "update event set support_number = support_number+1 where id = %d"%(data[KEY.EVENT_ID])
  count_supporter = "select count(*) from support_relation where event_id = %d and supportee = %d"%(data[KEY.EVENT_ID], launcher_id)
  help_max = "select help_max from event where id = %d and launcher = %d"%(data[KEY.EVENT_ID], launcher_id)
  state_sql = "select state from event where id = %d and launcher = %d"%(data[KEY.EVENT_ID], launcher_id)
  update_state = "update event set state = %d where id = %d"

  try:
    # update support_relation
    p = dbhelper.execute(sql)
    print "From user_event_manage_handler: attend result: %d"%p
    if p == 0:
      return False
    # update event information
    dbhelper.execute(update_event_sql)

    # Check if people are enough for helping
    supporters_result = dbhelper.execute_fetchone(count_supporter)
    help_max_result = dbhelper.execute_fetchone(help_max)
    state_result = dbhelper.execute_fetchone(state_sql)
    if supporters_result[0] == help_max_result[0] and state_result[0] == 0:
      # update event state to "supporter enough"
      dbhelper.execute(update_state%(2, data[KEY.EVENT_ID]))
      print "From db update help event:", supporters_result[0], help_max_result[0]
    elif supporters_result[0] < help_max_result[0] and state_result[0] == 2:
      # update event state to "ing"
      dbhelper.execute(update_state%(0, data[KEY.EVENT_ID]))
  except:
    return False

  #
  # trust and reputation compute here.
  #
  return True


'''
add a new comment to a help event.
@params includes event_id, represents comment belongs to which event,
                 author, user's id, author of comment,
                 content, content of comment.
@return new comment id if succeed,
        -1 otherwise.
'''
def add_comment(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return -1
  if KEY.CONTENT not in data:
    return -1
  sql = "insert into comment (event_id, author, content, time) values (%d, %d, '%s', now())"
  try:
    comment_id = dbhelper.insert(sql%(data[KEY.EVENT_ID], data[KEY.ID], data[KEY.CONTENT]))
    return comment_id
  except:
    return -1


'''
remove a comment from a help event by author him/her self.
@params includes id, indicates author him/her self.
                 event_id, indicates which event the comment belongs to.
                 comment_id, indicates comment itself.
@return True if delete successfully,
        False if fails.
'''
def remove_comment(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data or KEY.COMMENT_ID not in data:
    return False
  sql = "delete from comment where id = %d and event_id = %d and author = %d"
  try:
    dbhelper.execute(sql%(data[KEY.COMMENT_ID], data[KEY.EVENT_ID], data[KEY.ID]))
    return True
  except:
    return False


'''
get comments of a help event.
@params event_id, id of the help event.
@return a list of comments. each comment contain all detail information.
'''
def get_comments(data):
  if KEY.EVENT_ID not in data:
    return None
  comment_list = []
  comment = {}
  sql = "select id from comment where event_id = %d order by time DESC"
  try:
    sql_result = dbhelper.execute_fetchall(sql%(data[KEY.EVENT_ID]))
    for each_result in sql_result:
      for each_id in each_result:
        comment[KEY.COMMENT_ID] = each_id
        comment = get_comment_info(comment)
        if comment is not None:
          comment_list.append(comment)
    return comment_list
  except:
    return None


'''
get detail information of a comment.
@params includes comment_id, id of comment.
@return information of comment, includes id of comment,
                                         event_id, indicates which event belongs to,
                                         author_id, author's user id,
                                         author, nickname of author,
                                         content, main body of comment,
                                         time, add time of comment.
        None indicates a fail query. Maybe the chosen comment doesn't exist.
'''
def get_comment_info(data):
  if KEY.COMMENT_ID not in data:
    return None
  sql = "select event_id, author, content, time from comment where id = %d"
  comment_info = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(data[KEY.COMMENT_ID]))
    if sql_result is not None:
      comment_info = {}
      comment_info[KEY.COMMENT_ID] = data[KEY.COMMENT_ID]
      comment_info[KEY.EVENT_ID] = sql_result[0]
      comment_info[KEY.AUTHOR_ID] = sql_result[1]
      comment_info[KEY.CONTENT] = sql_result[2]
      comment_info[KEY.TIME] = str(sql_result[3])
      user = {}
      user[KEY.ID] = comment_info[KEY.AUTHOR_ID]
      user = get_user_information(user)
      if user is not None:
        comment_info[KEY.AUTHOR] = user[KEY.NICKNAME]
  except:
    pass
  finally:
    return comment_info


'''
add a static relation between two users. The relation is single direction.
@params includes two users' id, one is called id, the other called user_id.
parameter type indicates type of static relation. two users in one direction could only have one type of relation.
                 type:  0 indicates emergency contact relation.
                        1 indicates normal relation.
@return True if successfully adds.
        False otherwise.
'''
def add_static_relation(data):
  if KEY.ID not in data or KEY.USER_ACCOUNT not in data or KEY.TYPE not in data:
    return False
  find_user_id = "select id from account where account = %d"
  user_id = dbhelper.execute_fetchone(find_user_id%data[KEY.USER_ACCOUNT])
  #sql = "replace into static_relation (user_a, user_b, type, time) values (%d, %d, %d, now())"
  sql = "insert into static_relation (user_a, user_b, type, time) values (%d, %d, %d, now())"
  try:
    n = dbhelper.execute(sql%(data[KEY.ID], user_id[0], data[KEY.TYPE]))
    if n > 0:
      return True
    else:
      return False
  except:
    return False


'''
remove a static relation of two user.
@params includes two users' id, one is called id, the other called user_id.
@return True if successfully removes.
        False otherwise.
'''
def remove_static_relation(data):
  if KEY.ID not in data or KEY.USER_ACCOUNT not in data or KEY.TYPE not in data:
    return False
  find_user_id = "select id from account where account = %d"
  user_id = dbhelper.execute_fetchone(find_user_id%data[KEY.USER_ACCOUNT])
  sql = "delete from static_relation where user_a = %d and user_b = %d and type = %d"
  try:
    n = dbhelper.execute(sql%(data[KEY.ID], user_id[0], data[KEY.TYPE]))
    if n > 0:
      return True
    else:
      return False
  except:
    return False


'''
return a list of static relation.
@params includes id, user id.
parameter type indicates type of static relation. two users in one direction could only have one type of relation.
                 type:  0 indicates emergency contact relation.
                        1 indicates normal relation.
@return user list include account, nickname and avatar(could be null)
        None indicates no static relation.
'''
def get_static_relation(data):
  # related user list
  user_list = []
  # a related user, include account(table 'account'), nickname, avatar(table 'user')
  one_user = {}
  if KEY.ID not in data:
    return user_list

  # 1. get a user_id_list from table 'static_relation'
  get_id_list_sql = "select user_b from static_relation where user_a = %d"%data[KEY.ID]
  if KEY.TYPE in data:
    if data[KEY.TYPE] == 1 or data[KEY.TYPE] == 0:
      get_id_list_sql += " and type = %d"%data[KEY.TYPE]
  sql_result = dbhelper.execute_fetchall(get_id_list_sql)
  user_id_list = []
  for each_result in sql_result:
    for each_id in each_result:
      user_id_list.append(each_id)
  
  # 2. get each user's information, put them in to user list
  for each_user in user_id_list:
    one_user[KEY.ID] = each_user
    one_user = get_user(one_user)
    if one_user is not None:
      one_user[KEY.ID] = each_user
      user_list.append(one_user)

  return user_list



'''
get brief information of a user.
@params includes id of the user to get.
@return concrete information of the event:
        account, nickname, avatar.
        None indicates fail query.
'''
def get_user(data):
  if KEY.ID not in data:
    return None
  one_user = {}
  get_account_sql = "select account from account where id = %d"
  try:
    account_result = dbhelper.execute_fetchone(get_account_sql%(data[KEY.ID]))
    if account_result is not None:
      one_user[KEY.ACCOUNT] = account_result[0]
      user = {}
      user[KEY.ACCOUNT] = account_result[0]
      user = get_user_information(user)
      if user is not None:
        one_user[KEY.NICKNAME] = user[KEY.NICKNAME]
        one_user[KEY.NAME] = user[KEY.NAME]
  except:
    pass
  finally:
    return one_user



'''
give an evaluation to a user in a help event.
@params includes: id, evaluater.
                  user_account, evaluatee.
                  event_id, indicates the help event.
                  attitude, attitude point
                  skill, skill point
                  satisfy, satisfied point
                  assess, comment(optional)
                  love_point, love_point to evaluatee
@return True if successfully evaluate.
        False otherwise.
'''
def evaluate_user(data):
  if KEY.ID not in data or KEY.USER_ACCOUNT not in data or KEY.EVENT_ID not in data:
    return False
  if KEY.ATTITUDE not in data or KEY.SKILL not in data or KEY.SATISFY not in data:
    return False
  
  # get a new average reputation value
  value = 0.0
  value = data[KEY.ATTITUDE] + data[KEY.SKILL] + data[KEY.SATISFY]
  value /= 3.0

  # get type of the event
  get_type = "select type from event where id = %d"%data[KEY.EVENT_ID]
  type_result = dbhelper.execute_fetchone(get_type)
  event_type = type_result[0]

  result = 0
  # split user_account string into long array
  user_account = data[KEY.USER_ACCOUNT].split(",")
  # update each user's reputation in list
  for each_account in user_account:
    if (long(each_account) != 0):
      # get id by account
      find_user_id = "select id from account where account = %d"
      user_id = dbhelper.execute_fetchone(find_user_id%(long(each_account)))
      print "From evaluate_handler: %ld" % long(each_account)

      # update a record in table 'evaluation'
      sql = "replace into evaluation (event_id, `from`, `to`, value, time, comment) values (%d, %d, %d, %f, now(), '%s')"
      # get an updated reputation value from table 'evaluation'
      get_final_value = "select AVG(value) from evaluation where `to` = %d"
      # update evaluatee's reputation in table 'user'
      update_repu = "update user set reputation = %d where id = %d"
      # update love coins in table 'loving_bank'
      if event_type == 0:
        update_coin = "update loving_bank set coin = coin+1 where id = %d"
      if event_type == 1:
        update_coin = "update loving_bank set coin = coin+2 where id = %d"
      if event_type == 2:
        update_coin = "update loving_bank set coin = coin+3 where id = %d"

      try:
        a = dbhelper.execute(sql%(data[KEY.EVENT_ID], data[KEY.ID], user_id[0], value, data[KEY.ASSESS]))
        final_value = dbhelper.execute_fetchone(get_final_value%(user_id[0]))
        dbhelper.execute(update_repu%(final_value[0], user_id[0]))
        dbhelper.execute(update_coin%(data[KEY.EVENT_ID]))
        result += 1
      except:
        pass

  return result



'''
add a health record of a user into database.
@params includes id, user's id.
                 type, type of health indicator.
                 value, value of some health indicator.
@return the health record id of the new record.
        -1 indicates fail.
'''
def health_record(data):
  if KEY.ID not in data or KEY.TYPE not in data or KEY.VALUE not in data:
    return -1
  sql = "insert into health (user_id, type, value, time) values (%d, %d, %f, now())"
  record_id = -1
  try:
    record_id = dbhelper.insert(sql%(data[KEY.ID], data[KEY.TYPE], data[KEY.VALUE]))
  except:
    record_id = -1
  finally:
    return record_id


'''
get details of one certain health record.
@params includes record_id, id of the health record.
@return details of the health record, contains record id, user id, type, certain value and record time.
        None indicates fail query.
'''
def get_health_record(record_id):
  sql = "select id, user_id, type, value, time from health where id = %d"
  record = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(record_id))
    if sql_result is not None:
      record = {}
      record[KEY.HEALTH_ID] = sql_result[0]
      record[KEY.USER_ID] = sql_result[1]
      record[KEY.TYPE] = sql_result[2]
      record[KEY.VALUE] = float(sql_result[3])
      record[KEY.TIME] = str(sql_result[4])
  except:
    record = None
  finally:
    return record


'''
get all health records of a user, but at most 100 records.
@params includes id, user's id.
@return a list that contain all health records. each element is a json that contains details information of a health record.
        None indicates fail query.
'''
def get_health_records(data):
  if KEY.ID not in data:
    return None
  sql = "select id from health where user_id = %d order by time DESC limit %d"
  sql_result = None
  try:
    sql_result = dbhelper.execute_fetchall(sql%(data[KEY.ID], 100))
  except:
    sql_result = None
  records = None
  if sql_result is not None:
    records = []
    for each_result in sql_result:
      for each_id in each_result:
        a_record = get_health_record(each_id)
        if a_record is not None:
          records.append(a_record)
  return records


'''
add an illness record of a user into database.
@params includes id, user's id.
                 content, illness detail information.
@return illness record id.
        -1 indicates fail.
'''
def illness_record(data):
  if KEY.ID not in data or KEY.CONTENT not in data:
    return -1
  sql = "insert into illness (user_id, content, time) values (%d, '%s', now())"
  illness_id = -1
  try:
    illness_id = dbhelper.insert(sql%(data[KEY.ID], data[KEY.CONTENT]))
  except:
    illness_id = -1
  finally:
    return illness_id


'''
get details of an illness record.
@params includes record id, indicates which record to be queried.
@return content of an illness record, includes record's id, user's id, illness content and illness time.
        None indicates fail query or no such record.
'''
def get_illness_record(record_id):
  sql = "select id, user_id, content, time from illness where id = %d"
  record = None
  try:
    sql_result = dbhelper.execute_fetchone(sql%(record_id))
    if sql_result is not None:
      record = {}
      record[KEY.ILLNESS_ID] = sql_result[0]
      record[KEY.USER_ID] = sql_result[1]
      record[KEY.CONTENT] = sql_result[2]
      record[KEY.TIME] = str(sql_result[3])
  except:
    record = None
  finally:
    return record


'''
get all illness records of a user, but at most 100 records.
@params includes: id, user's id.
@return a list that contain all illness records. each element in the list is a json that is consist of details of an illness record.
        None indicates fail query.
'''
def get_illness_records(data):
  if KEY.ID not in data:
    return None
  sql = "select id from illness where user_id = %d order by time ASC limit %d"
  sql_result = None
  records = None
  try:
    sql_result = dbhelper.execute_fetchall(sql%(data[KEY.ID], 100))
  except:
    sql_result = None
  if sql_result is not None:
    records = []
    for each_result in sql_result:
      for each_id in each_result:
        a_record = get_illness_record(each_id)
        if a_record is not None:
          records.append(a_record)
  return records


'''
create a loving bank account. It contains loving bank and credit.
@params includes user_id, user's id, initial coin number and initial score value.
@return new bank account id if succeed.
        -1 if fail.
'''
def create_loving_bank(data, init_coin=0, init_score=0):
  if KEY.ID not in data:
    return -1
  sql = "insert into loving_bank (user_id, coin, score, ac_score) values (%d, %d, %d, %d)"
  try:
    bank_account_id = dbhelper.insert(sql%(data[KEY.ID], init_coin, init_score, init_score))
    return bank_account_id
  except:
    return -1


'''
user could sign in once a day. Especially, if user has signed in today, this method would return false.
@params includes user_id. user's id.
@return True if sign in successfully.
        False otherwise.
'''
def sign_in(data):
  if KEY.ID not in data:
    return False
  if is_sign_in(data[KEY.ID]):
    return False
  sql = "insert into sign_in (user_id, time) values (%d, now())"
  try:
    sign_in_id = dbhelper.insert(sql%(data[KEY.ID]))
    if sign_in_id > 0:
      # every day sign in and coin increase 2
      incre = "update loving_bank set coin = coin+2 where user_id = %d"
      a = dbhelper.execute(incre%(data[KEY.ID]))
      print "                                    ", a
      print "                                    ", a
      print "                                    ", a
      print "                                    ", a
      print "                                    ", a
      return True
    else:
      return False
  except:
    return False


'''
check whether a user has signed in today.
@params includes user_id. user's id.
@return True if user has signed in.
        False otherwise.
'''
def is_sign_in(user_id):
  result = False
  sql = "select count(*) from sign_in where user_id = %d and to_days(time) = to_days(now())"
  try:
    sql_result = dbhelper.execute_fetchone(sql%(user_id))[0]
    if sql_result > 0:
      result = True
    else:
      result = False
  except:
    result = False
  finally:
    return result


'''
get a event's followers id.
@params includes event's id and type is default to 2, meaning following.
@return an array of followers ids.
'''
def get_event_followers(data):
  followers_id_list = []
  if KEY.EVENT_ID not in data:
    return followers_id_list
  sql = "select supporter from support_relation where event_id = %d"%data[KEY.EVENT_ID]
  sql += " and type = 2"
  sql_result = dbhelper.execute_fetchall(sql)
  for each_result in sql_result:
    for each_id in each_result:
      followers_id_list.append(each_id)

  return followers_id_list



'''
get a supporter list of a event.
@params includes event's id and launcher's id.
@return an array of supporters accounts.
'''
def get_event_supporter(data):
  supporter_list = []
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return support_list

  # 1. find supporters id in table 'support_relation' by launcher id and event id
  find_id_sql = "select supporter from support_relation where supportee = %d and event_id = %d"
  id_result = dbhelper.execute_fetchall(find_id_sql%(data[KEY.ID], data[KEY.EVENT_ID]))

  # 2. find accounts from table 'account' by ids
  find_account_sql = "select account from account where id = %d"
  if id_result is not None:
    for each_id in id_result:
      supporter_result = dbhelper.execute_fetchone(find_account_sql%(each_id[0]))
      print each_id
      supporter = {}
      supporter[KEY.ACCOUNT] = supporter_result[0]
      user_info = get_user_information(supporter)
      # get current location of supporter
      find_longitude_sql = "select longitude from support_relation where event_id = %d and supporter = %d"
      find_latitude_sql = "select latitude from support_relation where event_id = %d and supporter = %d"
      longitude_result = dbhelper.execute_fetchone(find_longitude_sql%(data[KEY.EVENT_ID], each_id[0]))
      latitude_result = dbhelper.execute_fetchone(find_latitude_sql%(data[KEY.EVENT_ID], each_id[0]))
      if user_info is not None:
        supporter.update(user_info)
        supporter[KEY.ACCOUNT] = supporter_result[0]
        supporter[KEY.LONGITUDE] = float(longitude_result[0])
        supporter[KEY.LATITUDE] = float(latitude_result[0])
        supporter_list.append(supporter)
      #supporter_list.append(supporter_result[0])
  return supporter_list


'''
update current user location.
@params includes event's id, launcher's id and location.
@return True if update successfully.
        False otherwise.
'''
def update_location(data):
  if KEY.LONGITUDE not in data or KEY.LATITUDE not in data or KEY.ID not in data:
    return False

  # if there is a event id, also update a helper's location
  if KEY.EVENT_ID in data:
    help_sql = "update support_relation set longitude = %f, latitude = %f where event_id = %d and supporter = %d"
  # update a user's location, in table 'user'
  sql = "update user set longitude = %f, latitude = %f where id = %d"
  try:
    dbhelper.execute(sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.ID]))
    if KEY.EVENT_ID in data:
      dbhelper.execute(help_sql%(data[KEY.LONGITUDE], data[KEY.LATITUDE], data[KEY.EVENT_ID], data[KEY.ID]))
    return True
  except:
    return False


'''
update_user corresponding push token.
@params includes user's account, push token.
@return True if update successfully.
        False otherwise.
'''
def update_token(data):
  if KEY.ID not in data or KEY.TOKEN not in data:
    return False

  sql = "update account set push_token = '%s' where id = %d"
  try:
    dbhelper.execute(sql%(data[KEY.TOKEN], data[KEY.ID]))
    return True
  except:
    return False



'''
get users' push token from database.
@params includes users' id list.
@return a list of tokens.
        None otherwise.
'''
def get_push_token(data):
  if data == []:
    return None

  sql = "select push_token from account where id = %d"
  token_list = []
  for user_id in data:
    token_result = dbhelper.execute_fetchone(sql%(user_id))
    if token_result is not None:
      token_list.append(token_result[0])
  print "From database - get push token function: "
  print token_list
  return token_list


'''
get current user's location.
@params includes user's id.
@return user's location in table 'user'
'''
def get_user_current_location(data):
  location = {}
  
  if KEY.ID not in data:
    return location
  sql = "select longitude, latitude from user where id = %d"%(data[KEY.ID])

  try:
    location_result = dbhelper.execute_fetchone(sql)
    location[KEY.LONGITUDE] = location_result[0]
    location[KEY.LATITUDE] = location_result[1]
    print "From database - get user current location:"
    print location
    return location
  except:
    return location


'''
update file path in database of user's avatar.
@params includes avatar path, user's id.
@return True if update successfully.
        False otherwise.
'''
def update_db_avatar(data):
  if KEY.ID not in data or 'filepath' not in data:
    return False
  sql = "update user set avatar = '%s' where id = %d"
  try:
    result = dbhelper.execute(sql%(data['filepath'], data[KEY.ID]))
    print "From database - update db avatar: update operation result: %d"%result
    return True
  except:
    return False


'''
get file path in database of user's avatar.
@params includes user's id.
@return file path.
        "" otherwise.
'''
def get_db_avatar(data):
  if KEY.ID not in data:
    return ""
  sql = "select avatar from user where id = %d"
  try:
    result = dbhelper.execute_fetchone(sql%(data[KEY.ID]))
    print "From database - get db avatar: user id - '%d', avatar - '%s'"%(data[KEY.ID], result[0])
    return result[0]
  except:
    return ""



'''
get user's love coin.
@params includes user's id.
@return coins.
        -1 when none existed.
'''
def get_love_coin(data):
  if KEY.ID not in data:
    return -1
  sql = "select coin from loving_bank where user_id = %d"%data[KEY.ID]
  try:
    result = dbhelper.execute_fetchone(sql)
    return result[0]
  except:
    return -1



'''
get all uses' ids and accounts.
no params passed.
it return a list.
'''
def connect_hx():
    sql = "select * from account"
    user_list = []
    user_info = {}
    sql_result = dbhelper.execute_fetchall(sql)
    if sql_result is not None:
        for each_result in sql_result:
            user_info['username'] = each_result[KEY.ID]
            user_info[KEY.PASSWORD] = each_result[KEY.PASSWORD]
            if user_info is not None:
                user_list.append(user_info)
    return user_list



'''
get user's id by account.
@params includes user's account.
@return user's id.
'''
def get_user_id(data):
  if KEY.USER_ACCOUNT not in data:
    return -1
  sql = "select id from account where account = %d"%data[KEY.USER_ACCOUNT]
  sql_result = dbhelper.execute_fetchone(sql)
  if sql_result is not None:
    return sql_result[0]
  else:
    return -1



'''
get user's evaluation.
@params includes event id, user id.
@return value if existed.
        None otherwise.
'''
def get_user_evaluate(data):
  if KEY.ID not in data or KEY.EVENT_ID not in data:
    return None
  evaluate = {}
  sql = "select value, comment from evaluation where event_id = %d and `to` = %d"
  sql_result = dbhelper.execute_fetchone(sql%(data[KEY.EVENT_ID], data[KEY.ID]))
  if sql_result is not None:
    evaluate[KEY.VALUE] = float(sql_result[0])
    evaluate[KEY.COMMENT] = sql_result[1]
    return evaluate
  else:
    return None




