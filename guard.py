# забей, не нужно ///cd c:\users\oguard\desktop\python
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import sqlite3
from telebot import types
import payments

#О базе users и типах данных: userid integer, refs_str text, payment_code text, summary text
# -------------------------ГЛАВНОЕ МЕНЮ-----------------------------------------	

token = 'our_token'

feedback_url = 'https://t.me/dpaulov'
support_url = 'https://t.me/dpaulov'

bot = telebot.TeleBot(token)

# default: @dpaulov, @snidee
admins = [492919279, 659844079]

conn = sqlite3.connect('base.db',0.0,check_same_thread=False)
cursor = conn.cursor()

# КЛАСС ТОВАРА -------------------------------------------------------------------------

class Item:

	code = 'none'
	name = 'none'
	price = 'none'
	description = 'none'
	section = 'none'

	def __str__ (self):
		return ('item: {name = ' + '\'' + self.name + '\', price = ' + self.price + ', description = \'' + self.description + '\', section = ' + self.section + ', code = ' + self.code + '}')

	def __eq__ (self, other):
		return (self.name == other.name) and (self.price == other.price) and (self.description == other.description) and (self.code == other.code)	

	def __init__ (self, code):
		self.code = code

	def change_parameters(self, name, price, description, section):
		self.name = name
		self.price = price
		self.description = description
		self.section = section	
		
	def change_name (self, name):
		self.name = name

	def change_price (self, price):
		self.price = price

	def change_description (self, description):
		self.description = description

	def change_section (self, section):
		self.section = section	


# SENDING BUG REPORTS TO ADMINS

def send_report(text):
	try:
		for adminid in admins:
			bot.send_mesage(adminid, text)
	except:
		pass


# СПИСКИ -------------------------------------------------------------------------------

item1 = Item('1')
item2 = Item('2')
item3 = Item('3')
next_code = 4

item1.change_parameters('Item 1', '500', 'descr1', 'Курсы')
item2.change_parameters('Item 2', '200', 'descr2', 'Базы')
item3.change_parameters('Item 3', '300', 'descr3', 'Базы')

items = [item1, item2, item3]
sections = {'Курсы', 'Схемы', 'Базы', 'Чат-боты', 'Разное'}

# КНОПКИ ------------------------------------------------------------------------------
	# КНОПКИ ГЛАВНОГО МЕНЮ ----------------------------------------------------------
init_markup = InlineKeyboardMarkup()
courses = InlineKeyboardButton(text = 'Товары', callback_data = 'tosections')
referals = InlineKeyboardButton(text = 'Реферальная программа', callback_data = 'referals')
feedback = InlineKeyboardButton(text = 'Отзывы', url = feedback_url)
support = InlineKeyboardButton(text = 'Поддержка', url = support_url)

init_markup.row(courses)
init_markup.row(referals)
init_markup.row(feedback, support)

backtomenu = InlineKeyboardButton(text = 'В меню', callback_data = 'tomenu')
backtosections = InlineKeyboardButton(text = 'К разделам', callback_data = 'tosections')

# ОТПРАВКА ГЛАВНОГО МЕНЮ ---------------------------------------------------------------

def send_init_message(chatid):
	bot.send_message(chatid, 'Добро пожаловать', reply_markup = init_markup)























# ОБРАБОТЧИК КНОПОК ---------------------------------------------------------------------

@bot.callback_query_handler(func = lambda call: True)
def callback_handler(call):

	chatid = call.message.chat.id
	messageid = call.message.message_id

	if(call.data == 'tomenu'):
		send_init_message(chatid)

	elif(call.data == 'tosections'):
		sections_m = InlineKeyboardMarkup()
		
		for section in sections:
			sections_m.add(InlineKeyboardButton(text = section, callback_data = 'sec' + section))
		
		sections_m.add(backtomenu)	
		bot.edit_message_text('Выберите интересующий Вас раздел:',chatid, messageid,reply_markup = sections_m)


