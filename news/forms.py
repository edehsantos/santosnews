from django import forms
from .models import *

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=256)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(required=False, widget=forms.Textarea)
    
    
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment   
        fields = ['name', 'email', 'body'] 
        
        
class SearchForms(forms.Form):
    query = forms.CharField()
    
    
class Message_us(forms.ModelForm):
    class Meta:
        model = Message
        fields = "__all__"    
    
    
            