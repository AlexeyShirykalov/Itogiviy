import telebot
import requests

bot_token = '5991343824:AAFioU2OT7NJ3OUjJf6cBSBOUz83Szfl-Gk'
bot = telebot.TeleBot(bot_token)

url = 'https://www.cbr-xml-daily.ru/daily_json.js'

response = requests.get(url)
data = response.json()
usd_rate = data['Valute']['USD']['Value']
eur_rate = data['Valute']['EUR']['Value']

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message,
                 "Привет! Я бот для конвертации валют. Чтобы узнать курс, введите сообщение в формате"
                 " 'доллар, рубль, количество'")

@bot.message_handler(func=lambda message: True)
def convert(message):
    try:
        currency_from, currency_to, amount = message.text.split(',')
        amount = float(amount)
        currency_from = currency_from.strip().lower()
        currency_to = currency_to.strip().lower()

        if currency_from == 'доллар':
            currency_from_rate = usd_rate
        elif currency_from in ('евро', 'евр'):
            currency_from_rate = eur_rate
        else:
            bot.reply_to(message, "Я не знаю курс этой валюты")
            return

        if currency_to == 'рубль':
            currency_to_rate = 1
        elif currency_to in ('доллар', 'бакс'):
            currency_to_rate = 1 / usd_rate
        elif currency_to in ('евро', 'евр'):
            currency_to_rate = 1 / eur_rate
        else:
            bot.reply_to(message, "Я не знаю курс этой валюты")
            return

        converted_amount = round(amount * currency_from_rate * currency_to_rate, 2)
        reply_message = f'{amount} {currency_from} = {converted_amount} {currency_to}'
        bot.reply_to(message, reply_message)

    except Exception as ex:
        print(ex)
        bot.reply_to(message, "Я не понимаю это сообщение")

if __name__ == '__main__':
    bot.polling(none_stop=True)