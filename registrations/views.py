from django.views.generic import CreateView
from django.views.generic.edit import UpdateView, UpdateView, DeleteView
from django.views.generic.list import ListView
from .models import *
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin


#############################  CREATE  #############################

class ProcedureCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class StatusCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Status
    fields = ['name','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class PaymentCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Payment
    fields = ['name', 'discount', 'tax','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class AppointmentCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields = ['client','professional','status','procedure','payment' ]
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class ScheduleCreate(CreateView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class DayOffCreate(CreateView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = ['professional', 'daydate', 'reason','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

 
#############################  UPDATE  #############################

class ProcedureUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class StatusUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Status
    fields = ['name','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class PaymentUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Payment
    fields = ['name', 'discount', 'tax','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class AppointmentUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields = ['client','professional','status','procedure','payment' ]
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class ScheduleUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

class DayOffUpdate(UpdateView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = ['professional', 'daydate', 'reason','active']
    template_name = 'registrations/forms.html'
    success_url = reverse_lazy('index')

#############################  DELETE  #############################

class ProcedureDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Procedure
    fields = ['name', 'time', 'price','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('index')

class StatusDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Status
    fields = ['name','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('index')

class PaymentDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Payment
    fields = ['name', 'discount', 'tax','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('index')

class AppointmentDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Appointment
    fields = ['client','professional','status','procedure','payment' ]
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('index')

class ScheduleDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = Schedule
    fields = ['professional', 'begin', 'end','interval','weekday','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('index')

class DayOffDelete(DeleteView):
    #login_url = reverse_lazy('')
    model = DayOff
    fields = ['professional', 'daydate', 'reason','active']
    template_name = 'registrations/delete-forms.html'
    success_url = reverse_lazy('index')


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