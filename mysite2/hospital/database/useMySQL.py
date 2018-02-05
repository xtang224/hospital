#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import MySQLdb

def getCurrentUser():
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "SELECT * FROM hospital_current_user"
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      # 获取所有记录列表
      results = cursor.fetchall()
      for row in results:
         userNo = row[0]
         userName = row[1]
         userTired = row[2]
         userTemperature = row[3]
         userRespire = row[4]
         userHeart = row[5]
         userStomach = row[6]
         userShit = row[7]
         userPrevAsk = row[8]
         user = [userNo, userName, userTired, userTemperature, userRespire, userHeart, userStomach, userShit, userPrevAsk]
         # 打印结果
         #print "userNo=%s,userName=%s,userTired=%s,userTemperature=%s,userRespire=%s,userStomach=%s,userShit=%s,userPrevAsk=%s" % \
         #       (userNo, userName, userTired, userTemperature, userRespire, userHeart, userStomach, userShit, userPrevAsk)
   except:
      print "Error: unable to fetch data"

   # 关闭数据库连接
   db.close()
   return user

def setCurrentUserTired(tired='-1'):
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "UPDATE hospital_current_user SET hospital_user_tired = '%s'" % (tired)
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      db.commit()
   except:
      print "Error: unable to update data"

   # 关闭数据库连接
   db.close()
   return 

def setCurrentUserTemperature(temperature='-1'):
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "UPDATE hospital_current_user SET hospital_user_temperature = '%s'" % (temperature)
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      db.commit()
   except:
      print "Error: unable to update data"

   # 关闭数据库连接
   db.close()
   return

def setCurrentUserRespire(respire='-1'):
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "UPDATE hospital_current_user SET hospital_user_respire = '%s'" % (respire)
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      db.commit()
   except:
      print "Error: unable to update data"

   # 关闭数据库连接
   db.close()
   return

def setCurrentUserHeart(heart='-1'):
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "UPDATE hospital_current_user SET hospital_user_heart = '%s'" % (heart)
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      db.commit()
   except:
      print "Error: unable to update data"

   # 关闭数据库连接
   db.close()
   return

def setCurrentUserStomach(stomach='-1'):
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "UPDATE hospital_current_user SET hospital_user_stomach = '%s'" % (stomach)
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      db.commit()
   except:
      print "Error: unable to update data"

   # 关闭数据库连接
   db.close()
   return

def setCurrentUserShit(shit='-1'):
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "UPDATE hospital_current_user SET hospital_user_shit = '%s'" % (shit)
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      db.commit()
   except:
      print "Error: unable to update data"

   # 关闭数据库连接
   db.close()
   return

def setCurrentUserPrevAsk(prevAsk='-1'):
   db = MySQLdb.connect("localhost","root","","hospital")
   cursor = db.cursor()
   sql = "UPDATE hospital_current_user SET hospital_user_prevAsk = '%s'" % (prevAsk)
   user = []
   try:
      # 执行SQL语句
      cursor.execute(sql)
      db.commit()
   except:
      print "Error: unable to update data"

   # 关闭数据库连接
   db.close()
   return

