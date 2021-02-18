import requests
import string
from huey import crontab
from datetime import datetime
from dateutil import parser
from dateutil.relativedelta import *
from huey.contrib.djhuey import db_periodic_task, db_task

from order.models import Order, ProductInOrder
from .models import Shop, Profile

PROM_API = 'http://my.prom.ua/api/v1'
SHOP_TOKEN = ''
TELEGRAM_TOKEN = ''

def write_logs(text):
	server_time = datetime.now()
	format_text = "{} | {} \n".format(server_time, text)
	with open("script.log", "a+") as f:
		f.write(format_text)

def date_parse(date_created):
	date_created = parser.parse(date_created) + relativedelta(hours=+2)
	date_created = str(date_created)[:-12]
	return date_created

def my_atoi(str):
	num = ''

	for i in str:
		if i == ' ' or i == '\t':
			continue
		elif i.isdigit():
			num = num + i
		elif i == ',':
			num = num + '.'
		elif i == ' ' or i == '\t':
			break

	return (float(num))

def is_order_new(item):
	try:
		if item["status"] == 'pending':
			return True
		else:
			return False
	except Exception as c:
		print("Error while checking if order is new")
		print("Exception: {}".format(c))
		return False

def make_goods_list(order, ordered_items):
	products_list = []

	for good in ordered_items:
		product = ProductInOrder.objects.create(
			order = order, name = good['name'],
			price_per_item = my_atoi((good['price'])),
			nmb = good['quantity'], item_code = good['id']
		)
		string = "- {}\nК-во: {}\n".format(good['name'], good['quantity'])
		products_list.append(string)
	goods_list = ''.join(products_list)

	return goods_list

def create_new_order(item, shop):
	payment_option = item.get("payment_option", False)
	if payment_option:
		payment_option = payment_option.get("name", "Тип платежа не выбран")

	item_delivery_name = item.get("delivery_option", False)
	if item_delivery_name:
		item_delivery_name = item_delivery_name.get("Name", "")

	order = Order.objects.create(prom_id = item['id'],
		customer_email = item.get("email", ""),
		customer_name = item.get("client_first_name", ""),
		customer_lastname = item.get("client_last_name", ""),
		customer_secondname = item.get("client_second_name", ""),
		customer_phone = item.get("phone", ""),
		customer_address = item.get("delivery_address", ""),
		comment = item.get("client_notes", ""),
		payment_method = payment_option,
		delivery_option = item_delivery_name,
		shop_name = shop
		)

	return order

def send_message_telegram(order_msg, shop):
	managers = Profile.objects.filter(shop=shop, role='Manager',
		telegram_token__isnull=False, telegram_active=True)
	method = 'sendMessage'
	print(managers)
	print(shop)
	for manager in managers:
		response = requests.post(
				url='https://api.telegram.org/bot{0}/{1}'.format(TELEGRAM_TOKEN, method),
				data={'chat_id': manager.telegram_token, 'text': order_msg}
			).json()

def get_new_orders(shop):
	headers = {'Authorization': 'Bearer {}'.format(SHOP_TOKEN),
				'Content-type': 'application/json'}
	session = requests.Session()

	try:
		api_response = session.get(PROM_API + '/orders/list', headers=headers)
	except Exception as c:
		print("Probably Timeouted. Exception: {}".format(c))
		write_logs("Error on request to PromUa API {}. Exception: {}".format(shop.name, c))
	finally:
		try:
			api_response = session.get(PROM_API + '/orders/list', headers=headers)
		except:
			return

	try:
		update_order_status_list = []
		if api_response.status_code == 200:
			info = api_response.json()

		elif api_response.status_code == 401:
			shop.is_active = False
			write_logs("Disabled shop {} for getting a 401 error code".format(shop.name))
		else:
			write_logs("Response code from Prom API wasn't 200 or 401, it's {}. Shop: {}".format(api_response.status_code, shop.name))
			return

		for item in info['orders']:
			#if is_order_new(item) and not Order.objects.filter(prom_id = item['id']).exists():
			if not Order.objects.filter(prom_id = item['id']).exists():
				print("There is a new order")

				order = create_new_order(item, shop)
				date_created = date_parse(item["date_created"])
				shop.number_of_orders = shop.number_of_orders + 1
				goods_list = make_goods_list(order, item["products"])
				cabinet_url = "https://my.prom.ua/cms/order/edit/{}".format(item["id"])
				update_order_status_list.append(item["id"])

				try:
					order_msg = ("Поступил новый заказ! \n\nМагазин: {}\nЭлектронная почта: {} \n"
							"\nЗаказ № {} \nВремя заказа: {} \nОбщая стоимость: {} \n\nЗаказанные товары: \n{} \n\n"
							"Заказчик: \n{} {} {} \nКомментарий к заказу: {} \nНомер телефона: {} \n\n"
							"Адрес доставки: {} \n\n{} \n{} \n"
							"\n\nСсылка на заказ в кабинете: {}").format(
								shop.name, order.customer_email, order.prom_id,
								date_created, order.total_price, goods_list, order.customer_name,
								order.customer_lastname, order.customer_secondname, order.comment, order.customer_phone,
								order.customer_address, order.delivery_option, order.payment_method, cabinet_url)
					send_message_telegram(order_msg, shop)
				except Exception as c:
					print(order.customer_email)
					print("Error on order message formation. Exception: {}".format(c))
					write_logs("Error on order message formation on {}. Exception: {}".format(shop.name, c))
					continue

				write_logs("Adding {} order to Database".format(shop.name))
				print("Adding {} order to Database".format(shop.name))
				#if sms_notification:
				#	message = "Спасибо, Ваш заказ принят!\n{}".format(shop.name)
				#	sms_response = send_sms_to(message, item_phone.replace("+", ""))
				#	if not sms_response:
				#		send_message_to(MY_ID, "SMS Sent failed with error {}.".format(sms_response))

		#if status_update:
		#	if update_order_status_list:
		#		update_order_status(update_order_status_list, headers)

	except Exception as c:
		print("Exception: {}".format(c))
		print("something whent wrong while getting new orders")

@db_periodic_task(crontab(minute='*/1'))
def every_min():
	req_number = 0
	shops = Shop.objects.filter(is_active=True)

	for shop in shops:
		if shop.is_active:
			req_number+=1
			print("{} | Looking for new orders in {}".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), shop.name))
			get_new_orders(shop)
			shop.save()
		else:
			print ("{} | Skipping {} cos its dsbld".format(datetime.now().strftime('%Y-%m-%d %H:%M:%S'), shop.name))
    # This is a periodic task that executes queries.