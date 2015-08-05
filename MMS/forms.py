from django import forms
from django.forms.models import inlineformset_factory
from django.utils.safestring import mark_safe
from django.contrib.admin import widgets
from django.core.exceptions import NON_FIELD_ERRORS
from django.core.exceptions import ValidationError
from parsley.decorators import parsleyfy

@parsleyfy
class LoginForm(forms.Form):
    NTID = forms.CharField(max_length=20)
    passwd = forms.CharField()


