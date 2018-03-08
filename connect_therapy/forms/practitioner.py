from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField
from django.contrib.auth.models import User

from connect_therapy.models import Practitioner


class PractitionerSignUpForm(UserCreationForm):
    address_line_1 = forms.CharField(max_length=100)
    address_line_2 = forms.CharField(max_length=100, required=False)
    postcode = forms.CharField(max_length=10)
    mobile = forms.CharField(max_length=20)
    bio = forms.CharField(widget=forms.Textarea)

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("You've already signed up!",
                                        code='exists'
                                        )
        return email

    class Meta:
        model = User
        fields = ('first_name',
                  'last_name',
                  'email',
                  'mobile',
                  'address_line_1',
                  'address_line_2',
                  'postcode',
                  'bio',
                  'password1',
                  'password2')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'size': 35, 'class': 'form-control'}),
        }


class PractitionerLoginForm(AuthenticationForm):
    username = UsernameField(
        max_length=254,
        widget=forms.TextInput(attrs={
            'autofocus': True,
            'size': 35,
        }, ),
        label="Email"
    )

    def confirm_login_allowed(self, user):
        try:
            user.practitioner
        except Practitioner.DoesNotExist:
            raise forms.ValidationError(
                "You are not a practitioner",
                code='not-practitioner'
            )

        if not user.practitioner.is_approved:
            raise forms.ValidationError(
                "You have not been approved",
                code='not-approved'
            )
        super().confirm_login_allowed(user)


class PractitionerNotesForm(forms.Form):
    practitioner_notes = forms.CharField(label="notes for practitioner", widget=forms.Textarea)
    patient_notes_by_practitioner = forms.CharField(label="notes for patient", widget=forms.Textarea)