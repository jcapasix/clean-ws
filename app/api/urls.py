from django.conf.urls import include, url
from django.contrib import admin
#from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from app.api import views
from django.conf.urls import url
#from .views import CustomObtainAuthToken


urlpatterns = [

	url(r'^login/$', views.LoginService.as_view()),
	url(r'^register/$', views.RegisterService.as_view()),
	#url(r'^commerce/$', views.CommerceList.as_view()),
]