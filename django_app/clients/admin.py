from django.contrib import admin

from .models import *

class SmsStatusInline(admin.TabularInline):
	model = SmsStatus

class SmsStatusAdmin(admin.ModelAdmin):
	list_display = [field.name for field in SmsStatus._meta.fields]

	class Meta:
		model = SmsStatus

admin.site.register(SmsStatus, SmsStatusAdmin)

class ProfileAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Profile._meta.fields]
	inlines = [SmsStatusInline]

	class Meta:
		model = Profile

admin.site.register(Profile, ProfileAdmin)

class TeamAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Team._meta.fields]

	class Meta:
		model = Team

admin.site.register(Team, TeamAdmin)

class PaymentPlanAdmin(admin.ModelAdmin):
	list_display = [field.name for field in PaymentPlan._meta.fields]

	class Meta:
		model = PaymentPlan

admin.site.register(PaymentPlan, PaymentPlanAdmin)

class ShopAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Shop._meta.fields]

	class Meta:
		model = Shop

admin.site.register(Shop, ShopAdmin)

admin.site.register(Role)
# Register your models here.
