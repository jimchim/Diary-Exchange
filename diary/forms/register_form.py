from django import forms
from django.contrib.auth.models import User


class registerForm(forms.Form):	
	# TODO: Define form fields here
	username = forms.CharField(max_length = 20)
	email = forms.EmailField()
	password = forms.CharField(widget = forms.PasswordInput)
	confirm_password = forms.CharField(widget = forms.PasswordInput)

	def clean_email(self):    	
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exist():
			raise ValidationError('Email already used by another account.')
		return email
