from django import forms
from models import *
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    company = forms.CharField(max_length=100, required=False)
    subject = forms.CharField(max_length=100)
    email = forms.EmailField()
    url = forms.URLField(required=False)
    message = forms.CharField(widget=forms.Textarea)
    RECRUITING = 'Recruiting'
    STUDENT = 'Student'
    ADMIN = 'Administrator'
    PROF = 'Professor'
    OTHER = 'Other'
    PEOPLE_CHOICES = (
        (RECRUITING, 'Recruiting'),
        (STUDENT, 'Student'),
        (ADMIN, 'Administrator'),
        (PROF, 'Professor'),
        (OTHER, 'Other'),
    )
    #people = forms.CharField(max_length=20, choices=PEOPLE_CHOICES)

    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split())
        if num_words < 4:
            raise forms.ValidationError("Not enough words!")
        return message
