from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
                       url(r'lab2/$', 'store_lab_2'),
                       )