from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Cardiologist
from .models import Appointment
from .models import Patient
from .models import Test
from .models import Nurse
import json
from datetime import datetime


def show_status(date,time):
   if(date>datetime.now().date()):
        return 'In progress'
   if(date< datetime.now().date()):
        return 'Done'
   if(date==datetime.now().date() and time >datetime.now().time()):
        return 'Today'
   if(date==datetime.now().date() and time <datetime.now().time()):
        return 'Done'
   else:
        return 'Done'
    
def show_color(status):
    if(status =='In progress'):
        return 'primary'
    if(status == 'Today'):
        return 'danger'
    if(status =='Done'):
        return 'secondary'
    if(status =='Not Ready'):
        return 'secondary'
    if(status=='Ready'):
        return 'success'
    if(status=='Completed'):
        return 'primary'
    else:
        return 'secondary'
    
def get_context(tab1='',tab2='',tab3='',tab4='',tab5=''):
    flatten_spec = list()
    for i in Cardiologist.SPECIALIZATIONS:
        flatten_spec.append(i[1])
    
    cardiologists = Cardiologist.objects.all().values()
    for c in cardiologists:
        if (c['gender']=='f'):
            c['gender']='Female'
        else:
            c['gender']='Male'
        for i in flatten_spec:
           if i[0]==c['specialization'] :
              c['specialization'] = i
    patients = Patient.objects.all().values()
    appointments = Appointment.objects.all()
    flatten_app = list(list())
    for app in appointments:
        obj = list()
        obj.append(app.patient.name)
        obj.append(app.cardiologist.name)
        obj.append(app.due_date)
        obj.append(app.due_time)
        obj.append(show_status(app.due_date,app.due_time))
        obj.append(show_color(show_status(app.due_date,app.due_time)))
        flatten_app.append(obj)
    tests = Test.objects.all().order_by('id')
    flatten_tests = list(list())
    for test in tests:
        obj = list()
        obj.append(test.name)
        obj.append(test.cardiologist.name)
        obj.append(test.patient.name)
        obj.append(test.cost)
        obj.append(test.status)
       
        obj.append(show_color(test.status))
        flatten_tests.append(obj)
    patients_without_nurse = Patient.objects.filter(nurse=None).values()
    nurses = Nurse.objects.all().order_by('id').values()
    patientsRecords = Patient.objects.all().order_by('id')
    nursesPatients = list(list())
    for p in patientsRecords:
        if (p.nurse is not None):
            obj = list()
            obj.append(p.nurse.name)
            obj.append(p.nurse.age)
            obj.append(p.nurse.phone_number)
            obj.append(p.name)
            nursesPatients.append(obj)
    
    context={
       'specialization':flatten_spec,
       'cardiologists':cardiologists,
       'patients':patients,
       'appointments':flatten_app,
       'tests':flatten_tests,
       'patients_without_nurse':patients_without_nurse,
       'nurses':nurses,
       'nursesPatients':nursesPatients,
       'tab1':tab1,
       'tab2':tab2,
       'tab3':tab3,
       'tab4':tab4,
       'tab5':tab5,
    }
    return context

def main(request):
    template = loader.get_template('main.html')
    context = get_context(tab1='active')
    return HttpResponse(template.render(context,request))
