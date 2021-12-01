from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy
from .utility import * 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin



############################## VIEWS GERAIS ##############################

def AllSchedules(request):
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

def AllSchedulesMaster(request, master):
    print (master)
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
            return render(request, 'registrations/lists/fullschedulemaster.html',data)
            
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
    return render(request, 'registrations/lists/fullschedulemaster.html',data)


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
    fields = ['name', 'time', 'price']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-procedure')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url


class AppointmentCreate(CreateView):
    #login_url = reverse_lazy('')
    #fields = '__all__'
    model = Appointment
    fields = ['appdate','apphour','professional','client','procedure','status','payed' ]
    template_name = 'registrations/forms_appointment.html'
    success_url = reverse_lazy('myschedule')

    def get_initial(self):
        professional = User()
        client = Client()
        try:
            professional =  User.objects.get(id=self.request.GET.get('professional'))
            client =  Client.objects.get(id=self.request.GET.get('client'))
        except:
            None
        return {
            'appdate':self.request.GET.get('appdate'),
            'apphour':self.request.GET.get('apphour'),
            'client':client,
            'professional':professional,
        }

    def get_form(self, *args, **kwargs):
        form = super(AppointmentCreate, self).get_form(*args, **kwargs)
        form.fields['professional'].queryset = User.objects.filter(master = self.request.user.master, professional = True, is_active = 1)
        form.fields['client'].queryset = Client.objects.filter(master = self.request.user.master, is_active = 1)
        form.fields['procedure'].queryset = Procedure.objects.filter(master = self.request.user.master, is_active = 1)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url


class ScheduleCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-schedule')


    def get_form(self, *args, **kwargs):
        form = super(ScheduleCreate, self).get_form(*args, **kwargs)
        form.fields['professional'].queryset = User.objects.filter(professional = True, master= self.request.user.master)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url


class DayOffCreate(CreateView):
    #login_url = reverse_lazy('')
    model = DayOff
    #fields = ['professional', 'daydate', 'reason','active']
    fields = ['professional','daydate','reason']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-dayoff')

    def get_form(self, *args, **kwargs):
        form = super(DayOffCreate, self).get_form(*args, **kwargs)
        form.fields['professional'].queryset = User.objects.filter(professional = True, master= self.request.user.master)
        return form

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url


class UserCreate(CreateView):
    #login_url = reverse_lazy('')
    model = User
    fields = ['first_name','username','email','tel','professional']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-user')

    def get_initial(self):
        return {
            "hint_id_username": "",
        }

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url


class ClientCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Client
    fields = ['name','tel','birth','cpf','email','obs']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-client')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url

 #############################  UPDATE  #############################

class ProcedureUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-procedure')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Procedure, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class AppointmentUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields =  ['appdate','apphour','client','professional','status','procedure','payed' ]
    template_name = 'registrations/forms_appointment.html'
    success_url = reverse_lazy('myschedule')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Appointment, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class ScheduleUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-schedule')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Schedule, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class DayOffUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = ['professional', 'daydate', 'reason']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-dayoff')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(DayOff, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class UserUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = User
    fields = ['first_name','username','email','tel']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-user')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(User, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class ClientUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Client
    fields = ['name','tel','birth','cpf','email','obs']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-client')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Client, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


#############################  DELETE  #############################

class ProcedureDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-procedure')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class AppointmentDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('myschedule')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class ScheduleDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-schedule')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class DayOffDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-dayoff')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class UserDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = User
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-user')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class ClientDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Client
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-client')

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)




#############################  LIST  #############################
class ProcedureList(ListView):
    #login_url = reverse_lazy('login')
    model = Procedure
    template_name = 'registrations/lists/procedure.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = Procedure.objects.filter(master= self.request.user.master,name__icontains = self.request.GET.get('search'), is_active = 1).order_by('name')
        else:
            self.object_list = Procedure.objects.filter(master= self.request.user.master, is_active = 1).order_by('name')
        return self.object_list


class AppointmentList(ListView):
    #login_url = reverse_lazy('login')
    model = Appointment
    template_name = 'registrations/lists/appointment.html'

    def get_queryset(self):
        self.object_list = Schedule.objects.filter(master= self.request.user.master, is_active = 1)
        return self.object_list




class ScheduleList(ListView):
    #login_url = reverse_lazy('login')
    model = Schedule
    template_name = 'registrations/lists/schedule.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = Schedule.objects.filter(master= self.request.user.master, professional__first_name__icontains = self.request.GET.get('search'), is_active = 1).order_by('professional__first_name')
        else:
            self.object_list = Schedule.objects.filter(master= self.request.user.master, is_active = 1).order_by('professional__first_name')
        return self.object_list

class DayOffList(ListView):
    #login_url = reverse_lazy('login')
    model = DayOff
    template_name = 'registrations/lists/dayoff.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = DayOff.objects.filter(master= self.request.user.master, professional__first_name__icontains = self.request.GET.get('search'), is_active = 1).order_by('professional__first_name')
        else:
            self.object_list = DayOff.objects.filter(master= self.request.user.master, is_active = 1).order_by('professional__first_name')
        return self.object_list

    
class UserList(ListView):
    #login_url = reverse_lazy('login')
    model = User
    template_name = 'registrations/lists/users.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = User.objects.filter(master= self.request.user.master,first_name__icontains = self.request.GET.get('search'), is_active = 1).order_by('first_name')
        else:
            self.object_list = User.objects.filter(master= self.request.user.master, is_active = 1).order_by('first_name')
        return self.object_list


class ClientList(ListView):
    #login_url = reverse_lazy('login')
    model = Client
    template_name = 'registrations/lists/client.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = Client.objects.filter(master= self.request.user.master,name__icontains = self.request.GET.get('search'), is_active = 1).order_by('name')
        else:
            self.object_list = Client.objects.filter(master= self.request.user.master, is_active = 1).order_by('name')
        return self.object_list



