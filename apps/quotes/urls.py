from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^users/(?P<id>\d+)$', views.users),
    url(r'^add_quote$', views.add_quote),
    url(r'^add_fave$', views.add_fave),
    url(r'^remove_quote$', views.remove_quote),    
]
