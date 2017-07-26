from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^login$', views.login),
    url(r'^register$', views.register),
    url(r'^secrets$', views.secrets),
    url(r'^logout$', views.logout),
    url(r'^post$', views.post),
    url(r'^like/(?P<id>\d+)$', views.like),
    url(r'^unlike/(?P<id>\d+)$', views.unlike),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^popular$', views.popular),
    url(r'^addfriend/(?P<id>\d+)$', views.addfriend),
    url(r'^delfriend/(?P<id>\d+)$', views.delfriend),
]
