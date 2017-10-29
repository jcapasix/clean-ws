from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.template.defaultfilters import slugify


# Create your models here.
class TimeStampModel(models.Model):
	created = models.DateTimeField(auto_now_add=True)
	modified = models.DateTimeField(auto_now_add=True)
	is_active = models.BooleanField(default=True)
	#al momento de crearla no se creara como una tabla
	class Meta:
		abstract =True

class UserManager(BaseUserManager):
	def _create_user(self, username, email, password, is_active,is_staff, is_superuser, **extra_fields):
		#if not email:
			#raise ValueError('El email debe ser obligatorio')
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, is_active=is_active, is_staff=is_staff, is_superuser=is_superuser, **extra_fields)
		user.set_password(password)
		user.save(using=self.db)
		return user

	def create_user(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password,True, False, False, **extra_fields)
	def create_user_email(self, username, email, password=None, **extra_fields):
		return self._create_user(username, email, password,False, False, False, **extra_fields)
	def create_superuser(self, username, email, password, **extra_fields):
		return self._create_user(username, email, password,True, True, True, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(max_length=50, unique=True)
	email = models.EmailField(max_length=75, unique=False)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
		
	status = models.BooleanField(default=False)
	objects = UserManager()

	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)

	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']
	

	def get_short_name(self):
		return self.username

	def __unicode__(self): 
		return "%s" % (self.username)