from django.shortcuts import render, redirect
from django.http import HttpResponse

def	authenticated_user(view_func):
	def wrapper_func(request, *args, **kwargs):
		if request.user.is_authenticated:
			return view_func(request, *args, **kwargs)
		return redirect('login')
	return wrapper_func

def allowed_users(allowed_roles=[]):
	def decorator(view_func):
		def wrapper_func(request, *args, **kwargs):
			if request.user.groups.exists():
				group = request.user.groups.all()[0].name
				if group in allowed_roles:
					return view_func(request, *args, **kwargs)
			return redirect('no_permision')
		return wrapper_func
	return decorator
