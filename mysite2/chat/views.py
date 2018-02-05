#!/usr/bin/env python
#coding=utf8

from django.shortcuts import render, render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext, loader, Context
from chat.models import User,Pair, Person

import logging

import numpy as np
import cv2
import sqlite3
import redis

#from settings import Logging
#logger = LOGGING.getLogger('mylogger')
# Create your views here.

def  distance(pic1, pic2):
   w1 = pic1.size   
   w2 = pic2.size
   tPic1 = pic1.reshape(1,w1)
   tPic2 = pic2.reshape(1,w2)
   ret = 0
   minW = min(w1,w2)
   for i in range(minW):
      ret += tPic1[0,i]
   ret2 = 0
   for i in range(minW):
      ret2 += tPic1[0,i]  
   
   return (ret2-ret)*(ret2-ret)
   
def  getEmotion(oriImg):   
   imgs = ['pics/anger.jpg', 'pics/disgust.jpg', 'pics/fear.jpg', 'pics/happy.jpg', 'pics/sad.jpg', 'pics/surprise.jpg']   
   emotions = ["anger", "disgust", "fear", "happy", "sad", "surprise"]
   #print emotions
   minDist = 1000000
   emotion = ''
   for i in range(len(imgs)):
      tmpImg = cv2.imread(imgs[i])   
      dist = distance(oriImg, tmpImg)
      if dist<minDist:
         minDist = dist
         emotion = emotions[i]
   return emotion

def register(request):
   phonenumber = request.POST['phone']
   password = request.POST['passwd2']
   user = User(phone=phonenumber, passwd=password)
   user.save();
   return render(request, 'chat/login.html')
   #return HttpResponseRedirect('login.html')

def signup(request):
   return render(request, 'chat/signup.html')
   #return HttpResponseRedirect('signup.html')

def login(request):
   return render( request, 'chat/login.html')

def log2(request):
   phonenumber = request.POST['phone']
   password = request.POST['passwd2']
   user = User.objects.get(phone=phonenumber)
   print("user.phone=", phonenumber, " and user.passwd=", password)
   logging.debug(phonenumber)
   PHONE = user.phone  #here, PHONE is a global variable defined in the settings.py
 
   t = loader.get_template('chat/index.html')
   context = Context({'reply':"",'phone':phonenumber})
   
   #we want to start camera here
   cam = cv2.VideoCapture(0)
   #while 1:
   _, img = cam.read()
   cv2.imshow("pic", img)
   cv2.imwrite('myPic.bmp', img)
   cv2.waitKey(30) & 0xff
   
   if user.passwd==password:
       logging.debug("login success")
       return HttpResponse(t.render(context))
       #return HttpResponse("login success")
       #return render_to_response(request, 'chat/index.html', context)
   else:
      logging.debug("login unsuccess")
      #return HttpResponse("login NOT success")
      return render(request, 'chat/logError.html')

def index(request):
   return render(request, 'chat/index.html')

def logError(request):
   return render(request, 'chat/logError.html')

def indAbout(request):
   return render(request, 'chat/indAbout.html')

def docs(request):
   return render(request, 'chat/docs.html')

def ask(request):
   question2 = request.GET['dialogue_question']
   dialogue_bid = request.GET['dialogue_bid']
   dialogue_uid = request.GET['dialogue_uid']
   idTab = request.GET['idTab']
   dialogue_user_phone = request.GET['dialogue_user_phone']
   dialogue_reply = request.GET['dialogue_reply']
   #dialogue_user_phone = PHONE 
   user = User.objects.get(phone=dialogue_user_phone)
   password = user.passwd
   
   #conn = sqlite3.connect("D:\\python_web\\mysite2\\db.sqlite3")
   #conn = sqlite3.connect("/run/media/xtang/84E42A26E42A1AC6/python_web/mysite2/db.sqlite3")
   conn = sqlite3.connect("/home/xtang/python_web/mysite2/db.sqlite3")
   cur = conn.cursor()
   if int(idTab)==0:
      #cur.execute("delete from chat_person where phone=?", (dialogue_user_phone))
      print "in 0, idTab = ", idTab
      #cur.execute("insert into chat_person(phone,question,reply) values('1111','','')")
      person = Person(phone=dialogue_user_phone,question=question2,reply=dialogue_reply)
      person.save()
      #r = redis.Redis(host='localhost', port=6379, db=1)
      #r[dialogue_user_phone] = question2
      #r.shutdown()
   else:
      print "in 1, idTab = ", idTab
      #cur.execute("update chat_person set reply=? where phone=?", (dialogue_reply, dialogue_user_phone))
      person = Person(phone=dialogue_user_phone,question=question2,reply=dialogue_reply)
      person.save()
      #r = redis.Redis(host='localhost', port=6379, db=1)
      #question3 = r.get(dialogue_user_phone)
      #r[dialogue_user_phone] = question3 + "_" + dialogue_reply
      #r.shutdown()
   for englishWord, chineseWord in cur.execute("select englishWord, chineseWord from chat_pair"):
      print englishWord, chineseWord
   for phone, question,reply in cur.execute("select phone, question,reply from chat_person"):
      print phone, question, reply
   
   #we want to start camera here
   cam = cv2.VideoCapture(0)
   _, img = cam.read()
   cv2.imshow("pic", img)
   cv2.imwrite('pics/myPic.bmp', img)
   cv2.waitKey(30) & 0xff

   address = 'http://localhost:8080/ReplyServlet?ask=' + question2 + "&dialogue_bid=" + dialogue_bid + "&dialogue_uid=" + dialogue_uid + "&idTab=" + idTab + "&phone=" + dialogue_user_phone + "&password=" + password + "&reply=" + dialogue_reply
   return HttpResponseRedirect(address)

def reply(request):
   phonenumber = request.GET['phone']
   reply = request.GET['reply']
   user = User.objects.get(phone=phonenumber)
   password = user.passwd
   #context = RequestContext(request,{'reply':reply})
   t = loader.get_template('chat/index.html')

   oImg = cv2.imread('pics/myPic.bmp')
   myEmotion = getEmotion(oImg)
   #myEmotion = 'anger'
   pair = Pair.objects.get(englishWord=myEmotion)
   reply +=  pair.chineseWord
   context = Context({'reply':reply,'phone':phonenumber})

   return HttpResponse(t.render(context))
   

   
