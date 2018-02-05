from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible  #only if you need to support python 2
class User(models.Model):
   phone = models.CharField(max_length=20)
   passwd = models.CharField(max_length=20)
   def __str__(self):
      return self.phone

@python_2_unicode_compatible  #only if you need to support python 2
class Pair(models.Model):
   englishWord = models.CharField(max_length=20)
   chineseWord = models.CharField(max_length=20)
   def __str__(self):
      return self.englishWord
	  
@python_2_unicode_compatible  #only if you need to support python 2
class Person(models.Model):
   phone = models.CharField(max_length=20)
   question = models.CharField(max_length=200)
   reply = models.CharField(max_length=200)
   def __str__(self):
      return self.phone	  

