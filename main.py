#!/usr/python

import os

import tornado
import tornado.httpserver

from handler import regist_handler
from handler import login_handler
from handler import get_user_information_handler
from handler import modify_user_information_handler
from handler import modify_password_handler
from handler import add_event_handler
from handler import update_event_handler
from handler import remove_event_handler
from handler import get_launch_events_handler
from handler import get_join_events_handler
from handler import user_event_manage_handler
from handler import add_comment_handler
from handler import remove_comment_handler
from handler import get_comments_handler
from handler import user_relation_manage_handler
from handler import add_health_handler
from handler import get_health_records_handler
from handler import add_illness_handler
from handler import get_illness_records_handler
from handler import user_relation_manage_handler
from handler import sign_in_handler
from handler import evaluate_handler
from handler import get_static_relation_handler
from handler import get_event_supporter_handler
from handler import get_all_events_handler
from handler import get_single_event_handler
from handler import update_user_location_handler
from handler import update_push_token_handler
from handler import test_baidu_handler
from handler import upload_avatar_handler
from handler import get_love_coin_handler
from handler import upload_file_handler
from handler import download_file_handler
from handler import user_get_evaluate_handler


def main():
  port = 1503
  application = tornado.web.Application(
    handlers=[
      (r"/account/regist", regist_handler.Regist_Handler),
      (r"/account/login", login_handler.Login_Handler),
      (r"/user/get_information", get_user_information_handler.Get_User_Information_Handler),
      (r"/user/modify_information", modify_user_information_handler.Modify_User_Information_Handler),
      (r"/account/modify_password", modify_password_handler.Modify_Password_Handler),
      (r"/event/add", add_event_handler.Add_Event_Handler),
      (r"/event/modify", update_event_handler.Update_Event_Handler),
      (r"/event/remove", remove_event_handler.Remove_Event_Handler),
      (r"/event/query_launch", get_launch_events_handler.Get_Launch_Events_Handler),
      (r"/event/query_join", get_join_events_handler.Get_Join_Events_Handler),
      (r"/user/event_manage", user_event_manage_handler.User_Event_Manage_Handler),     
      (r"/comment/add", add_comment_handler.Add_Comment_Handler),
      (r"/comment/remove", remove_comment_handler.Remove_Comment_Handler),
      (r"/comment/query", get_comments_handler.Get_Comments_Handler),
      (r"/user/relation_manage", user_relation_manage_handler.User_Relation_Manage_Handler),      
      (r"/health/upload", add_health_handler.Add_Health_Handler),
      (r"/health/query", get_health_records_handler.Get_Health_Records_Handler),
      (r"/illness/upload", add_illness_handler.Add_Illness_Handler),
      (r"/illness/query", get_illness_records_handler.Get_Illness_Records_Handler),
      (r"/user/evaluate", evaluate_handler.Evaluate_Handler),
      (r"/account/signin", sign_in_handler.Sign_In_Handler),
      (r"/user/get_relation", get_static_relation_handler.Get_Static_Relation_Handler),
      (r"/event/get_supporter", get_event_supporter_handler.Get_Event_Supporter_Handler),
      (r"/event/query_all", get_all_events_handler.Get_All_Events_Handler),
      (r"/event/query", get_single_event_handler.Get_Single_Events_Handler),
      (r"/user/update_location", update_user_location_handler.Update_User_Location_Handler),
      (r"/account/update_token", update_push_token_handler.Update_Push_Token_Handler),
      (r"/test_baidu", test_baidu_handler.Test_Baidu_Handler),
      (r"/user/avatar", upload_avatar_handler.Upload_Avatar_Handler),
      (r"/user/love_coins", get_love_coin_handler.Get_Love_Coin_Handler),
      (r"/file/upload", upload_file_handler.Upload_File_Handler),
      (r"/file/download", download_file_handler.Download_File_Handler),
      (r"/user/get_evaluate", user_get_evaluate_handler.User_Get_Evaluate_Handler),

    ], debug=True)
  http_server = tornado.httpserver.HTTPServer(application)
  http_server.listen(port)

  tornado.ioloop.IOLoop.instance().start()


if __name__ == '__main__':
  main()

