from django import forms
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User

from .models import Profile

from django.contrib.auth import (
    authenticate,
    get_user_model,
    login,
    logout
)


class UserLoginForm(forms.Form):
    username = forms.CharField(label="")
    password  = forms.CharField(widget=forms.PasswordInput, label="")

    # editing place holders
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Password'})

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
    
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("Wrong username or password! try again.")
            if not user.check_password(password):
                raise forms.ValidationError("Password Incorrect!")
            if not user.is_active:
                raise forms.ValidationError("This user is no longer active!")

        return super(UserLoginForm, self).clean(*args, **kwargs)



class UserRegisterForm(UserCreationForm):
    
    email = forms.EmailField(label='', required=True)
    first_name = forms.CharField(label='')
    last_name = forms.CharField(label='')

    def __init__(self, *args, **kwargs):

        super(UserCreationForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['first_name'].widget.attrs.update({'placeholder': 'First Name'})
        self.fields['last_name'].widget.attrs.update({'placeholder': 'Last Name'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm Password'})
        self.fields['username'].label = ''
        self.fields['password1'].label = ''
        self.fields['password2'].label = ''
        self.fields['username'].help_text = ''
        self.fields['password1'].help_text = ''
        self.fields['password2'].help_text = ''

    class Meta:
        model = User 
        fields = [ 'username','first_name', 'last_name', 'email', 'password1', 'password2']

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise forms.ValidationError("This email has been already registered")

        return super(*args, **kwargs).clean()


class UpdateUser(forms.ModelForm):

    email = forms.EmailField(label='Email', required=False)
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)

    class Meta:
        model = User 
        fields = ['email', 'first_name', 'last_name']


class UpdateProfile(forms.ModelForm):

    class Meta:
        model = Profile 
        fields = ['image', 'job_title', 'bio']

