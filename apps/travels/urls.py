from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^add$', views.show_add, name='show_add'),
	url(r'^add/process/(?P<id>\d+)$', views.create, name='create'),
	url(r'^trip/(?P<id>\d+)$', views.show_trip, name='show_trip'),
	url(r'^trip/(?P<id>\d+)/join$', views.join, name='join'),
]
