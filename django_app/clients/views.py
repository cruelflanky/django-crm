from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse

import string
import random
import hashlib

from .models import *
from .forms import *
from .decorators import authenticated_user, allowed_users
from datetime import datetime, timedelta
from order.models import Order, Shop

def gen_hash():
	letters = string.ascii_letters
	result_str = ''.join(random.choice(letters) for i in range(random.randint(5,10)))
	m = hashlib.md5()
	m.update(result_str.encode('utf-8'))
	return m.hexdigest()

def signup(request):
	group = Group.objects.get(name = 'Manager')
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			group.user_set.add(user)
			email = form.cleaned_data.get('email')
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			profile = Profile.objects.create(user=user, email=email,
				activation_code = gen_hash(), role = group)
			SmsStatus.objects.create(profile=profile)
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
		messages.error(request, 'Your password can’t be too similar to your other personal information.')
		messages.error(request, 'Your password must contain at least 8 characters.')
		messages.error(request, 'Your password can’t be a commonly used password.')
		messages.error(request, 'Your password can’t be entirely numeric.')
		return redirect('signup')
	return render(request, 'signup.html', {'form': CreateUserForm()})

@authenticated_user
def dashboard(request):
	return render(request, 'index.html')

@authenticated_user
def profile(request):
	profile = request.user.profile
	sms = SmsStatus.objects.get(profile=profile)
	form2 = SmsStatusForm(instance=sms)
	payment_plans = PaymentPlan.objects.filter(is_active=True)

	if request.method == 'POST':
		form2 = SmsStatusForm(request.POST, instance=sms)
		if form2.is_valid():
			print(form2)
			form2.save()
			return redirect('profile')

	context = {'form2' : form2, 'payment_plans': payment_plans}
	return render(request, 'profile.html', context)

@authenticated_user
def profile_edit(request):
	profile = request.user.profile
	sms = SmsStatus.objects.get(profile=profile)
	form = ProfileForm(instance=profile)
	form2 = SmsStatusForm(instance=sms)

	if request.method == 'POST':
		form = ProfileForm(request.POST, request.FILES, instance=profile)
		form2 = SmsStatusForm(request.POST, instance=sms)
		if form.is_valid():
			form.save()
			return redirect('profile')
		if form2.is_valid():
			form2.save()
			return redirect('profile')

	context = {'form': form , 'form2' : form2}
	return render(request, 'profile_edit.html', context)

@authenticated_user
def orders(request):
	orders = []
	shops =Shop.objects.filter(profile=request.user.profile)
	for shop in shops:
		orders.append(Order.objects.filter(shop_name=shop))
	context = {'orders': orders }
	return render(request, 'orders.html', context)

@authenticated_user
@allowed_users(allowed_roles=['Admin'])
def staff(request):
	form = ManagerCreateForm()
	profiles = Profile.objects.all()

	if request.method == 'POST':
		form = ManagerCreateForm(request.POST)
		if form.is_valid():
			user = form.save()
			group = form.cleaned_data.get('role')
			if group:
				group.user_set.add(user)
			profile = Profile.objects.create(user=user,
				email = form.cleaned_data.get('email'),
				first_name = form.cleaned_data.get('first_name'),
				last_name = form.cleaned_data.get('last_name'),
				team = form.cleaned_data.get('team'),
				role = group, activation_code = gen_hash())
			SmsStatus.objects.create(profile=profile)

	context = {'form': form ,'profiles': profiles}
	return render(request, 'staff.html', context)

@authenticated_user
@allowed_users(allowed_roles=['Admin'])
def delete_profile(request, pk):
	profile = Profile.objects.get(id=pk)

	if request.method == "GET":
		profile.delete()

	return redirect('staff')

@authenticated_user
@allowed_users(allowed_roles=['Admin'])
def update_profile(request, pk):
	profile = Profile.objects.get(id=pk)
	form = ProfileEditForm(instance=profile,
		initial = {'role': profile.user.groups.all()[0]})

	if request.method == 'POST':
		form = ProfileEditForm(request.POST, instance=profile,
			initial = {'role': profile.user.groups.all()[0]})
		if form.is_valid():
			form.save()
			group = form.cleaned_data.get('role')
			if group != profile.role and profile.role != None:
				profile.user.groups.clear()
			group.user_set.add(profile.user)
			profile.role = group.name
			profile.save()
			return redirect('staff')

	context = {'form':form}
	return render(request, 'edit_profile.html', context)

