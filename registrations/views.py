from asyncio.windows_events import NULL
from cgi import print_directory
from django.contrib.auth.decorators import login_required
from django.http import request
from django.http.response import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy
from .utility import * 
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
import random

WEEKDAY = ['Segunda-feira','Terça-feira','Quarta-feira','Quinta-feira','Sexta-feira','Sábado','Domingo']

############################## VIEWS GERAIS ##############################


def AllSchedulesMaster(request, nickmaster):
    print(nickmaster)
    data = {
        'professionals':{},
        'feriados':{},
        'free':{},
    }

    #data['date'] formato yyyy-mm-dddd
    #date formato dd/mm/aaaa
    if (request.GET.get('date')):
        data['date'] = request.GET.get('date')
        date = Time().convertdate(request.GET.get('date'))
    else:
        data['date'] = datetime.today().strftime('%Y-%m-%d')
        date = datetime.today().strftime('%d/%m/%Y')
    data['datec'] = date

    
    busyclient = []
    schedule = []
    busy = []
    free = []
    
    weekday = Time().convertweekday(date)
    data['weekday'] = WEEKDAY[weekday]
    try:
        data['master'] = User.objects.get(nickname = nickmaster)
        data['master'].access_schedules +=1
        data['master'].save()
        if ( data['master'].is_master == True):
            data['professionals'] = User.objects.filter(master = data['master'])
        else:
            data['professionals'] = User.objects.filter(nickname = nickmaster)
    except:
        pass
    for i in data['professionals']:
        try:
            data['feriados'] = DayOff.objects.filter(daydate = date).filter(professional=i).filter(is_active = True)
            schedule = Schedule.objects.filter(professional = i).filter(weekday=weekday).filter(is_active = True).filter(is_shared = 'S')
            busy = Appointment.objects.filter(professional = i, appdate = date).filter(is_active = True)            
            busy = list(busy)
        except:
            pass
        for j in schedule:
            free += Time().FreeSchedule(j,busy)
            for k in free:
                app = Appointment()
                app.apphour = k
                app.appdate = date
                app.professional = i
                app.status = ""
                busyclient.append(app)
    busyclient = sorted(busyclient,key = lambda x: x.apphour)
    data['free']=busyclient
    return render(request, 'registrations/lists/allschedulesmaster.html',data)


