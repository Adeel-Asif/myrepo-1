from django import forms

from .models import Post


from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .choices import * 
class PostForm(forms.ModelForm):
    booked = forms.ChoiceField(choices = booked_status, widget=forms.Select(), required=True)
    depart_date= forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    return_date=forms.DateTimeField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    middle_name = forms.CharField(required=False)
    class Meta:
        model = Post
        fields = ('first_name','middle_name','last_name','mobile_no','work_no',
            'other_no','customer_email','depart_date','return_date','booked','remarks')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    number = forms.IntegerField()
    birth_date = forms.DateField(widget=forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'}))
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date','number', 'password1', 'password2' )        

        