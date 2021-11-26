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
    data['datec'] = date
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
        app.status = ""
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
    #fields = '__all__'
    model = Appointment
    fields = ['appdate','apphour','client','professional','procedure','status','payed' ]
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('myschedule')
    usuario = User.objects.get(id=1)
    initial = {
        'appdate': '',
    }
    
    def get_form(self, *args, **kwargs):
        form = super(AppointmentCreate, self).get_form(*args, **kwargs)
        form.fields['professional'].queryset = User.objects.filter(id = self.request.user.id)
        # form.fields['b_a'].queryset = A.objects.filter(a_user=self.request.user) 
        return form

'''class StudentCreateView(CreateView):
    fields = ("name","age","school")
    model = models.Student
    template_name = 'basic_app/student_form.html'

    pk_url_kwarg = 'student_pk'
    slug_url_kwarg='school'
    def get_initial(self):
        school = get_object_or_404(models.School, school_pk=self.kwargs.get('school_pk'))
        return {
        'school':school,
    }'''



class ScheduleCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-schedule')


class DayOffCreate(CreateView):
    #login_url = reverse_lazy('')
    model = DayOff
    #fields = ['professional', 'daydate', 'reason','active']
    fields = '__all__'
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-dayoff')

class UserCreate(CreateView):
    #login_url = reverse_lazy('')
    model = User
    fields = ['first_name','username','email','tel','professional']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-user')

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
    fields =  ['appdate','apphour','client','professional','status','procedure','payed' ]
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

class UserUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = User
    fields = ['first_name','username','email','tel','professional']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-user')


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

class UserDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = User
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-user')

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
            self.object_list = DayOff.objects.filter(reason__icontains = self.request.GET.get('search'))
        else:
            self.object_list = DayOff.objects.all()
        return self.object_list

    
class UserList(ListView):
    #login_url = reverse_lazy('login')
    model = User
    template_name = 'registrations/lists/users.html'



