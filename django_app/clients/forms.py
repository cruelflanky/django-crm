from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from django.core.exceptions import ValidationError
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Row, Column

from .models import Profile, SmsStatus, Team, Shop

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ['user', 'created', 'team', 'role', 'payment_plan', 'payment_end', 'activation_code', 'shop']

		widgets = {
			'first_name' : forms.TextInput(attrs={'class': 'form-control'}),
			'last_name' : forms.TextInput(attrs={'class': 'form-control'}),
			'phone' : forms.TextInput(attrs={'class': 'form-control'}),
			'email' : forms.EmailInput(attrs={'class': 'form-control'}),
			'prom_id' : forms.TextInput(attrs={'class': 'form-control'}),
			'prom_token' : forms.TextInput(attrs={'class': 'form-control'}),
			'viber_token' : forms.TextInput(attrs={'class': 'form-control'}),
			'telegram_token' : forms.TextInput(attrs={'class': 'form-control'}),
		}

class SmsStatusForm(ModelForm):
	class Meta:
		model = SmsStatus
		fields = '__all__'
		exclude = ['profile', 'name']

class CreateUserForm(UserCreationForm):
	class Meta:
		model = User
		fields = ['username', 'email', 'password1', 'password2']

class ManagerCreateForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput())
	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	email = forms.CharField(widget=forms.TextInput(), error_messages={'exists': 'Oops'})
	password1 = forms.CharField(widget=forms.PasswordInput(), label='Password')
	password2 = forms.CharField(widget=forms.PasswordInput(), label='Repeat password')
	team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
	role = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'username',
			Row(
				Column('first_name', css_class='form-group col-md-6 mb-0'),
				Column('last_name', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			'email',
			Row(
				Column('password1', css_class='form-group col-md-6 mb-0'),
				Column('password2', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('team', css_class='form-group col-md-6 mb-0'),
				Column('role', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Submit('submit', 'Create profile')
		)

	def save(self, commit=True):
		user = super(ManagerCreateForm, self).save(commit=False)
		user.email = self.cleaned_data["email"]
		if commit:
			user.save()
		return user

	def clean_email(self):
		if User.objects.filter(email=self.cleaned_data['email']).exists():
			raise ValidationError(self.fields['email'].error_messages['exists'])
		return self.cleaned_data['email']

class ProfileEditForm(ModelForm):
	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	email = forms.CharField(widget=forms.TextInput(), error_messages={'exists': 'Oops'})
	phone = forms.CharField(widget=forms.TextInput(), required=False)
	prom_id = forms.CharField(widget=forms.TextInput(), required=False)
	prom_token = forms.CharField(widget=forms.TextInput(), required=False)
	viber_active = forms.BooleanField(required=False)
	viber_token = forms.CharField(widget=forms.TextInput(), required=False)
	telegram_active = forms.BooleanField(required=False)
	telegram_token = forms.CharField(widget=forms.TextInput(), required=False)
	team = forms.ModelChoiceField(queryset=Team.objects.all(), required=False)
	role = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)
	shop = forms.ModelMultipleChoiceField(queryset=Shop.objects.all(), required=False,
		widget=forms.CheckboxSelectMultiple)
	activation_code = forms.CharField(widget=forms.TextInput(), required=False)

	class Meta:
		model = Profile
		fields = '__all__'
		exclude = ['user', 'created', 'profile_pic', 'payment_end', 'payment_plan']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('first_name', css_class='form-group col-md-6 mb-0'),
				Column('last_name', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			'email',
			Row(
				Column('phone', css_class='form-group col-md-6 mb-0'),
				Column('prom_id', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			'prom_token',
			Row(
				Column('team', css_class='form-group col-md-6 mb-0'),
				Column('role', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('telegram_active', css_class='form-group col-md-6 mb-0'),
				Column('telegram_token', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Row(
				Column('viber_active', css_class='form-group col-md-6 mb-0'),
				Column('viber_token', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			'shop',
			'activation_code',
			Submit('submit', 'Edit profile')
		)

class TeamCreateForm(ModelForm):

	name = forms.CharField(widget=forms.TextInput())
	managers = forms.ModelMultipleChoiceField(queryset=Profile.objects.filter(role='Manager'),
		widget=forms.CheckboxSelectMultiple)

	class Meta:
		model = Team
		fields = '__all__'

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'name',
			'managers',
			Submit('submit', 'Create profile')
		)

	def save(self, commit=True):
		user = super(TeamCreateForm, self).save(commit=False)
		if commit:
			user.save()
		return user

class ShopCreateForm(ModelForm):

	name = forms.CharField(widget=forms.TextInput())
	url = forms.URLField(widget=forms.URLInput())
	shop_token = forms.CharField(widget=forms.TextInput())
	managers = forms.ModelMultipleChoiceField(queryset=Profile.objects.filter(role='Manager'))

	class Meta:
		model = Shop
		fields = '__all__'
		exclude = ['number_of_orders', 'created', 'updated', 'is_active']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			Row(
				Column('name', css_class='form-group col-md-6 mb-0'),
				Column('url', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			'shop_token',
			'managers',
			Submit('submit', 'Add shop')
		)

	def save(self, commit=True):
		user = super(ShopCreateForm, self).save(commit=False)
		if commit:
			user.save()
		return user

class ChooseManagerForm(forms.Form):

	shops = forms.CharField(widget=forms.HiddenInput())
	managers = forms.ModelMultipleChoiceField(queryset=Profile.objects.filter(role='Manager'),
		widget=forms.CheckboxSelectMultiple)

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'shops',
			'managers',
			Submit('submit', 'Create profile')
		)

class ShopEditForm(ModelForm):
	name = forms.CharField(widget=forms.TextInput())
	url = forms.URLField(widget=forms.URLInput())
	is_active = forms.BooleanField(required=False)
	shop_token = forms.CharField(widget=forms.TextInput())

	class Meta:
		model = Shop
		fields = '__all__'
		exclude = ['number_of_orders', 'created', 'updated']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper()
		self.helper.layout = Layout(
			'name',
			'url',
			Row(
				Column('is_active', css_class='form-group col-md-6 mb-0'),
				Column('shop_token', css_class='form-group col-md-6 mb-0'),
				css_class='form-row'
			),
			Submit('submit', 'Edit profile')
		)