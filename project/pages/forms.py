from dataclasses import fields
from email import message
from django import forms
from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your first name'})
        self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your email'})
        self.fields['phone'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your phone'})
        self.fields['message'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your Message'})