from django.http import request
from django.shortcuts import render
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy
from .utility import * 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



############################## VIEWS GERAIS ##############################

def FullSchedule(request):
    data={}
    pass
    return render(request, 'registrations/lists/myschedule.html',data)

def FullScheduleMaster(request, master):
    data = {
        'feriados':{},
        'free':{},
    }

    print(master)
    if (request.GET.get('date')):
        data['date'] = request.GET.get('date')
        date = Time().convertdate(request.GET.get('date'))
    else:
        data['date'] = datetime.today().strftime('%Y-%m-%d')
        date = datetime.today().strftime('%d/%m/%Y')
    schedule = []
    busy = []
    free = []
    weekday = Time().convertweekday(date)

    try:
        data['feriados'] = DayOff.objects.filter(daydate = date).filter(professional=request.user.id)
        schedule = Schedule.objects.filter(professional=request.user.id).filter(weekday=weekday)
        busy = Appointment.objects.filter(professional=request.user.id).filter(appdate = date)
    except:
        pass


    if len(data['feriados']) >= 1 and request.user.is_staff==False:
            return render(request, 'registrations/lists/myschedule.html',data)
            
    busy = list(busy)
    busyclient = []
    for i in schedule:
        free += Time().FreeSchedule(i,busy)
    for i in free:
        app = Appointment()
        app.apphour = i
        app.appdate = date
        app.professional = request.user
        busyclient.append(app)
    busy += busyclient
    busy = sorted(busy,key = lambda x: x.apphour)
    data['free']=busy
    return render(request, 'registrations/lists/myschedule.html',data)



def MySchedule(request): #VIEW ONDE BUSCA OS HORÁRIOS DO PROFISSIONAL LOGADO.
    data = {
        'feriados':{},
        'free':{},
    }
    if (request.GET.get('date')):
        data['date'] = request.GET.get('date')
        date = Time().convertdate(request.GET.get('date'))
    else:
        data['date'] = datetime.today().strftime('%Y-%m-%d')
        date = datetime.today().strftime('%d/%m/%Y')
    schedule = []
    busy = []
    free = []
    weekday = Time().convertweekday(date)

    try:
        data['feriados'] = DayOff.objects.filter(daydate = date).filter(professional=request.user.id)
        schedule = Schedule.objects.filter(professional=request.user.id).filter(weekday=weekday)
        busy = Appointment.objects.filter(professional=request.user.id).filter(appdate = date)
    except:
        pass


    if len(data['feriados']) >= 1 and request.user.is_staff==False:
            return render(request, 'registrations/lists/myschedule.html',data)
            
    busy = list(busy)
    busyclient = []
    for i in schedule:
        free += Time().FreeSchedule(i,busy)
    for i in free:
        app = Appointment()
        app.apphour = i
        app.appdate = date
        app.professional = request.user
        busyclient.append(app)
    busy += busyclient
    busy = sorted(busy,key = lambda x: x.apphour)
    data['free']=busy
    return render(request, 'registrations/lists/myschedule.html',data)




#############################  CREATE  #############################

class ProcedureCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-procedure')


class StatusCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Status
    fields = ['name','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-status')


class PaymentCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Payment
    fields = ['name', 'discount', 'tax','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-payment')


class AppointmentCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields = ['appdate','apphour','client','professional','status','procedure','payment' ]
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('myschedule')


class ScheduleCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-schedule')


class DayOffCreate(CreateView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = ['professional', 'daydate', 'reason','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-dayoff')

 #############################  UPDATE  #############################

class ProcedureUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-procedure')


class StatusUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Status
    fields = ['name','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-status')


class PaymentUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Payment
    fields = ['name', 'discount', 'tax','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-payment')


class AppointmentUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields =  ['appdate','apphour','client','professional','status','procedure','payment' ]
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('myschedule')


class ScheduleUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-schedule')


class DayOffUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = ['professional', 'daydate', 'reason','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-dayoff')


#############################  DELETE  #############################

class ProcedureDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-procedure')


class StatusDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Status
    fields = ['name','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-status')


class PaymentDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Payment
    fields = ['name', 'discount', 'tax','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-payment')


class AppointmentDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields = ['client','professional','status','procedure','payment' ]
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('myschedule')


class ScheduleDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-schedule')


class DayOffDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = ['professional', 'daydate', 'reason','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-dayoff')


#############################  LIST  #############################
class ProcedureList(ListView):
    #login_url = reverse_lazy('login')
    model = Procedure
    template_name = 'registrations/lists/procedure.html'


class StatusList(ListView):
    #login_url = reverse_lazy('login')
    model = Status
    template_name = 'registrations/lists/status.html'


class PaymentList(ListView):
    #login_url = reverse_lazy('login')
    model = Payment
    template_name = 'registrations/lists/payment.html'


class AppointmentList(ListView):
    #login_url = reverse_lazy('login')
    model = Appointment
    template_name = 'registrations/lists/appointment.html'


class ScheduleList(ListView):
    #login_url = reverse_lazy('login')
    model = Schedule
    template_name = 'registrations/lists/schedule.html'
    

class DayOffList(ListView):
    #login_url = reverse_lazy('login')
    model = DayOff
    template_name = 'registrations/lists/dayoff.html'
    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = DayOff.objects.filter(reason__contains = self.request.GET.get('search'))
        else:
            self.object_list = DayOff.objects.all()
        return self.object_list




