from django.conf.urls import url
from . import views

app_name = 'chat'
urlpatterns = [  
     url(r'^$', views.register, name='register'),  
     url(r'^signup', views.signup, name='signup'), 
     url(r'^login', views.login, name='login'),
     url(r'^log2', views.log2, name='log2'),
     url(r'^index', views.index, name='index'), 
     url(r'^logError', views.logError, name='logError'),  
     url(r'^indAbout', views.indAbout, name='indAbout'), 
     url(r'^docs', views.docs, name='docs'), 
     url(r'^ask', views.ask, name='ask'), 
     url(r'^reply', views.reply, name='reply'),      
]
