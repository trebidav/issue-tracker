from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Category(models.Model):
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=300)

class Issue(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=64)
	description = models.CharField(max_length=300)
	category = models.ForeignKey()
	date_created = models.DateTimeField(auto_now=False, auto_now_add=True)
	

