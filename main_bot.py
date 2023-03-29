import telebot
from telebot import types

token= '6162234981:AAFFNXWvL5Kn4vxG8muF1s3AXwFK4CA2pDo'
bot = telebot.TeleBot(token)

slovar_login = dict()


@bot.message_handler(commands=['start'])
def start_message(message):
  print(message.chat.id)
  markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
  item1 = types.KeyboardButton("Войти")
  item2 = types.KeyboardButton("Регистрация")
  markup.add(item1)
  markup.add(item2)

  bot.send_message(message.chat.id,
                   "Приветсвую тебя. Прежде чем начать пожалуйста войдите в аккаунт, либо создайте его",
                   reply_markup=markup)

@bot.message_handler(content_types='text')
def message_reply(message):
    if message.text=="Войти":
        bot.send_message(message.chat.id,"Введите имя и пароль через пробел")
        bot.register_next_step_handler(message, login)

    if message.text=="Регистрация":
        bot.send_message(message.chat.id,"Введите желаемое имя и пароль два раза через пробел")
        bot.register_next_step_handler(message, registration)

def login(message):
  message_text = (message.text).split()
  if len(message_text) == 2:
    if message_text[0] in slovar_login and slovar_login[message_text[0]] == message_text[1]:
      bot.send_message(message.chat.id, f"Вы успешно зашли под логином {message_text[0]}")
    else:
      bot.send_message(message.chat.id, "Неправильный логин или пароль")
  else:
    bot.send_message(message.chat.id, "Неправильный формат ввода")

def registration(message):
  message_text = (message.text).split()
  if len(message_text) == 3 and message_text[1] == message_text[2]:
    slovar_login[message_text[0]] = message_text[1]
    print(slovar_login)
  else:
    bot.send_message(message.chat.id, "Неправильный формат ввода")

bot.infinity_polling()
