from SimpleQIWI import QApi
import random
import datetime
import sqlite3

conn=sqlite3.connect('base.db',0.0,check_same_thread=False)
cursor=conn.cursor()

api=QApi(token='',phone='') #phone format is '79998882233' without '+' //Okay, ponyal

def getPaymentCode():
	code=''
	letter_dict='ABCDEFGHIJKLMFVNOPQRS'
	num_dict='123456789012398723457'
	for i in range(1,10): #second parameter is max lenght of payment code
		a=random.randint(1,20)
		if a%2==0:
			code+=letter_dict[a]
		else:
			code+=num_dict[a]
	return code

def checkQiwiPayment(userid):
	payments=0
	today=str(datetime.datetime.today()).split()[0]
	yesterday=str(datetime.datetime.today()-datetime.timedelta(days=1)).split()[0]
	cursor.execute("SELECT payment_code FROM users WHERE chatid=?",(userid,))
	payment_code=cursor.fetchall()[0][0]
	cursor.execute("SELECT summary FROM users WHERE chatid=?",(userid,))
	summary=int(cursor.fetchall()[0][0])
	for i in api._get_payments()['data']:
		if i['comment']==payment_code and i['date'].split()[0] in [today,yesterday] and i['sum']['amount']==summary and i['sum']['currency']==643:
			#currency 643 - russian rubles
			payments+=1
	if payments>1:
		return 'more_one'
	elif payments==0:
		return 'no_payments'
		#bot.send_message(NNNN, 'New payment. Amount: '+i['sum']['amount']+' rub.')
		#Create a bot object for turning on payment notifications
	elif payments==1:
		return 'success'



