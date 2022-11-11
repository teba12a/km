from pyrogram import Client,filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from config import *
import threading
import requests
import random
import redis
import time
import json
import os
from email.mime.text import MIMEText
from email.header import Header
import smtplib
R = redis.Redis(charset="utf-8", decode_responses=True)
app = Client("Mail"+BOT_ID,bot_token=TOKEN,api_id = API_ID, api_hash = API_HASH)
def updateCallback(client, callback_query,redis):
	userID = callback_query.from_user.id
	chatID = callback_query.message.chat.id
	userFN = callback_query.from_user.first_name
	title = callback_query.message.chat.title
	message_id = callback_query.message.id
	date = callback_query.data
	if date == "bkk":
		kup = InlineKeyboardMarkup([[InlineKeyboardButton("تعيين اميل",callback_data="setmail"),InlineKeyboardButton("تعيين عنوان",callback_data="setTit"),InlineKeyboardButton("تعيين كليشة",callback_data="settxt")],[InlineKeyboardButton("بدء spam",callback_data="spam")],[InlineKeyboardButton("العمالقة",url="T.ME/TM_BOYKA")]])
		redis.delete("{}:{}:Type".format(BOT_ID,userID))
		app.answer_callback_query(callback_query.id, text="تم اللغاء الامر بنجاح")
		app.edit_message_text(chatID, message_id,"• اهلا بك في بوت الرفع .\n• يمكنك ارسال رسائل بريدية عن طريق اضافه اميلات هذا البوت تابع لـ تيم العمالقة . \n ᡕᠵ᠊ᡃ່࡚ࠢ࠘ ⸝່ࠡࠣ᠊߯᠆ࠣ࠘ᡁࠣ࠘᠊᠊ࠢ࠘𐡏 ¦ 𝑺𝑨𝑺 ┋ 𝑇𝑀\n [Developer Khaild](t.me/E_M_K) ", disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN,reply_markup=kup)
	if date == "spam":
		if not redis.get("{}:{}:title".format(BOT_ID,userID)):
			app.answer_callback_query(callback_query.id, text="⚠️ لم تقم بتعيين عنوان لرسالتك .")
			return False
		if not redis.get("{}:{}:txt".format(BOT_ID,userID)):
			app.answer_callback_query(callback_query.id, text="⚠️ لم تقم بتعيين كليشه رسالتك .")
			return False
		if not redis.get("{}:{}:mail".format(BOT_ID,userID)) and not redis.get("{}:{}:mailpas".format(BOT_ID,userID)):
			app.answer_callback_query(callback_query.id, text="⚠️ لم تقم بتعيين اميل .")
			return False
		app.edit_message_text(chatID, message_id, "قم بارسال البريد الذي تريد ارسال الرساله اليه")
		redis.set("{}:{}:Type".format(BOT_ID,userID),"mailto")
	if date == "setTit":
		kup = InlineKeyboardMarkup([[InlineKeyboardButton("رجوع",callback_data="bkk")]])
		redis.set("{}:{}:Type".format(BOT_ID,userID),"setTit")
		app.answer_callback_query(callback_query.id, text="انت الان تعدل العنوان")
		app.edit_message_text(chatID, message_id, "ارسل عنوان الرساله الان .", disable_web_page_preview=True,reply_markup=kup)
	if date == "settxt":
		kup = InlineKeyboardMarkup([[InlineKeyboardButton("رجوع",callback_data="bkk")]])
		redis.set("{}:{}:Type".format(BOT_ID,userID),"settxt")
		app.answer_callback_query(callback_query.id, text="انت الان تعدل الكليشه المرسله")
		app.edit_message_text(chatID, message_id, "قم بارسال الكليشه التي تود ارسالها", disable_web_page_preview=True,reply_markup=kup)
	if date == "setmail":
		kup = InlineKeyboardMarkup([[InlineKeyboardButton("رجوع",callback_data="bkk")]])
		redis.set("{}:{}:Type".format(BOT_ID,userID),"mail")
		app.edit_message_text(chatID, message_id, "ارسل البريد الخاص بك الان . \n يجب ان يكون gmail .", disable_web_page_preview=True,reply_markup=kup)
		if redis.get("{}:{}:mail".format(BOT_ID,userID)):
			app.answer_callback_query(callback_query.id, text="انت الان تعدل البريد الخاص بك")
		else:
			app.answer_callback_query(callback_query.id, text="انت الان تعمل على تعيين بريد خاص بك ")
@app.on_callback_query()
def callback(client, callback_query ):
    t = threading.Thread(target=updateCallback,args=(client, callback_query,R))
    t.daemon = True
    t.start()