@authenticated_user
@allowed_users(allowed_roles=['Admin'])
def teams(request):
	form = TeamCreateForm()
	teams = Team.objects.all()

	if request.method == 'POST':
		form = TeamCreateForm(request.POST)
		if form.is_valid():
			team = form.save()
			managers = form.cleaned_data.get('managers')
			print(managers)
			for manager in managers:
				Profile.objects.filter(id=manager.id).update(team=team)
			return redirect('teams')

	context = {'form': form ,'teams': teams}
	return render(request, 'teams.html', context)

@authenticated_user
@allowed_users(allowed_roles=['Admin'])
def delete_team(request, pk):
	team = Team.objects.get(id=pk)

	if request.method == "GET":
		team.delete()

	return redirect('teams')

@authenticated_user
def set_payment(request, pk):
	payment_plan = PaymentPlan.objects.get(id=pk)
	profile = request.user.profile
	now = datetime.now()

	if request.method == "GET":
		profile = Profile.objects.get(id=profile.id)
		profile.payment_plan = payment_plan
		if profile.payment_end:
			profile.payment_end += payment_plan.duration
		else:
			profile.payment_end = now + payment_plan.duration
		profile.save()

	return redirect('profile')

@authenticated_user
def my_clients(request):
	return render(request, 'my_clients.html')

def add_managers_to_shop(managers, shop):
	for manager in managers:
		profile = Profile.objects.get(id=manager.id)
		profile.shop.add(shop)
		profile.save()

@authenticated_user
@allowed_users(allowed_roles=['Admin', 'Director'])
def all_clients(request):
	form = ChooseManagerForm()
	form2 = ShopCreateForm()
	shops = Shop.objects.all()

	if request.method == 'POST':
		form = ChooseManagerForm(request.POST)
		form2 = ShopCreateForm(request.POST)
		if form.is_valid():
			managers = form.cleaned_data.get('managers')
			selected_shops = form.cleaned_data.get('shops')
			for shop in selected_shops.split(':'):
				shop = Shop.objects.get(id=int(shop))
				add_managers_to_shop(managers, shop)
		if form2.is_valid():
			shop = form2.save()
			managers = form.cleaned_data.get('managers')
			add_managers_to_shop(managers, shop)
		return redirect('all_clients')

	context = {'shops' : shops, 'form' : form, 'form2' : form2}
	return render(request, 'all_clients.html', context)

@authenticated_user
@allowed_users(allowed_roles=['Admin', 'Director'])
def relink_shops(request):
	return_dict = dict()
	shops = []
	data = request.POST
	csrf = data.get("csrfmiddlewaretoken")
	return_dict["csrf"] = csrf
	for shop in data:
		if shop.isnumeric():
			shops.append(shop)
	return_dict["shops"] = ':'.join(shops)
	return JsonResponse(return_dict)

@authenticated_user
@allowed_users(allowed_roles=['Admin', 'Director'])
def delete_shop(request, pk):
	shop = Shop.objects.get(id=pk)

	if request.method == "GET":
		shop.delete()

	return redirect('all_clients')

@authenticated_user
@allowed_users(allowed_roles=['Admin', 'Director'])
def update_shop(request, pk):
	shop = Shop.objects.get(id=pk)
	form = ShopEditForm(instance=shop)

	if request.method == 'POST':
		form = ShopEditForm(request.POST, instance=shop)
		if form.is_valid():
			form.save()
			return redirect('all_clients')

	context = {'form':form}
	return render(request, 'edit_shop.html', context)

@authenticated_user
def bd_search(request):
	profiles = Profile.objects.all()

	if request.method == 'POST':
		form = ManagerCreateForm(request.POST)
		if form.is_valid():
			user = form.save()
			group = form.cleaned_data.get('role')
			if group:
				group.user_set.add(user)
			profile = Profile.objects.create(user=user,
				email = form.cleaned_data.get('email'),
				first_name = form.cleaned_data.get('first_name'),
				last_name = form.cleaned_data.get('last_name'),
				team = form.cleaned_data.get('team'),
				role = group)
			SmsStatus.objects.create(profile=profile)

	context = {'form': form ,'profiles': profiles}
	return render(request, 'bd_search.html', context)

@authenticated_user
@allowed_users(allowed_roles=['Admin', 'Director'])
def dublicates(request):
	orders = []

	if request.user.groups.all()[0] == 'Admin':
		shops = Shop.objects.all()
	else:
		shops =Shop.objects.filter(profile=request.user.profile)

	for shop in shops:
		orders.append(Order.objects.filter(shop_name=shop))
	context = {'orders': orders }
	return render(request, 'dublicates.html', context)

@authenticated_user
def no_permision(request):
	return render(request, 'permision.html')
