from django import forms
from .models import Order


class OrderCheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ('first_name', 'last_name', 'city', 'address', 'phone', 'email','note')

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['first_name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your first name'})
            self.fields['last_name'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your last name'})
            self.fields['city'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your city'})
            self.fields['address'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your address'})
            self.fields['phone'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your phone'})
            self.fields['email'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your email'})
            self.fields['note'].widget.attrs.update({'class': 'form-control','placeholder':'Enter your note'})