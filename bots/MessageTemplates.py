# -*- coding: utf-8 -*-

NEW_ORDER_MESSAGE = ("Поступил новый заказ! \n\nМагазин: {shop_name}\nЭлектронная почта: {email} \n"
					"\nЗаказ № {order_number} \nВремя заказа: {order_time}"
					"\nОбщая стоимость: {cost} \n\nЗаказанные товары: \n{goods}\n\n"
					"Заказчик: \n{last_name} {first_name} {second_name}"
					"\nКомментарий к заказу: {commentary} \nНомер телефона: {phone} \n\n"
					"Адрес доставки: {delivery} \n\n{delivery_name} \n{payment_option} \n"
					"\n\nСсылка на заказ в кабинете: {cabinet_url}")
ORDER_THANKS_MESSAGE = "Спасибо, Ваш заказ принят!\n{shop_name}"

VIBER_GREETING_MESSAGE = "Здравствуйте, я Автобот Prom.ua и я помогу Вам обрабатывать заказы быстрее, давайте начнем!\n" \
						"Для начала - введите пожалуйста ваш код активации, который вы получили от менеджера"

VIBER_ACTIVATION_CODE_MESSAGE = "\nВведите ваш 'код активации', который вам прислал ваш менеджер!"


VIBER_ACTIVATED_BOT_MESSAGE = "\nВы успешно активировали VIOprom бота, контакты службы поддержки "

VIBER_WRONG_ACTIVATION_CODE_MESSAGE = "\nНеверный код активации : {}"

VIBER_ACTIVATED_CODE_MESSAGE = "\nВы уже активировали данного бота!"

TELEGRAM_GREETING_MESSAGE = "Здравствуйте, {name}!\n" \
							"Я Автобот Prom.ua и я помогу Вам обрабатывать заказы быстрее, давайте начнем!" \
							" Для начала - введите пожалуйста ваш код активации, который вы получили от менеджера"

TELEGRAM_ACTIVATED_BOT_MESSAGE = "\nВы успешно активировали VIOprom бота, контакты службы поддержки "

VIBER_API_KEY_REQUEST = "Введите пожалуйста ваш ключ к API, он должен был прийти вам на почту от службы поддержки Prom.UA\n" \

FINISH_MESSAGE = "Вы успешно активировали VIOprom бота, контакты службы поддержки ." \
				"Если у вас остались какие-либо вопросы свяжитесь пожалуйста с нашим менеджером\n"