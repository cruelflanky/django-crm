from django.db import models
from django.urls import reverse
from django.db.models.signals import post_save

from clients.models import Profile, Shop

# Create your models here.

class Status(models.Model):

	name = models.CharField(verbose_name = 'категория', max_length=50)
	is_active = models.BooleanField(default=True)

	created = models.DateTimeField(auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Статус заказа'
		verbose_name_plural = 'Статусы заказа'

	def __str__(self):
		return "Статус %s" % self.name

class Order(models.Model):

	shop_name = models.ForeignKey(Shop, on_delete=models.CASCADE, verbose_name = 'магазин', null=True)
	prom_id = models.CharField(verbose_name = 'id', max_length=51, null=True, default=None)
	customer_name = models.CharField(verbose_name = 'имя', max_length=50)
	customer_lastname = models.CharField(verbose_name = 'фамилия', max_length=50, null=True, default=None)
	customer_secondname = models.CharField(verbose_name = 'отчество', max_length=50, null=True, default=None)
	customer_email = models.EmailField(verbose_name = 'почта', blank=True, null=True, default=None)
	customer_phone = models.CharField(verbose_name = 'номер тел', max_length=15, null=True, default=None)
	customer_address = models.CharField(verbose_name = 'адрес', max_length=250, null=True,default=None)
	total_price = models.DecimalField(verbose_name = 'общая стоимость', max_digits=9, decimal_places=1, default=0) #total price for all products in order
	comment = models.TextField(blank=True, null=True, default=None)
	status = models.ForeignKey(Status, on_delete=models.SET_NULL, verbose_name = 'статус', null=True, default=None)
	payment_method = models.CharField(verbose_name = 'вид платежа', max_length=150, null=True, default=None)
	delivery_option = models.CharField(verbose_name = 'способ доставки', max_length=150, null=True, default=None)

	created = models.DateTimeField(verbose_name = 'создан', auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name = 'обновлен', auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

	def __str__(self):
		return "Заказ %s" % (self.id)

	def save(self, *args, **kwargs):
		super(Order, self).save(*args, **kwargs)

class ProductInOrder(models.Model):
	name = models.CharField(verbose_name = 'имя', max_length=250, blank=True)
	order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, default=None, verbose_name = 'заказ')
	nmb = models.IntegerField(default=1, verbose_name = 'кол-во')
	item_code = models.IntegerField(default=0, verbose_name = 'код')
	price_per_item = models.DecimalField(max_digits=6, decimal_places=1, default=0, verbose_name = 'цена за шт')
	total_price = models.DecimalField(max_digits=9, decimal_places=1, default=0, verbose_name = 'общая стоимость') #price*nmb

	created = models.DateTimeField(verbose_name = 'создан', auto_now_add=True, auto_now=False)
	updated = models.DateTimeField(verbose_name = 'обновлен', auto_now_add=False, auto_now=True)

	class Meta:
		verbose_name = 'Товар в заказе'
		verbose_name_plural = 'Товары в заказе'

	def __str__(self):
		return "%s" % self.name

	def save(self, *args, **kwargs):
		price_per_item = self.price_per_item
		self.total_price = int(self.nmb) * price_per_item

		super(ProductInOrder, self).save(*args, **kwargs)

def products_in_order_post_save(sender, instance, created, **kwargs):

	order = instance.order
	order_total_price = 0

	all_products_in_order = ProductInOrder.objects.filter(order=order)

	for item in all_products_in_order:
		order_total_price += item.total_price

	instance.order.total_price = order_total_price
	instance.order.save(force_update=True)

post_save.connect(products_in_order_post_save, sender=ProductInOrder)
