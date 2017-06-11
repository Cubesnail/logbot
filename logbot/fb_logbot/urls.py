#logbot/fb_logbot/urls.py

from django.conf.urls import include, url
from .views import logbot_view
urlpatterns = [ 
                url(r'^abcdef/?$', logbot_view.as_view())
]