def editNurse(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        age = request.POST['age']
        patients = list(str(request.POST['patients']).removeprefix('[').removesuffix(']').split(','))
        phonenumber = request.POST['phonenumber']
        nurse_id = int(request.POST['id'])-1
        if(not(bool(name)) or not(bool(patients)) or not(bool(phonenumber))):
           return HttpResponse('please, Fill the mandatory fields')
        ALREADY_EXISTS = bool(Nurse.objects.filter(name =name).values())
        similar_name_count = Nurse.objects.filter(name__contains = name).count()
        nurseRecord = Nurse.objects.order_by('id')[nurse_id]
        if (not ALREADY_EXISTS):
            nurseRecord.name = name
        
        nurseRecord.age = age
        nurseRecord.phone_number = phonenumber
        nurseRecord.save()
        #reset patients of old nurse
        patients_records = Patient.objects.filter(nurse = nurseRecord).all()
        for p in patients_records:
            # set to none
            p.nurse = None
            p.save()
        # update patients
        for p in patients:
            try:
                patientRecord = Patient.objects.get(name=p)
                patientRecord.nurse = nurseRecord
                patientRecord.save()
            except:
                continue;
     
    return HttpResponse('Successfully edited')
def addTest(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        patientName = request.POST['patientName']
        cardiologistName = request.POST['cardiologistName']
        cost = request.POST['cost']
        status = request.POST['status']
        if(not(bool(name)) or not(bool(cost)) or not(bool(patientName)) or not(bool(cardiologistName))):
             return HttpResponse('please, Fill the mandatory fields')
        ALREADY_EXISTS = bool(Test.objects.filter(name =name).values())
        similar_name_count = Test.objects.filter(name__contains = name).count()
        cardiologist = Cardiologist.objects.filter(name = cardiologistName).first()
        patient = Patient.objects.filter(name = patientName).first()
        testRecord = Test.objects.create()
        if (ALREADY_EXISTS):
            testRecord.name = name+str(similar_name_count+1)
        else:
            testRecord.name =name
        testRecord.patient =patient
        testRecord.cost=cost
        testRecord.cardiologist = cardiologist
        testRecord.status = status
        testRecord.save()
        return HttpResponse('Successfully created')
def editTest(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        patientName = request.POST['patientName']
        cardiologistName = request.POST['cardiologistName']
        cost = request.POST['cost']
        status = request.POST['status']
        test_id = int(request.POST['id'])-1
        if(not(bool(name)) or not(bool(cost)) or not(bool(patientName)) or not(bool(cardiologistName))):
             return HttpResponse('please, Fill the mandatory fields')
        ALREADY_EXISTS = bool(Test.objects.filter(name =name).values())
        similar_name_count = Test.objects.filter(name__contains = name).count()
       
        cardiologist = Cardiologist.objects.filter(name = cardiologistName).first()
        patient = Patient.objects.filter(name = patientName).first()   
        testRecord = Test.objects.order_by('id')[test_id]
        if (not ALREADY_EXISTS):
             testRecord.name =name
        testRecord.patient =patient
        testRecord.cost= cost
        testRecord.cardiologist = cardiologist
        testRecord.status = status
        testRecord.save()
        return HttpResponse('Successfully edited')
def addCardiologist(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        gender = request.POST['gender']
        experience = request.POST['experience']
        spec = request.POST['specialization']
        phonenumber = request.POST['phonenumber']
        briefInfo = request.POST['briefInfo']
        age = request.POST['age']
        if(not bool(name)):
           return HttpResponse('please, Enter the cardiologist name')
        ALREADY_EXISTS = bool(Cardiologist.objects.filter(name =name).values())
        if (ALREADY_EXISTS):
            return HttpResponse('This name already exists, please choose another one')
        cardiologistRecord = Cardiologist.objects.create()
        cardiologistRecord.name = name
        cardiologistRecord.age = age
        cardiologistRecord.gender = gender
        cardiologistRecord.experience = experience
        cardiologistRecord.brief_info =briefInfo
        cardiologistRecord.specialization = spec[0]
        cardiologistRecord.phone_number = phonenumber
        cardiologistRecord.save()
        return HttpResponse("Successfully created")
def addNurse(request):
    if (request.method == 'POST'):
        name = request.POST['name']
        age = request.POST['age']
        patients = list(str(request.POST['patients']).removeprefix('[').removesuffix(']').split(','))
        phonenumber = request.POST['phonenumber']
        if(not(bool(name)) or not(bool(patients)) or not(bool(phonenumber))):
           return HttpResponse('please, Fill the mandatory fields')
        ALREADY_EXISTS = bool(Nurse.objects.filter(name =name).values())
        similar_name_count = Nurse.objects.filter(name__contains = name).count()
        nurseRecord = Nurse.objects.create()
        if (ALREADY_EXISTS):
            nurseRecord.name = name+str(similar_name_count+1)
        else:
            nurseRecord.name =name
        nurseRecord.age = age
        nurseRecord.phone_number = phonenumber
        nurseRecord.save()
        for p in patients:
            try:
                patientRecord = Patient.objects.get(name=p)
                patientRecord.nurse = nurseRecord
                patientRecord.save()
            except:
                continue
     
    return HttpResponse('Successfully created')
def addAppointment(request):
     if (request.method == 'POST'):
        name = request.POST['name']
        gender = request.POST['gender']
        dueDate = request.POST['dueDate']
        cardiologistName = request.POST['cardiologistName']
        phonenumber = request.POST['phonenumber']
        dueTime = request.POST['dueTime']
        age = request.POST['age']
        medicalHistory = request.POST['medicalHistory']
        patientInsurance = request.POST['patientInsurance']
        if(not(bool(name)) or not(bool(dueDate)) or not(bool(dueTime)) or not(bool(cardiologistName))):
           return HttpResponse('please, Fill the mandatory fields')
        dueTime = datetime.strptime(dueTime,'%H:%M')
        dueDate = datetime.strptime(dueDate,'%Y-%m-%d')
        ALREADY_EXISTS = bool(Appointment.objects.filter(due_date = dueDate.date() ,due_time = dueTime.time()).values())
        if (ALREADY_EXISTS):
            return HttpResponse('This appointment is already taken, please choose another time or date')
        similar_name_count = Patient.objects.filter(name__contains = name).count()
        patient = Patient.objects.create()
        if (similar_name_count > 0):
            patient.name = name+str(similar_name_count+1)
        else:
            patient.name =name
        patient.age = age
        patient.gender = gender
        patient.insurance_details = patientInsurance
        patient.medical_history = medicalHistory
        patient.phone_number = phonenumber
        patient.save()
        cardiologist = Cardiologist.objects.filter(name = cardiologistName).first()
        appointmentRecord = Appointment.objects.create()
        appointmentRecord.patient = patient
        appointmentRecord.cardiologist = cardiologist
        appointmentRecord.due_date = dueDate.date()
        appointmentRecord.due_time = dueTime.time()
        appointmentRecord.save()
        return(HttpResponse("Successfully created"))


def activate_tab1(request):
    template = loader.get_template('main.html')
    context = get_context(tab1='active')
    return HttpResponse(template.render(context,request))
def activate_tab2(request):
    template = loader.get_template('main.html')
    context = get_context(tab2='active')
    return HttpResponse(template.render(context,request))

def activate_tab3(request):
    template = loader.get_template('main.html')
    context = get_context(tab3='active')
    return HttpResponse(template.render(context,request))

def activate_tab4(request):
    template = loader.get_template('main.html')
    context = get_context(tab4='active')
    return HttpResponse(template.render(context,request))

def activate_tab5(request):
    template = loader.get_template('main.html')
    context = get_context(tab5='active')
    return HttpResponse(template.render(context,request))





