from django.contrib import admin
from .models import Cardiologist
from .models import Patient
from .models import Appointment
from .models import Test
from .models import Nurse

class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('cardiologist','patient')
admin.site.register(Cardiologist)
admin.site.register(Patient)
admin.site.register(Appointment,AppointmentAdmin)
admin.site.register(Test)
admin.site.register(Nurse)