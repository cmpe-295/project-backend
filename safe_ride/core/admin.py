from django.contrib import admin

# Register your models here.
from .models import Client, Driver, SiteUser

admin.site.register(Client)
admin.site.register(Driver)
admin.site.register(SiteUser)