def updateHandlers(client, message,redis):
	type = message.chat.type
	messageID = message.id
	userID = message.from_user.id
	chatID = message.chat.id
	text = message.text
	title = message.chat.title
	if userID == SUDO:
		if text ==  '/start':
			kup = InlineKeyboardMarkup([[InlineKeyboardButton("تعيين اميل",callback_data="setmail"),InlineKeyboardButton("تعيين عنوان",callback_data="setTit"),InlineKeyboardButton("تعيين كليشة",callback_data="settxt")],[InlineKeyboardButton("بدء spam",callback_data="spam")],[InlineKeyboardButton("العمالقة",url="T.ME/TM_BOYKA")]])
			message.reply_text("• اهلا بك في بوت الرفع .\n• يمكنك ارسال رسائل بريدية عن طريق اضافه اميلات هذا البوت تابع لـ تيم العمالقة . \n ᡕᠵ᠊ᡃ່࡚ࠢ࠘ ⸝່ࠡࠣ᠊߯᠆ࠣ࠘ᡁࠣ࠘᠊᠊ࠢ࠘𐡏 ¦ 𝑺𝑨𝑺 ┋ 𝑇𝑀\n [Developer Khaild](t.me/E_M_K) ", quote=True, disable_web_page_preview=True, parse_mode=ParseMode.MARKDOWN,reply_markup=kup)
		if text and redis.get("{}:{}:Type".format(BOT_ID,userID)) == "setTit":
			redis.set("{}:{}:title".format(BOT_ID,userID),text)
			redis.delete("{}:{}:Type".format(BOT_ID,userID))
			message.reply_text("تم حفظ العنوان بنجاح", quote=True)
		if text and redis.get("{}:{}:Type".format(BOT_ID,userID)) == "settxt":
			redis.set("{}:{}:txt".format(BOT_ID,userID),text)
			redis.delete("{}:{}:Type".format(BOT_ID,userID))
			message.reply_text("تم حفظ الكليشه بنجاح", quote=True)
		if text and redis.get("{}:{}:Type".format(BOT_ID,userID)) == "mailpas":
			redis.set("{}:{}:mailpas".format(BOT_ID,userID),text)
			redis.delete("{}:{}:Type".format(BOT_ID,userID))
			message.reply_text("تم حفظ كلمه المرور بنجاح", quote=True)
		if text and redis.get("{}:{}:Type".format(BOT_ID,userID)) == "mailto":
			if '@' in text:
				redis.set("{}:{}:mailto".format(BOT_ID,userID),text)
				redis.delete("{}:{}:Type".format(BOT_ID,userID))
				message.reply_text("• تم تنفيذ الامر بنجاح .", quote=True)
				server = smtplib.SMTP("smtp.gmail.com",587)
				server.ehlo()
				server.starttls()
				server.login(redis.get("{}:{}:mail".format(BOT_ID,userID)),redis.get("{}:{}:mailpas".format(BOT_ID,userID)))
				Body = redis.get("{}:{}:txt".format(BOT_ID,userID))
				title = redis.get("{}:{}:title".format(BOT_ID,userID))
				messagemail = MIMEText(Body, 'plain', 'utf-8')
				messagemail ['Subject'] = Header(title, 'utf-8')
				messagemail ['From'] = Header(redis.get("{}:{}:mail".format(BOT_ID,userID)), 'utf-8')
				messagemail ['To'] = Header(redis.get("{}:{}:mailto".format(BOT_ID,userID)), 'utf-8')
				for b in range(10):
					server.sendmail(redis.get("{}:{}:mail".format(BOT_ID,userID)),redis.get("{}:{}:mailto".format(BOT_ID,userID)),messagemail.as_string())
					server.sendmail(redis.get("{}:{}:mail".format(BOT_ID,userID)),redis.get("{}:{}:mailto".format(BOT_ID,userID)),messagemail.as_string())
					server.sendmail(redis.get("{}:{}:mail".format(BOT_ID,userID)),redis.get("{}:{}:mailto".format(BOT_ID,userID)),messagemail.as_string())
					server.sendmail(redis.get("{}:{}:mail".format(BOT_ID,userID)),redis.get("{}:{}:mailto".format(BOT_ID,userID)),messagemail.as_string())
					server.sendmail(redis.get("{}:{}:mail".format(BOT_ID,userID)),redis.get("{}:{}:mailto".format(BOT_ID,userID)),messagemail.as_string())
				server.quit()
		if text and redis.get("{}:{}:Type".format(BOT_ID,userID)) == "mail":
			if '@gmail.com' in text:
				redis.set("{}:{}:mail".format(BOT_ID,userID),text)
				redis.set("{}:{}:Type".format(BOT_ID,userID),"mailpas")
				message.reply_text("تم حفظ البريد بنجاح \n ارسل الان كلمه المرور الخاصه بالبريد", quote=True)
			else:
				message.reply_text("تاكد من ان البريد المرسل هو gmail.", quote=True)
@app.on_message(filters.private)
def update(client, message):
	t = threading.Thread(target=updateHandlers,args=(client, message,R))
	t.daemon = True
	t.start()
app.run()