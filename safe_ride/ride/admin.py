from django.contrib import admin

# Register your models here.
from .models import Ride, DriverLocation


class RideAdmin(admin.ModelAdmin):
    list_display = ("client", "request_received_at", "initial_eta", "serviced_by", "active", "deleted")
    list_display_links = ("client", "request_received_at", "initial_eta", "serviced_by", "active", "deleted")
    ordering = ("-request_received_at", )
    list_filter = ("client", "serviced_by")


admin.site.register(Ride, RideAdmin)


class DriverLocationAdmin(admin.ModelAdmin):
    list_display = ("driver", "latitude", "longitude", "timestamp", "latest")
    list_display_links = ("driver", "latitude", "longitude", "timestamp", "latest")
    ordering = ("-timestamp", )
    list_filter = ("driver", "latest")


admin.site.register(DriverLocation, DriverLocationAdmin)
