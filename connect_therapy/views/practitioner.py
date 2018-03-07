from django.contrib.auth import authenticate, login, views as auth_views
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views import generic
from django.views.generic import FormView

from connect_therapy.forms.practitioner import PractitionerSignUpForm,\
    PractitionerLoginForm, PractitionerNotesForm
from connect_therapy.models import Practitioner, Appointment


class PractitionerSignUpView(FormView):
    form_class = PractitionerSignUpForm
    template_name = 'connect_therapy/practitioner/signup.html'
    success_url = reverse_lazy('connect_therapy:practitioner-signup-success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.save()
        practitioner = Practitioner(
            user=user,
            address_line_1=form.cleaned_data['address_line_1'],
            address_line_2=form.cleaned_data['address_line_2'],
            postcode=form.cleaned_data['postcode'],
            mobile=form.cleaned_data['mobile'],
            bio=form.cleaned_data['bio']
        )
        practitioner.save()
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1']
                            )
        login(request=self.request, user=user)
        return super().form_valid(form)


class PractitionerLoginView(auth_views.LoginView):
    template_name = 'connect_therapy/practitioner/login.html'
    authentication_form = PractitionerLoginForm

    def get_success_url(self):
        return reverse_lazy('connect_therapy:practitioner-login-success')


class PractitionerNotesView(FormView):
    form_class = PractitionerNotesForm
    template_name = 'connect_therapy/practitioner/notes.html'
    success_url = reverse_lazy('connect_therapy:practitioner-login-success')

    def form_valid(self, form):
        self.appointment.practitioner_notes = form.cleaned_data['practitioner_notes']
        self.appointment.patient_notes_by_practitioner = form.cleaned_data['patient_notes_by_practitioner']
        self.appointment.save()
        return super().form_valid(form)

    def get(self, request, appointment_id):
        self.appointment = get_object_or_404(Appointment, pk=appointment_id)
        return super().get(request)

    def post(self, request, appointment_id):
        self.appointment = get_object_or_404(Appointment, pk=appointment_id)
        return super().post(request)


class PractitionerMyAppointmentsView(generic.TemplateView):
    template_name = 'connect_therapy/practitioner/my-appointments.html'

    model = Appointment

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['future_appointments'] = Appointment.objects.filter(
            start_date_and_time__gte=timezone.now(),
            practitioner=self.request.user.practitioner
        ).order_by('-start_date_and_time')
        context['past_appointments'] = Appointment.objects.filter(
            start_date_and_time__lt=timezone.now(),
            practitioner=self.request.user.practitioner
        ).order_by('-start_date_and_time')
        return context


class PractitionerPreviousNotesView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('connect_therapy:practitioner-appointment-notes')
    model = Appointment
    template_name = 'connect_therapy/practitioner/appointment-notes.html'


class PractitionerCurrentNotesView(LoginRequiredMixin, generic.DetailView):
    login_url = reverse_lazy('connect_therapy:practitioner-before-meeting-notes')
    model = Appointment
    template_name = 'connect_therapy/practitioner/before-meeting-notes.html'