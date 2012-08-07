from sdust_oj.admin.views import *
from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',    
    url(r'^$', admin_index , name='admin_index'),
)
