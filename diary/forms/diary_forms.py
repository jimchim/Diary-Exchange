from django import forms


class registerForm(forms.Form):	
    # TODO: Define form fields here
    username = forms.CharField(max_length = 20)
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)
    confirm_password = forms.CharField(widget = forms.PasswordInput)
    