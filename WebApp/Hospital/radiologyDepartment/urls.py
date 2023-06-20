from django.urls import path
from . import views


urlpatterns=[
    path('',views.main,name='main'),
    path('Affiliated-Cardiologists',views.activate_tab1),
    path('Patients',views.activate_tab2),
    path('Appointments',views.activate_tab3),
    path('Tests',views.activate_tab4),
    path('Nurses',views.activate_tab5),
    path('addCardiologist/',views.addCardiologist,name='addCardiologist'),
    path('addAppointment/',views.addAppointment,name='addAppointment'),
    path('addTest/',views.addTest,name='addTest'),
    path('editTest/',views.editTest,name='editTest'),
    path('addNurse/',views.addNurse,name='addNurse'),
    path('editNurse/',views.editNurse,name='editNurse'),
]