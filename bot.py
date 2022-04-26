import pyowm
import pyowm.exceptions
import requests
import telebot
from pyowm.exceptions import api_response_error
import config
from pogoda import get_forecast
from ZaWarudo import get_time
import xml.etree.ElementTree as ET
from urllib.request import urlopen



#Exchange_rate
def get_valutes():
    url = 'http://www.cbr.ru/scripts/XML_daily.asp?'
    with urlopen(url, timeout=10) as usd:
        current_value_usd = ET.parse(usd).findtext('.//Valute[@ID="R01235"]/Value')
        str_usd = 'USD: ' + current_value_usd
        print(str_usd)

    with urlopen(url, timeout=10) as eur:
        current_value_eur = ET.parse(eur).findtext('.//Valute[@ID="R01239"]/Value')
        str_eur = 'EUR: ' + current_value_eur
        print(str_eur)

    return str_usd + "\n" + str_eur

bot = telebot.TeleBot(config.token,threaded=False)

@bot.message_handler(commands=['start'])
def command_start(message):
    start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    start_markup.row('/start', '/help', '/hide')
    start_markup.row('/weather', '/world_time', '/Exchange_rate')
    bot.send_message(message.chat.id, "🤖 Бот работает!\n⚙ Нажмите /help чтобы увидеть функции бота")
    bot.send_message(message.from_user.id, "⌨️ Клавиатура успешно добавлена\n⌨️ /hide Чтобы ее убрать ", reply_markup=start_markup)

@bot.message_handler(commands=['hide'])
def command_hide(message):
	hide_markup = telebot.types.ReplyKeyboardRemove()
	bot.send_message(message.chat.id, "⌨💤...", reply_markup=hide_markup)


@bot.message_handler(commands=['help'])
def command_help(message):
	bot.send_message(message.chat.id, "✍ /start - Клавиатура дисплея\n"
									  "☁ /weather - Погода\n"
									  "⌛ /world_time - Время \n"
									  "$ /Exchange_rate- Валюта на сегодня \n")




@bot.message_handler(commands=['weather'])
def command_weather(message):
    sent = bot.send_message(message.chat.id, "🗺 Укажите страну или город\n🔍 Пример: Россия или Москва 🗺")
    bot.register_next_step_handler(sent, send_forecast)


def send_forecast(message):
    try:
        get_forecast(message.text)
    except pyowm.exceptions.api_response_error.NotFoundError:
        bot.send_message(message.chat.id, "❌  Ошиблись местом или допустили ошибку, попробуйте еще раз  ❌ ")
    forecast = get_forecast(message.text)
    bot.send_message(message.chat.id, forecast)

@bot.message_handler(commands=['world_time'])
def command_world_time(message):
	sent = bot.send_message(message.chat.id, "🗺 Укажите страну или город\n🔍 Пример: Россия или Москва 🗺")
	bot.register_next_step_handler(sent, send_time)


def send_time(message):
	try:
		get_time(message.text)
	except IndexError:
		bot.send_message(message.chat.id, "❌  Ошиблись местом или допустили ошибку, попробуйте еще раз  ❌ " )
	time = get_time(message.text)
	bot.send_message(message.chat.id, time)


@bot.message_handler(commands=['Exchange_rate'])
def handle_text(message):
	bot.send_message(message.chat.id, get_valutes())

@bot.callback_query_handler(func=lambda c:True)
def inline(c):
	if c.data == 'USD':
		bot.send_message(c.message.chat.id, f"{usd('USD')} UAH")

	if c.data == 'EUR':
		bot.send_message(c.message.chat.id, f"{usd('EUR')} UAH")

	if c.data == 'RUB':
		bot.send_message(c.message.chat.id, f"{usd('RUB')} UAH")

def usd(rat):
	text = requests.get('http://resources.finance.ua/ua/public/currency-cash.json').json()
	return (text['organizations'][0]['currencies'][rat]['ask'])

def send_rus_trans(message):
	start_markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True,
													 one_time_keyboard=False)
	start_markup.row('/start', '/help', '/hide')
	start_markup.row('/weather', '/world_time', '/news')
	start_markup.row('/crypto', '/stocks', '/translate')
	bot.send_message(message.chat.id, to_ru(message.text), reply_markup=start_markup)





while True:
	try:
		bot.infinity_polling(True)
	except Exception:
		tm.sleep(1)