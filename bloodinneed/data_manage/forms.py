from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate
from .models import Donor, Blog
from django import forms




class DonorCreationForm(UserCreationForm):
    full_name = forms.CharField(required=True,max_length=100, help_text='Required.')
    contact = forms.CharField(required=True,max_length=100, help_text='Required.')
    username = forms.CharField(required=True,max_length=100, help_text='Required.')
    is_donor = forms.BooleanField(required=False,help_text='Select if you want to be a donor.')
    blood_group = forms.CharField(required=True,max_length=10, help_text='Required. ex: A+')
    class Meta:
        model= Donor
        fields=(
            'full_name',
            'contact',
            'username',
            'is_donor',
            'location',
            'blood_group'
        )



class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Donor
        fields = (
            'username',
        )

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if not authenticate(username=username, password=password):
            raise forms.ValidationError('Invalid login.')

class DonorUpdate(forms.ModelForm):

    #Iccha UserCreation also


    class Meta:
        model = Donor
        fields = (
            'full_name',
            'contact',
            'username',
            'is_donor',
            'location',
            'blood_group'

        )




class BlogForm(forms.ModelForm):
    content = forms.CharField(required=True,max_length=1000, help_text='Blood group/Details/Text.')
    location = forms.CharField( max_length=200, help_text='Hospital Location if you need Blood.')
    need = forms.BooleanField( required=False,help_text='Select if you need Blood.')
    blog_blood_group = forms.CharField(required=False, help_text='Tell if you need Blood. ex: A+')
    class Meta:
        model= Blog
        fields=(
            'content',
            'need',
            'location',
            'blog_blood_group'
        )

