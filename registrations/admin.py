from registrations.models import Procedure
from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(Procedure)
admin.site.register(Appointment)
admin.site.register(DayOff)
admin.site.register(Schedule)
admin.site.register(Client)

