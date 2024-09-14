from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from mproduct.models import Subscriber


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(max_length=254,help_text="Required. Inform a valid email address.")
    firstname = forms.CharField(max_length=10,help_text="first name",required=True)
    lastname = forms.CharField(max_length=10,help_text="last name",required=True)
    company = forms.CharField(max_length=30,help_text="company name",required=True)
    companysize = forms.IntegerField(help_text="company size",required=True)

    class Meta:
        model = User
        fields = ['username','email','password1','password2','firstname','lastname']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['firstname']
        user.last_name = self.cleaned_data['lastname']

        if commit:
            user.save()
            subscriber = Subscriber(user=user)
            subscriber.company = self.cleaned_data['company']
            subscriber.companysize = self.cleaned_data['companysize']
            subscriber.save()
        return user
