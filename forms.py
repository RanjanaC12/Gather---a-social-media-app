from django.db import models  
from django.forms import fields  
from Users.models import User_table  
from django import forms  
  
  
class UserImageForm(forms.ModelForm):  
    class Meta:   
        models = User_table
        fields =  ['image']  