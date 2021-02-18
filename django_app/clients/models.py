from django.db import models
from django.contrib.auth.models import User
from datetime import timedelta

# Create your models here.

class Team(models.Model):

	name = models.CharField(verbose_name = 'Team', max_length=50)
	is_active = models.BooleanField(default=True)

	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Команда'
		verbose_name_plural = 'Команды'

	def __str__(self):
		return "%s" % self.name

class PaymentPlan(models.Model):
	name = models.CharField(verbose_name = 'Payment Plan', max_length=50)
	comment = models.CharField(verbose_name = 'Comment', max_length=100)
	duration = models.DurationField(default=timedelta(days=14))
	is_active = models.BooleanField(default=True)

	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Подписка'
		verbose_name_plural = 'Подписки'

	def __str__(self):
		return "%s" % self.name

class Shop(models.Model):
	name = models.CharField(verbose_name = 'магазин', max_length=50, null=True)
	url = models.URLField(verbose_name='ссылка', null=True)
	is_active = models.BooleanField(default=True)
	shop_token = models.CharField(verbose_name = 'токен магазина', max_length=50, default=None, null=True)
	number_of_orders = models.DecimalField(verbose_name = 'кол-во заказов', max_digits=9, decimal_places=0, default=0)

	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Магазин'
		verbose_name_plural = 'Магазины'

	def __str__(self):
		return "%s" % self.name

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
	role = models.CharField(verbose_name = 'Role', max_length=50, blank=True, null=True, default=None)
	first_name = models.CharField(verbose_name = 'First name', max_length=50)
	last_name = models.CharField(verbose_name = 'Last name', max_length=50)
	phone = models.CharField(verbose_name = 'Phone number', max_length=50)
	email = models.CharField(verbose_name = 'Email', max_length=50)
	profile_pic = models.ImageField(default='profile_pic.png', null=True, blank=True)
	prom_id = models.CharField(verbose_name = 'Prom ID', max_length=50, default=None, null=True)
	prom_token = models.CharField(verbose_name = 'Prom token', max_length=50, default=None, null=True)
	viber_active = models.BooleanField(default=False, verbose_name = 'Viber on/off')
	viber_token = models.CharField(verbose_name = 'Viber Token', max_length=50, default=None, null=True)
	telegram_active = models.BooleanField(default=False, verbose_name = 'Telegram on/off')
	telegram_token = models.CharField(verbose_name = 'Telegram Token', max_length=50, default=None, null=True)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	team = models.ForeignKey(Team, on_delete=models.SET_NULL, blank=True, null=True, default=None, verbose_name = 'Team')
	shop = models.ManyToManyField(Shop, blank=True, default=None, verbose_name = 'Магазин')
	payment_plan = models.OneToOneField(PaymentPlan, null=True, on_delete=models.SET_NULL, blank=True, default=None, verbose_name = 'Payment Plan')
	payment_end = models.DateTimeField(default=None, null=True)
	activation_code = models.CharField(verbose_name = 'Activation code', max_length=50, default=None, null=True)

	class Meta:
		verbose_name = 'Профиль'
		verbose_name_plural = 'Профили'

	def __str__(self):
		return self.user.username


class SmsStatus(models.Model):

	types = ['Принятие заказа Вашей компанией',
		'Номер Вашей карты и заказа, если клиент выбрал оплату картой (Поле для ввода номера карты)',
		'Отправлять номер ТТН смской автоматически после создания (поле для ввода ключа апи НП и поле для ввода ключа Джастин)',
		'Отправлять смс с ссылкой для добавления отзыва Вашей компании после 2 недель после отправки']

	profile = models.OneToOneField(Profile, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'профиль')
	name = models.CharField(verbose_name = 'Смс рассылка', max_length=50, blank=True)
	sms_1 = models.BooleanField(default=False, verbose_name = types[0])
	sms_2 = models.BooleanField(default=False, verbose_name = types[1])
	sms_3 = models.BooleanField(default=False, verbose_name = types[2])
	sms_4 = models.BooleanField(default=False, verbose_name = types[3])

	class Meta:
		verbose_name = 'СМС уведомление'
		verbose_name_plural = 'СМС уведомления'

	def __str__(self):
		return "Статус %s" % self.name

class Role(models.Model):

	name = models.CharField(verbose_name = 'Наименование', max_length=50)
	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Роль'
		verbose_name_plural = 'Роли'

	def __str__(self):
		return "Роль %s" % self.name
