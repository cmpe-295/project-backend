from django.conf.urls import patterns, url

urlpatterns = patterns('core.views',
                       url(r'^list_drivers/$', 'list_drivers'),
                       url(r'^client_sign_up/$', 'client_sign_up'),
                       url(r'^activate_app/(?P<activation_string>.+)/$', 'activate_app'),
                       url(r'^get_info/$', 'get_info'),
                       url(r'^update_device_token/$', 'update_device_token'),
                       url(r'^update_client_token/$', 'update_client_token'),
                       url(r'^monitor/$', 'monitor'),
                       url(r'^get_info/$', 'get_info'),
                       url(r'', 'home')
                       )