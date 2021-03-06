#!/usr/bin/env python
#coding=utf8

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from hospital.models import User,Pair, Person

import logging

import numpy as np
import cv2
import sqlite3
import redis

#from settings import Logging
#logger = LOGGING.getLogger('mylogger')
# Create your views here.

import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.path.append('/home/xtang/python_web/mysite2/hospital/machine')
sys.path.append('/home/xtang/python_web/mysite2/hospital/database')
import kNN
import useMySQL
from numpy import *

import urllib
def getHtml(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html
  
def search(request):
   keyword = request.POST['keyword']
   print 'keyword = ', keyword
   if keyword==u'哮喘':
      return render(request, 'hospital/respire/asthma.html')
   elif keyword==u'感冒':
      return render(request, 'hospital/respire/cold.html')
   elif keyword==u'气管炎':
      return render(request, 'hospital/respire/qiguanyan.html')
   elif keyword==u'拉肚子':
      return render(request, 'hospital/digest/laduzi.html')
   elif keyword==u'消化不良':
      return render(request, 'hospital/digest/illDigest.html')
   elif keyword==u'胃炎':
      return render(request, 'hospital/digest/stomachIll.html')
   else:
      html = getHtml('http://localhost:8000/hospital/respire/asthma.html')      
      #print 'html = ', html
      pos = html.find(keyword)
      if pos!=-1:
         return render(request, 'hospital/respire/asthma.html')
      html = getHtml('http://localhost:8000/hospital/respire/cold.html')
      pos = html.find(keyword)
      if pos!=-1:
         return render(request, 'hospital/respire/cold.html')
      html = getHtml('http://localhost:8000/hospital/respire/qiguanyan.html')
      pos = html.find(keyword)
      if pos!=-1:
         return render(request, 'hospital/respire/qiguanyan.html')
      html = getHtml('http://localhost:8000/hospital/digest/laduzi.html')
      pos = html.find(keyword)
      if pos!=-1:
         return render(request, 'hospital/digest/laduzi.html')
      html = getHtml('http://localhost:8000/hospital/digest/illDigest.html')
      pos = html.find(keyword)
      if pos!=-1:
         return render(request, 'hospital/digest/illDigest.html')
      html = getHtml('http://localhost:8000/hospital/digest/stomachIll.html')
      pos = html.find(keyword)
      if pos!=-1:
         return render(request, 'hospital/digest/stomachIll.html')
   return render(request, 'hospital/index.html')

def index(request):
   return render(request, 'hospital/index.html')

def robot(request):
   return render(request, 'hospital/robot.html')

def asthma(request):
   return render(request, 'hospital/respire/asthma.html')

def cold(request):
   return render(request, 'hospital/respire/cold.html')

def qiguanyan(request):
   return render(request, 'hospital/respire/qiguanyan.html')

def laduzi(request):
   return render(request, 'hospital/digest/laduzi.html')

def illDigest(request):
   return render(request, 'hospital/digest/illDigest.html')

def stomachIll(request):
   return render(request, 'hospital/digest/stomachIll.html')

def ask(request):
   ask=''
   question = request.GET['dialogue_question']
   last_ask = request.GET['last_ask']
   print 'question = ', question
   print 'last_ask = ', last_ask
   if question==u'哮喘':
      return render(request, 'hospital/respire/asthma.html')
   elif question==u'感冒':
      return render(request, 'hospital/respire/cold.html')
   elif question==u'气管炎':
      return render(request, 'hospital/respire/qiguanyan.html')
   elif question==u'拉肚子':
      return render(request, 'hospital/digest/laduzi.html')
   elif question==u'消化不良':
      return render(request, 'hospital/digest/illDigest.html')
   elif question==u'胃炎':
      return render(request, 'hospital/digest/stomachIll.html')

   #below will start smart diagonose system
   #first, we want to be sure whether this is the first time for the current user to ask question
   currentUser = useMySQL.getCurrentUser()
   print 'currentUser = ', currentUser
   inputCor = 'correct'
   context = ''
   if last_ask == u'':
      last_ask = currentUser[8]
   if last_ask==u'-1':
      reply = '这是您的第一次提问，我们需要输入您的基本信息，请问您是否感觉疲劳，请输入0-7之间的一个数字，其中0表示根本不疲劳，数字越大，表示疲劳感越强，7表示非常疲劳：'
      t = loader.get_template('hospital/robot.html')
      context = Context({'reply':reply,'last_ask':'tired','ask':ask})
      useMySQL.setCurrentUserPrevAsk('tired')
      return HttpResponse(t.render(context))
   elif last_ask==u'tired':
      try:
         question2 = float(question)
      except:
         inputCor = 'incorrect'         
      if inputCor=='incorrect':
         reply = '请输入一个数字;请再次输入您的疲劳感信息，请输入0-7之间的一个数字，其中0表示根本不疲劳，数字越大，表示疲劳感越强，7表示非常疲劳：' 
         context = Context({'reply':reply,'last_ask':'tired','ask':ask})
      else:
         reply = '请继续输入您的体温，如果没有测量过体温，感觉正常请输入37，发烧或发冷则请分别输入大于37或小于37的数字'
         context = Context({'reply':reply,'last_ask':'temperature','ask':ask})
         useMySQL.setCurrentUserPrevAsk('temperature')
         useMySQL.setCurrentUserTired(question)
      t = loader.get_template('hospital/robot.html')      
      return HttpResponse(t.render(context))
   elif last_ask==u'temperature':
      try:
         question2 = float(question)
      except:
         inputCor = 'incorrect'
      if inputCor == 'incorrect':
         reply = '请输入一个数字;请再次输入您的体温，如果没有测量过体温，感觉正常请输入37，发烧或发冷则请分别输入大于37或小于37的数字：' 
         context = Context({'reply':reply,'last_ask':'temperature','ask':ask})
      else:
         reply = '请继续输入您的呼吸感觉，请输入0-7之间的一个数字，其中0表示呼吸很顺畅，数字越大，表示呼吸越困难，7表示呼吸非常困难：'
         context = Context({'reply':reply,'last_ask':'respire','ask':ask})
         useMySQL.setCurrentUserPrevAsk('respire')
         useMySQL.setCurrentUserTemperature(question)
      t = loader.get_template('hospital/robot.html')      
      return HttpResponse(t.render(context))
   elif last_ask==u'respire':
      try:
         question2 = float(question)
      except:
         inputCor = 'incorrect'
      if inputCor == 'incorrect':
         reply = '请输入一个数字;请再次输入您的呼吸感觉，请输入0-7之间的一个数字，其中0表示呼吸很顺畅，数字越大，表示呼吸越困难，7表示呼吸非常困难：' 
         context = Context({'reply':reply,'last_ask':'respire','ask':ask})
      else:
         reply = '请继续输入您的心跳感觉，请输入0-7之间的一个数字，其中0表示心跳很平稳或正常，数字越大，表示心跳越不平稳或越不正常，7表示心跳非常不正常：'
         context = Context({'reply':reply,'last_ask':'heart','ask':ask})
         useMySQL.setCurrentUserPrevAsk('heart')
         useMySQL.setCurrentUserRespire(question)
      t = loader.get_template('hospital/robot.html')      
      return HttpResponse(t.render(context))
   elif last_ask==u'heart':
      try:
         question2 = float(question)
      except:
         inputCor = 'incorrect'
      if inputCor == 'incorrect':
         reply = '请输入一个数字;请再次输入您的心跳感觉，请输入0-7之间的一个数字，其中0表示心跳很平稳或正常，数字越大，表示心跳越不平稳或越不正常，7表示心跳非常不正常：' 
         context = Context({'reply':reply,'last_ask':'heart','ask':ask})
      else:
         reply = '请继续输入您的胃部感觉，请输入0-7之间的一个数字，其中0表示胃部感觉很好或正常，数字越大，表示胃部感觉越不好或越不正常，7表示胃部感觉非常不正常：'
         context = Context({'reply':reply,'last_ask':'stomach','ask':ask})
         useMySQL.setCurrentUserPrevAsk('stomach')
         useMySQL.setCurrentUserHeart(question)
      t = loader.get_template('hospital/robot.html')      
      return HttpResponse(t.render(context))
   elif last_ask==u'stomach':
      try:
         question2 = float(question)
      except:
         inputCor = 'incorrect'
      if inputCor == 'incorrect':
         reply = '请输入一个数字;请再次输入您的胃部感觉，请输入0-7之间的一个数字，其中0表示胃部感觉很好，数字越大，表示胃部感觉越不好或越不正常，7表示胃部感觉非常不正常：' 
         context = Context({'reply':reply,'last_ask':'stomach','ask':ask})
      else:
         reply = '请继续输入您的大便情况，请输入0-7之间的一个数字，其中0表示大便很干，数字越大，表示大便越呈现水样状态，7表示水样大便：'
         context = Context({'reply':reply,'last_ask':'shit','ask':ask})
         useMySQL.setCurrentUserPrevAsk('shit')
         useMySQL.setCurrentUserStomach(question)
      t = loader.get_template('hospital/robot.html')      
      return HttpResponse(t.render(context))
   elif last_ask==u'shit':
      try:
         question2 = float(question)
      except:
         inputCor = 'incorrect'
         reply = '请输入一个数字;请再次输入您的大便情况，请输入0-7之间的一个数字，其中0表示大便很干，数字越大，表示大便越呈现水样状态，7表示水样大便：' 
         context = Context({'reply':reply,'last_ask':'shit','ask':ask})
         t = loader.get_template('hospital/robot.html')      
         return HttpResponse(t.render(context))
      useMySQL.setCurrentUserPrevAsk('-1')
      useMySQL.setCurrentUserShit(question)
      currentUser = useMySQL.getCurrentUser()
      userForTest = []
      lenForTest = len(currentUser)-1
      for i in range(2,lenForTest):
         userForTest.append(float(currentUser[i]))
      #0:哮喘;1:感冒;2:气管炎;3:拉肚子;4:消化不良;5:胃炎
      #hospitalTrainSet.txt::1st column:疲劳感；2nd column:体温；3rd column:呼吸感觉；4th column:心跳情况;5th column:胃部感觉;6th column:大便情况  
      hospitalDataMat, hospitalLabels = kNN.file2matrix('/home/xtang/python_web/mysite2/hospital/machine/hospitalTrainSet.txt')
      print 'hospitalDataMat = ', hospitalDataMat
      print 'hospitalLabels = ', hospitalLabels
      #hospitalDataMat, ranges, minVals = kNN.autoNorm(hospitalDataMat)
      result = kNN.classify0(userForTest, array(hospitalDataMat), hospitalLabels, 3)
      print 'result = ', result
     
      if result==0:
         reply = "我们认为您得了哮喘,并已经把这一诊断结果帮您输入，请直接点击‘提交你的问题’"
         ask = '哮喘'
      elif result==1:
         reply = "我们认为您得了感冒,并已经把这一诊断结果帮您输入，请直接点击‘提交你的问题’"
         ask = '感冒'
      elif result==2:
         reply = "我们认为您得了气管炎,并已经把这一诊断结果帮您输入，请直接点击‘提交你的问题’"
         ask = '气管炎'
      elif result==3:
         reply = "我们认为您得了拉肚子,并已经把这一诊断结果帮您输入，请直接点击‘提交你的问题’"
         ask = '拉肚子'
      elif result==4:
         reply = "我们认为您得了消化不良,并已经把这一诊断结果帮您输入，请直接点击‘提交你的问题’"
         ask = '消化不良'
      elif result==5:
         reply = "我们认为您得了胃炎,并已经把这一诊断结果帮您输入，请直接点击‘提交你的问题’" 
         ask = '胃炎'
      t = loader.get_template('hospital/robot.html')
      context = Context({'reply':reply,'last_ask':'','ask':ask})         
      return HttpResponse(t.render(context))
  
   return render(request, 'hospital/robot.html')
   

   
