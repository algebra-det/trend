from django import forms
from .models import MyUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, ValidationError

class UserAddForm(UserCreationForm):
    email = forms.EmailField(max_length=30)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name']


class UserNormalAddForm(UserCreationForm):
    email = forms.EmailField(max_length=30)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'dob', 'city', 'province']


    def __init__(self, *args, **kwargs):
        # first call parent's constructor
        super(UserNormalAddForm, self).__init__(*args, **kwargs)
        # there's a `fields` property now
        self.fields['dob'].required = True
        self.fields['city'].required = True
        self.fields['province'].required = True


class UserChangeAdminForm(UserChangeForm):
    email = forms.EmailField(max_length=30)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name']


class UserChangeNormalForm(UserChangeForm):
    email = forms.EmailField(max_length=30)

    class Meta:
        model = MyUser
        fields = ['email', 'first_name', 'last_name', 'dob', 'province', 'city']