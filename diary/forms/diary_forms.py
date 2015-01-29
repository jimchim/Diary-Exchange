from django import forms
from django.contrib.auth.models import User
from diary.models import Entry

class registerForm(forms.Form):	
	# TODO: Define form fields here
	username = forms.CharField(max_length = 20)
	email = forms.EmailField()
	password = forms.CharField(widget = forms.PasswordInput)
	confirm_password = forms.CharField(widget = forms.PasswordInput)	
	
	def clean_email(self):    	
		email = self.cleaned_data['email']
		if User.objects.filter(email=email).exists():
			#msg = forms.ValidationError('Email already used by another account.')
			#self.add_error('email', 'Email already used by another account.')
			raise forms.ValidationError('Email already used by another account.')
			
		return email

	def clean_password(self):
		password = self.cleaned_data['password']

		if len(password) < 8:
			raise forms.ValidationError('Password too short, 8 characters minimum.')
		return password


	def clean_confirm_password(self):
		password = self.cleaned_data.get('password', '')
		confirm_password = self.cleaned_data['confirm_password']

		if password == '':
			return

		if confirm_password != password:
			raise forms.ValidationError('Confirm password not matched')
		return confirm_password

class entryForm(forms.Form):
	subject = forms.CharField(max_length = 180)
	body = forms.CharField(widget = forms.Textarea)
	# class Meta:
	# 	model = Entry
	# 	fields = ['subject', 'body', 'author']	

	# def clean_subject(self): #this works
	# 	subject = self.cleaned_data['subject']
	# 	if  subject != "hello world":
	# 		raise forms.ValidationError('You need to say hello to the world in your subject')
	# 	return subject	  