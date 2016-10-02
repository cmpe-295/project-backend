from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
                       url(r'^list_drivers/$', 'list_drivers'),
                       url(r'^client_sign_up/$', 'client_sign_up'),
                       )