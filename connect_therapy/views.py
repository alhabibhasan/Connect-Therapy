from django.urls import reverse_lazy
from django.views.generic import FormView
from django.contrib.auth import authenticate, login
from django.contrib.auth import views as auth_views

from connect_therapy.forms import PatientSignUpForm, PatientLoginForm, \
    PractitionerSignUpForm
from connect_therapy.models import Patient, Practitioner


class PatientSignUpView(FormView):
    form_class = PatientSignUpForm
    template_name = 'connect_therapy/patient/signup.html'
    success_url = reverse_lazy('connect_therapy:patient-signup-success')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.username = user.email
        user.save()
        patient = Patient(user=user,
                          date_of_birth=form.cleaned_data['date_of_birth'],
                          gender=form.cleaned_data['gender'],
                          mobile=form.cleaned_data['mobile']
                          )
        patient.save()
        user = authenticate(username=form.cleaned_data['email'],
                            password=form.cleaned_data['password1']
                            )
        login(request=self.request, user=user)
        return super().form_valid(form)


class PatientLoginView(auth_views.LoginView):
    template_name = 'connect_therapy/patient/login.html'
    authentication_form = PatientLoginForm

    def get_success_url(self):
        return reverse_lazy('connect_therapy:patient-login-success')


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
