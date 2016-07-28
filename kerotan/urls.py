from django.conf.urls import url
from kerotan import views


urlpatterns = [
    url(r'^$', views.display_google_map, name='display_google_map'),
]
