from django import forms

from .models import login, create

class Login(forms.ModelForm):
	
	email = forms.CharField(required=True,
							widget=forms.Textarea(attrs={
								"placeholder": "votreEmail@imagine.xyz",
								'row':1,
								'col':1}))
	pwd = forms.CharField(required=True,
						widget=forms.Textarea(attrs={
								"placeholder": "MotDePasse127!",
								"row":8,
								'col':68}))
	class Meta:
		model = login
		fields = [
		"email",
		"pwd"
		]

class Create(forms.ModelForm):
	prompt = forms.CharField(required=True)
	nb_img = forms.CharField(required=True)
	own_img= forms.FileField()
	class Meta:
		model = login
		fields = [
		"prompt"]