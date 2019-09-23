from django import forms
from django.contrib.auth.forms import UserCreationForm
from RegLogin.models import PROFILE
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput)


class UserCreateForm(UserCreationForm):
    first_name = forms.CharField(required=True, max_length=20)
    username=forms.CharField(required=True)
    password1 = forms.CharField(required=True,widget=forms.PasswordInput)
    password2 = forms.CharField(required=True, widget=forms.PasswordInput)
    # first_name, last_name, password, username, email
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username=self.cleaned_data['username']
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
        class Meta:
            model = PROFILE
            fields = ('Phone', 'Address')