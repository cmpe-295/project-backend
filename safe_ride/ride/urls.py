from django.conf.urls import patterns, url

urlpatterns = patterns('ride.views',
                       url(r'request/$', 'request_ride', name="request_ride"),
                       url(r'cancel/$', 'cancel_ride', name="cancel_ride"),
                       url(r'update_driver_location/$', 'update_driver_location', name="update_driver_location"),
                       url(r'update_client_location/$', 'update_client_location', name="update_client_location"),
                       url(r'^update_client_token/$', 'update_client_token'),
                       url(r'pickup_client/$', 'pickup_client', name="pickup_client"),
                       url(r'drop_client/$', 'drop_client', name="drop_client"),
                       url(r'get_driver_location/$', 'get_driver_location', name="get_driver_location"),
                       url(r'get_current_route/$', 'get_current_route', name="get_current_route")
                       )