# ПРОВЕРКА ПЛАТЕЖА


	elif(call.data == 'checkpay'):
		result = payments.checkQiwiPayment(call.message.chat.id)
		global message_text

		if result == 'more_one':
			message_text = 'bu'
		elif result == 'no_payments':
			message_text = 'ga'
		else:
			message_text = 'ga'

		bot.send_message(call.message.chat.id, )	







	else:
		if 'sec' in call.data:
			
			section_name = call.data[3:]
			section_items = []

			for item in items:
				if (item.section == section_name):
					section_items.append(item)
			text = '<strong>'		
			
			try:
				i = section_items[0]
				text += i.name + '</strong>\n<strong>Цена:</strong> <code>' + i.price	+ ' руб</code>\n' + i.description + '\nКод товара: <code>' + i.code + '</code>'
			except Exception as e:
				text +=  'В данном разделе товары временно отсутствуют</strong>' 	
				 		
			items_m = InlineKeyboardMarkup()
			
			if (len(section_items)>1):
				page = InlineKeyboardButton(text = '.1.', callback_data = 'none')
				next_page = InlineKeyboardButton(text = '2 >', callback_data = section_name + ' page2')
				buy = InlineKeyboardButton(text = 'Купить', callback_data = 'buy ' + section_items[0].code + ' ' + section_name)
				items_m.row(page, next_page)
				items_m.row(buy)
			elif (len(section_items)>0):
				page = InlineKeyboardButton(text = '.1.', callback_data = 'none')
				buy = InlineKeyboardButton(text = 'Купить', callback_data = 'buy ' + section_items[0].code + ' ' + section_name)
				items_m.row(page)
				items_m.row(buy)
			else:
				page = InlineKeyboardButton(text = '.1.', callback_data = 'none')
				items_m.add(page)
			
			items_m.row(backtosections)
			bot.edit_message_text(text, chatid, messageid, reply_markup = items_m, parse_mode = 'HTML')

		elif 'page' in call.data:
			section_name = call.data.split(' ')[0]
			section_items = []
			cur_page = int(call.data.split(' ')[1][4:])

			for item in items:
				if (item.section == section_name):
					section_items.append(item)
			text = '<strong>'		
			
			try:
				i = section_items[cur_page-1]
				text += i.name + '</strong>\n<strong>Цена:</strong> <code>' + i.price	+ ' руб</code>\n' + i.description + '\nКод товара: <code>' + i.code + '</code>'
			except Exception as e:
				text +=  'В данном разделе товары временно отсутствуют</strong>' 	
				 		
			items_m = InlineKeyboardMarkup()
			
			if (len(section_items)>1):
				page = InlineKeyboardButton(text = '.' + str(cur_page) + '.', callback_data = 'none')
				if(cur_page == len(section_items)):
					prev_page = InlineKeyboardButton(text = '< ' + str(cur_page-1), callback_data = section_name + ' page' + str(cur_page-1))
					buy = InlineKeyboardButton(text = 'Купить', callback_data = 'buy ' + section_items[cur_page-1].code + ' ' + section_name)
					items_m.row(prev_page, page)
					items_m.row(buy)
				elif(cur_page < 1):
					next_page = InlineKeyboardButton(text = str(cur_page + 1) + ' >', callback_data = section_name + ' page' + str(cur_page+1))
					prev_page = InlineKeyboardButton(text = '< ' + str(cur_page-1), callback_data = section_name + ' page' + str(cur_page-1))
					buy = InlineKeyboardButton(text = 'Купить', callback_data = 'buy ' + section_items[cur_page-1].code + ' ' + section_name)
					items_m.row(prev_page, page, next_page)
					items_m.row(buy)
				else:
					next_page = InlineKeyboardButton(text = str(cur_page + 1) + ' >', callback_data = section_name + ' page' + str(cur_page+1))
					buy = InlineKeyboardButton(text = 'Купить', callback_data = 'buy ' + section_items[cur_page-1].code + ' ' + section_name)
					items_m.row(page, next_page)
					items_m.row(buy)
			
			elif (len(section_items)>0):
				page = InlineKeyboardButton(text = '.1.', callback_data = 'none')
				buy = InlineKeyboardButton(text = 'Купить', callback_data = 'buy ' + section_items[cur_page-1].code + ' ' + section_name)
				items_m.row(page)
				items_m.row(buy)
			
			else:
				page = InlineKeyboardButton(text = '.1.', callback_data = 'none')
				items_m.add(page)
			
			items_m.add(backtosections)
			bot.edit_message_text(text, chatid, messageid, reply_markup = items_m, parse_mode = 'HTML')					

		elif 'buy' in call.data:
			item_code = str(call.data.split(' ')[1])
			section_name = call.data.split(' ')[2]
			payment_code = payments.getPaymentCode()
			global page
			global summary
			section_items = []

			for item in items:
				if item.section == section_name:
					section_items.append(item)
				

			for item in section_items:
				if item.code == item_code:
					summary = str(item)
					page = str(section_items.index(item) + 1)

			#
			#
			#
			#
			#
			#
			#

			message_text = 'текст да круто' # мне лень писать текст сюда, напиши плез
			buy_markup = InlineKeyboardMarkup()
			check_payment = InlineKeyboardButton(text = 'Проверить платёж', callback_data = 'checkpay')
			back_to_page = InlineKeyboardButton(text = 'Назад к товару', callback_data = section_name + ' page' + )
			bot.send_message(call.message.chat.id, message_text, reply_markup = buy_markup, parse_mode = 'HTML')







