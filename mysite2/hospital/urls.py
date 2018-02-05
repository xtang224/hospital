from django.conf.urls import url
from . import views

app_name = 'hospital'
urlpatterns = [  
     url(r'^$', views.index, name='index'),     
     url(r'^index', views.index, name='index'),      
     url(r'^search', views.search, name='search'),  
     url(r'^respire/asthma', views.asthma, name='asthma'),
     url(r'^respire/cold', views.cold, name='cold'),
     url(r'^respire/qiguanyan', views.qiguanyan, name='qiguanyan'),   
     url(r'^digest/laduzi', views.laduzi, name='laduzi'),   
     url(r'^digest/illDigest', views.illDigest, name='illDigest'),
     url(r'^digest/stomachIll', views.stomachIll, name='stomachIll'),  
     url(r'^robot', views.robot, name='robot'),
     url(r'^ask', views.ask, name='ask'),                                
]
