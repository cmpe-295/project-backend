from django.conf.urls import patterns, url

urlpatterns = patterns('ride.views',
                       url(r'request/$', 'request_ride', name="request_ride"),
                       url(r'cancel/$', 'cancel_ride', name="cancel_ride"),
                       url(r'update_driver_location/$', 'update_driver_location', name="update_driver_location"),
                       url(r'update_client_location/$', 'update_client_location', name="update_client_location"),
                       )
