import telebot

token= '6162234981:AAFFNXWvL5Kn4vxG8muF1s3AXwFK4CA2pDo'
bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_message(message):
  print(message.chat.id)
  bot.send_message(message.chat.id, "привет")


bot.infinity_polling()