# СМЕНА НАЗВАНИЯ ТОВАРА ----------------------------------------------------------

@bot.message_handler(commands = ['changename'])
def changename_handler(message):
	chatid = message.chat.id
	if chatid in admins:
		try:
			text = message.text.split(' ')[1:]
			newname = str()

			for word in text[1:]:
				newname += word + ' '

			for item in items:
				if(item.code == text[0]):
					bot.send_message(chatid, 'Название товара с кодом ' + item.code + ' успешно изменено с <strong>' + item.name + '</strong> на <strong>' + newname + '</strong>', parse_mode = 'HTML')
					item.change_name(newname)	

		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /changename стоит выполнять в формате:\n/changename код_товара Новое название товара.\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')	

# СМЕНА ЦЕНЫ ТОВАРА --------------------------------------------------------------

@bot.message_handler(commands = ['changeprice'])
def changeprice_handler(message):
	chatid = message.chat.id
	if chatid in admins:
		try:
			text = message.text.split(' ')[1:]
			newprice = text[1]

			for item in items:
				if(item.code == text[0]):
					bot.send_message(chatid, 'Цена товара с кодом ' + item.code + ' успешно изменена с <strong>' + item.price + '</strong> на <strong>' + newprice + '</strong>', parse_mode = 'HTML')
					item.change_price(newprice)	

		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /changeprice стоит выполнять в формате:\n/changeprice код_товара Новая цена товара.\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')

# СМЕНА ОПИСАНИЯ ТОВАРА ----------------------------------------------------------

@bot.message_handler(commands = ['changedescr'])
def changedescr_handler(message):
	chatid = message.chat.id
	if chatid in admins:
		try:
			text = message.text.split(' ')[1:]
			newdescr = str()
			
			for word in text[1:]:
				newdescr += word + ' '
			
			for item in items:
				if(item.code == text[0]):
					bot.send_message(chatid, 'Описание товара с кодом ' + item.code + ' успешно изменено с ' + item.description + ' на ' + newdescr, parse_mode = 'HTML')
					item.change_description(newdescr)	
		
		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /changedescr стоит выполнять в формате:\n/changedescr код_товара Новое описание товара.\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')	

# СМЕНА РАЗДЕЛА ТОВАРА --------------------------------------------------------------

@bot.message_handler(commands = ['changeitemsection'])
def changeitemsection_handler(message):
	chatid = message.chat.id
	if chatid in admins:
		try:
			text = message.text.split(' ')[1:]
			newsection = text[1]
			sections.add(newsection)	
			
			for item in items:
				if(item.code == text[0]):
					bot.send_message(chatid, 'Товар с кодом ' + item.code + ' успешно перемещен с раздела <strong>' + item.section + '</strong> в раздел <strong>' + newsection + '</strong>', parse_mode = 'HTML')
					item.change_section(newsection)	
		
		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /changeitemsection стоит выполнять в формате:\n/changeitemsection код_товара Новый раздел товара.\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')		

# ДОБАВЛЕНИЕ НОВОГО ТОВАРА --------------------------------------------------------

@bot.message_handler(commands = ['additem'])
def additem_handler(message):
	global next_code
	chatid = message.chat.id
	if chatid in admins:
		try:
			text = message.text[9:]
			params = text.split('~')
			newname = params[0]
			newprice = params[1]
			a=int(newprice)
			newdescr = params[2]
			newsection = 'Разное'

			try:
				arr=list(params[3])
				newsection=arr[0].upper()
				for a in range(1,len(arr)):
					newsection+=arr[a]
				print(newsection)
				sections.add(newsection)
			except Exception as e2:
				print('', end = '')

			newitem = Item(str(next_code))
			next_code += 1
			newitem.change_parameters(newname, newprice, newdescr, newsection)
			items.append(newitem)	
			bot.send_message(chatid, 'Был добавлен товар с кодом ' + newitem.code + ', названием <strong>' + newitem.name + '</strong>, ценой в <strong>' + newitem.price + '</strong> руб, с описанием: ' + newitem.description + ' в раздел ' + newitem.section, parse_mode = 'HTML')
		
		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /additem стоит выполнять в формате:\n/additem Название нового товара~Цена товара~Описание товара~Раздел товара (ОПЦИОНАЛЬНО).\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')				

# УДАЛЕНИЕ ТОВАРА -----------------------------------------------------------------