@login_required
def AllSchedules( request):
    data = {
        'professionals':{},
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

    #AQUI UTILIZO PARA PASSAR PELOS STATUS USANDO OS BOTOES DA AGENDA
    if(request.GET.get('idappointment') and request.GET.get('newstatus')):
        appointment = Appointment.objects.get(pk = request.GET.get('idappointment'))
        appointment.status = request.GET.get('newstatus')
        if(request.GET.get('newstatus') == '4' and request.GET.get('payedstatus') ):
            appointment.payed = request.GET.get('payedstatus')
        #valida se o usuario que esta pedindo é da mesma empresa que o agendamento
        if (request.user.master == appointment.master):
            appointment.save()


    schedule = []
    busy = []
    free = []
    weekday = Time().convertweekday(date)
    data['weekday'] = WEEKDAY[weekday]
    try:
        data['professionals'] = User.objects.filter(master = request.user.master)
        data['professionaldefault'] = data['professionals'][0]
        
        if(request.GET.get('id_professional')):
            professional = User.objects.get(id = request.GET.get('id_professional'))
            data['professionaldefault'] = professional
        else:
            professional = data['professionals'][0]

        data['feriados'] = DayOff.objects.filter(daydate = date).filter(professional=request.user.id).filter(is_active = True)
        schedule = Schedule.objects.filter(master = request.user.master, professional = professional).filter(weekday=weekday).filter(is_active = True)
        busy = Appointment.objects.filter(master = request.user.master, professional = professional, appdate = date).filter(is_active = True)
        
    except:
        pass

            
    busy = list(busy)
    busyclient = []
    for i in schedule:
        free += Time().FreeSchedule(i,busy)
    for i in free:
        app = Appointment()
        app.apphour = i
        app.appdate = date
        app.professional = professional
        app.status = ""
        busyclient.append(app)
    busy += busyclient
    busy = sorted(busy,key = lambda x: x.apphour)
    data['free']=busy
    return render(request, 'registrations/lists/allschedules.html',data)


@login_required
def MySchedule(request): #VIEW ONDE BUSCA OS HORÁRIOS DO PROFISSIONAL LOGADO.
    data = {
        'feriados':{},
        'free':{},
    }
     #AQUI UTILIZO PARA PASSAR PELOS STATUS USANDO OS BOTOES DA AGENDA
    if(request.GET.get('idappointment') and request.GET.get('newstatus')):
        appointment = Appointment.objects.get(pk = request.GET.get('idappointment'))
        appointment.status = request.GET.get('newstatus')
        if(request.GET.get('newstatus') == '4' and request.GET.get('payedstatus') ):
            appointment.payed = request.GET.get('payedstatus')
        #valida se o usuario que esta pedindo é da mesma empresa que o agendamento
        if (request.user.master == appointment.master):
            appointment.save()

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
    data['weekday'] = WEEKDAY[weekday]

    try:
        data['feriados'] = DayOff.objects.filter(daydate = date).filter(professional=request.user.id)
        schedule = Schedule.objects.filter(professional=request.user.id).filter(weekday=weekday).filter(is_active = True)
        busy = Appointment.objects.filter(professional=request.user.id).filter(appdate = date).filter(is_active = True)
        today = datetime.today()
        tomorrow =  today + timedelta(minutes = 500)
        print(f' asqui {tomorrow}')
        testapp = Appointment.objects.filter(professional = request.user).filter(date__isnull =  True).count()
        print(testapp)
    except:
        pass

    """    if len(data['feriados']) >= 1 and request.user.is_staff==False:
            return render(request, 'registrations/lists/myschedule.html',data)"""
            
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



def PassRecovery(request):

    if request.method == 'GET':
        return render(request, 'registrations/passrecovery.html')

    if request.method == 'POST':
        print(request.POST.get('username'))
        
        try:
            user = User.objects.get(username = request.POST.get('username'),email = request.POST.get('email'))
        except:
            pass
        
        x = str(random.randint(10000000,99999999))
        user.password = x
        user.set_password(user.password)
        subject = "NkjTec Sistemas | RECUPERAÇÃO DE SENHA!"
        content = "Sua nova senha é: "+ x
        u = Emails()
        print(u.sendmails(user.email,subject,content))
        user.save()
        return render(request, 'registrations/passrecovery.html')

@login_required
def PassChange(request):
    data={}
    if request.method == 'GET':
        data['target'] = request.GET.get('target')
        return render(request, 'registrations/passchange.html',data)

    if request.method == 'POST':
        try:
            user = User.objects.get(id = request.user.id)
            target = User.objects.get(id = request.POST.get('target'))
        except:
            pass
        if(user.master == target.master):
            target.set_password(request.POST.get('password'))
            subject = "NkjTec Sistemas | Alteracao de senha"
            content = "Sua Senha foi alterada, senão foi você sugerimos que recupere sua senha o quanto antes!"
            u = Emails()
            print(u.sendmails(user.email,subject,content))
            target.save()
            if(user != target):
                return redirect('myschedule')            
        return redirect('login')



#############################  CREATE  #############################

class ProcedureCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-procedure')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url


class AppointmentCreate(LoginRequiredMixin, CreateView):
    #login_url = reverse_lazy('')
    #fields = '__all__'
    model = Appointment
    fields =  ['client','appdate','apphour','professional','status','procedure','payed']
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
        if(self.request.POST.get('my_checkbox') == 'on'):
            newclient = Client()
            newclient.name = self.request.POST.get('id_newclient')
            newclient.tel = self.request.POST.get('id_tel')
            newclient.master = self.request.user.master
            newclient.created_by = self.request.user
            newclient.save()
            form.instance.client = newclient
        form.instance.date = Time().convertdateBRtoUS(self.request.POST.get('appdate'))
        form.instance.total = form.instance.procedure.price
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        url = super().form_valid(form)
        return url

    ''' TENTATIVA DE SOBRESCREEVER O POST
    def post(self, request, *args, **kwargs):
        if(self.request.POST.get('my_checkbox') == 'on'):
            
            print('testeposstttt')
            newclient = Client()
            newclient.name = self.request.POST.get('id_newclient')
            newclient.tel = self.request.POST.get('id_tel')
            newclient.master = self.request.user.master
            newclient.created_by = self.request.user
            newclient.save()
            form.instance.client = newclient
        form = self.get_form()
        print(form.instance)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
    '''




class ScheduleCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','is_shared']
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


class DayOffCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = DayOff
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


class UserCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
    model = User
    fields = ['first_name','nickname','username','password','email','tel','professional']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-user')

    def get_initial(self):
        return {
            "hint_id_username": "",
        }

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.master = self.request.user.master
        form.instance.set_password(self.request.POST.get('password'))
        url = super().form_valid(form)
        return url


class ClientCreate(LoginRequiredMixin, CreateView):
    login_url = reverse_lazy('login')
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

class ProcedureUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Procedure
    fields = ['name', 'time', 'price']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-procedure')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Procedure, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class AppointmentUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Appointment
    fields =  ['client','appdate','apphour','professional','status','procedure','total','payed']
    template_name = 'registrations/update_appointment.html'
    success_url = reverse_lazy('myschedule')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Appointment, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class ScheduleUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','is_shared']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-schedule')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Schedule, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class DayOffUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = DayOff
    fields = ['professional', 'daydate', 'reason']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('list-dayoff')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(DayOff, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class UserUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = User
    fields = ['first_name','username','email','tel','nickname','is_active']
    template_name = 'registrations/userupdate.html'
    success_url = reverse_lazy('list-user')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(User, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object


class ClientUpdate(LoginRequiredMixin, UpdateView):
    login_url = reverse_lazy('login')
    model = Client
    fields = ['name','tel','birth','cpf','email','obs']
    template_name = 'registrations/update_client.html'
    success_url = reverse_lazy('list-client')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Client, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['appointments'] = Appointment.objects.filter(client__id = self.kwargs['pk']).filter(is_active = True).order_by('-date','-id')
        return context


#############################  DELETE  #############################

class ProcedureDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Procedure
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-procedure')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Procedure, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class AppointmentDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Appointment
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('myschedule')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Appointment, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class ScheduleDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Schedule
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-schedule')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Schedule, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class DayOffDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = DayOff
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-dayoff')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(DayOff, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class UserDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = User
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-user')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(User, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)


class ClientDelete(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('login')
    model = Client
    fields = []
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('list-client')

    def get_object(self, queryset= None):
        self.object = get_object_or_404(Client, pk=self.kwargs['pk'], master = self.request.user.master)
        return self.object

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.is_active = False
        self.object.save()
        return HttpResponseRedirect(success_url)




#############################  LIST  #############################
class ProcedureList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Procedure
    template_name = 'registrations/lists/procedure.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = Procedure.objects.filter(master= self.request.user.master,name__icontains = self.request.GET.get('search'), is_active = 1).order_by('name')
        else:
            self.object_list = Procedure.objects.filter(master= self.request.user.master, is_active = 1).order_by('name')
        return self.object_list


class AppointmentList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Appointment
    template_name = 'registrations/lists/appointment.html'

    def get_queryset(self):
        self.object_list = Appointment.objects.filter(master= self.request.user.master, is_active = 1).order_by('-id')
        return self.object_list




class ScheduleList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Schedule
    template_name = 'registrations/lists/schedule.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = Schedule.objects.filter(master= self.request.user.master, professional__first_name__icontains = self.request.GET.get('search'), is_active = 1).order_by('professional__first_name')
        else:
            self.object_list = Schedule.objects.filter(master= self.request.user.master, is_active = 1).order_by('professional__first_name')
        return self.object_list

class DayOffList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = DayOff
    template_name = 'registrations/lists/dayoff.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = DayOff.objects.filter(master= self.request.user.master, professional__first_name__icontains = self.request.GET.get('search'), is_active = 1).order_by('professional__first_name')
        else:
            self.object_list = DayOff.objects.filter(master= self.request.user.master, is_active = 1).order_by('professional__first_name')
        return self.object_list

    
class UserList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = User
    template_name = 'registrations/lists/users.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = User.objects.filter(master= self.request.user.master,first_name__icontains = self.request.GET.get('search'))
        else:
            self.object_list = User.objects.filter(master= self.request.user.master)
        return self.object_list


class ClientList(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('login')
    model = Client
    template_name = 'registrations/lists/client.html'

    def get_queryset(self):
        if (self.request.GET.get('search')):
            self.object_list = Client.objects.filter(master= self.request.user.master,name__icontains = self.request.GET.get('search'), is_active = 1)
        else:
            self.object_list = Client.objects.filter(master= self.request.user.master, is_active = 1)
        return self.object_list



