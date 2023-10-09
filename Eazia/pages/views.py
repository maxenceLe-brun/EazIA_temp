from django.shortcuts import render
from django.http import HttpResponse
from .form import Login, Create
from .models import login, create
from main.main import main
import requests

# Create your views here.

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def login_view(request, *args, **kwargs):
	form = Login(request.POST or None)
	my_context = {
		"form":form,
	}
	return render(request, "login.html", my_context)

def loged_view(request, *args,**kwargs):
	print("\nsign!!!\n")
	form = Login(request.POST or None)
	user = request.POST["user"]
	password = request.POST["password"]
	my_context = {
		"password":password,
		"user":user,
		"form":form,
	}
	print(my_context)
	if password and user:
		return home_view(request, *args, **kwargs)
	return login_view(request, *args, **kwargs)

def home_view(request, *args, **kwargs):
	print("\nhome!!!\n")
	form = Login(request.POST or None)
	my_context = {
		"form":form,
	}
	print(my_context)
	return render(request, "navbar.html", my_context)

def post_view(request, *args, **kwargs):
	print('\nposts!!!\n')
	form = Create(request.POST or None)
	my_context = {
		"form":form,
	}
	print(my_context)
	return render(request, "post.html", my_context)

def posting_view(request, *args, **kwargs):
	print("\nposting!!!\n")
	form = Create(request.POST or None)
	print(str(form))
	prompt = request.POST["post[prompt]"]
	nb_img = request.POST["post[many_imgs]"]
	own_img= request.POST["post[pictures][]"]
	my_context = {
		"form":form,
		"post[prompt]":prompt,
		"post[many_imgs]":nb_img,
		"post[pictures][]":own_img,
	}
	print(my_context, prompt, nb_img, own_img)
	
	return render(request, "postId.html", my_context)

def about_view(request, *args, **kwargs):
	print("\nabout!!!\n")
	my_context = {
		"title": "abc this is about us",
		"this_is_true": True,
		"my_number": 123,
		"my_list": [1313, 4231, 312, "Abc"],
		"my_html": "<h1>Hello World</h1>"

	}
	return render(request, "about.html", my_context)

def history_view(request, *args, **kwargs):
	print("\nhistory!!!\n")
	my_context = {

	}
	return render(request, "history.html", my_context)

def draft_view(request, *args, **kwargs):
	print("\ndraft!!!\n")
	my_context = {

	}
	return render(request, "draft.html", my_context)

def programs_view(request, *args, **kwargs):
	print("\nprograms!!!\n")
	my_context = {

	}
	return render(request, "programs.html", my_context)

def generate_view(request, *args, **kwargs):
	print("\nhistory!!!\n")
	my_context = {

	}
	return render(request, "history.html", my_context)