@bot.message_handler(commands = ['deleteitem'])
def deleteitem_handler(message):
	chatid = message.chat.id
	if chatid in admins:
		try:
			code = message.text.split(' ')[1]
			
			for item in items:
				if(item.code == code):
					bot.send_message(chatid, 'Товар с кодом ' + item.code + ' успешно удален с раздела <strong>' + item.section + '</strong>', parse_mode = 'HTML')
					items.remove(item)	
		
		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /deleteitem стоит выполнять в формате:\n/deleteitem код_товара.s\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')	

# СМЕНА НАЗВАНИЯ РАЗДЕЛА -----------------------------------------------------------

@bot.message_handler(commands = ['changesection'])
def changesection_handler(message):
	chatid = message.chat.id
	if chatid in admins:
		try:
			section = message.text.split(' ')[1]
			newname = message.text.split(' ')[2]
			
			for item in items:
				if(item.section == section):
					item.change_section(newname)
			
			for section2 in sections:
				if(section == section2):
					bot.send_message(chatid, 'Раздел <strong>' + section + '</strong> успешно переименован в <strong>' + newname + '</strong>', parse_mode = 'HTML')
					sections.remove(section)
					sections.add(newname)	
		
		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /changesection стоит выполнять в формате:\n/changesection старое_название_раздела новое_название_раздела.s\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')	



# УДАЛЕНИЕ РАЗДЕЛА ---------------------------------------------------------------

@bot.message_handler(commands = ['deletesection'])
def deletesection_handler(message):
	chatid = message.chat.id
	if chatid in admins:
		try:
			section = message.text.split(' ')[1]
			
			for item in items:
				if(item.section == section):
					item.change_section('Разное')
			
			for section2 in sections:
				if(section == section2):
					bot.send_message(chatid, 'Раздел <strong>' + section + '</strong> успешно удалён. Всё его содержимое перемещено в раздел <strong>Разное</strong>.', parse_mode = 'HTML')
					sections.remove(section)
		
		except Exception as e:
			bot.send_message(chatid, 'Возникла ошибка при введении команды.\nКоманду /deletesection стоит выполнять в формате:\n/deletesection название_раздела.\nПодробности ошибки: ' + str(e))	
	
	else:
		bot.send_message(chatid, 'У вас нет доступа к данной команде.')

# ДОБАВЛЕНИЕ НОВОГО ЮЗЕРА В КАЧЕСТВЕ РЕФЕРАЛА-----------

def addref(refid,newuserid): 
	try:
		cursor.execute("SELECT refs_str FROM users WHERE chatid=?",(refid,)) #Taking current refid`s referals
		currefs=cursor.fetchall()[0][0]
		cursor.execute("UPDATE users SET refs_str=?",(currefs+' '+newuserid)) #Adding newuserid to refs_str
		conn.commit()
	except Exception as e:
		bot.send_report(e)

# ПРОВЕРКА ЗАПУСКА БОТА -------------------------------------------------------------

@bot.message_handler(commands = ['start'])
def message_handler(message):
	chatid = message.chat.id
	send_init_message(chatid)
	cursor.execute("SELECT * FROM users WHERE userid=?",(message.chat.id,))
	if len(cursor.fetchall())==0: 
		cursor.execute("INSERT INTO users VALUES (?,?,?,?)",(chatid, '','','',))
		#userid integer, refs_str text, payment_code text, summary text
		conn.commit()
		addref(message.text[7:],message.chat.id)

# СОХРАНЕНИЕ В БД ПРИ КОМАНДЕ /SAVE ----------------------------------------------

@bot.message_handler(commands = ['save'])
def savebase(message):
	if message.chat.id in admins:
		try:
			for section in sections:
				cursor.execute("INSERT INTO sections VALUES (?)",(section,))
				conn.commit()
			bot.send_message(message.chat.id, 'Все данные успешно сохранены в базу данных.')	
		except Exception as e:
			print(e)
			bot.send_message(message.chat.id, 'При сохранении что-то пошло не так.\n Подробности ошибки: ' + str(e))
	else:
		bot.send_message(message.chat.id, 'У вас нет доступа к данной команде.')			



# ВЫГРУЗКА ИЗ БД НА СТАРТЕ --------------------

def loadbase():
	try:
		conn.commit()
		cursor.execute("""SELECT * FROM sections""")
		for i in cursor.fetchall():
			sections.add(i[0])
		cursor.execute("""DELETE FROM sections""")
		conn.commit()	
	except Exception as e:
		print(e)
		cursor.execute("""CREATE TABLE sections (name text)""")
		conn.commit()		


# ИНИЦИАЛИЗАЦИЯ ---------------------

def starting():
	loadbase()
	try: 
		cursor.execute("CREATE TABLE users (userid integer, refs_str text, payment_code text, summary text)")
		conn.commit()
	except:
		print('Таблица "users" уже существует, работаем...')

starting()


bot.polling()
