import telebot
from telebot import types
import sqlite3

token = '6162234981:AAFFNXWvL5Kn4vxG8muF1s3AXwFK4CA2pDo'
bot = telebot.TeleBot(token)

id_login = dict()

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
    if message.text == "Войти":
        if message.chat.id not in id_login.keys():
            bot.send_message(message.chat.id, "Введите имя и пароль через пробел")
            bot.register_next_step_handler(message, login)
        else:
            bot.send_message(message.chat.id, "Вы уже зашли")


    elif message.text == "Регистрация":
        if message.chat.id not in id_login.keys():
            bot.send_message(message.chat.id, "Введите желаемое имя и пароль два раза через пробел")
            bot.register_next_step_handler(message, registration)
        else:
            bot.send_message(message.chat.id, "Вы уже зашли")


    else:
        if message.chat.id in id_login.keys():
            # тут все команды после входа
            if message.text == "Играть":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Города")
                item2 = types.KeyboardButton("Дота 3")
                item3 = types.KeyboardButton("Геншин импакт")
                item4 = types.KeyboardButton("Шелли и Кольт")
                item5 = types.KeyboardButton("Назад")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)
                markup.add(item5)
                bot.send_message(message.chat.id, "Выберите игру из выпадающего списка",reply_markup=markup)
            if message.text == "Профиль":
                con = sqlite3.connect("progress_bd.db")
                cur = con.cursor()
                result = cur.execute(f"""SELECT * FROM progress WHERE login = '{id_login[message.chat.id]}'""").fetchone()
                stroka = f"Имя: {result[1]}"
                con.close()
                bot.send_message(message.chat.id, stroka)
            if message.text == "Выход":
                id_login.pop(message.chat.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Войти")
                item2 = types.KeyboardButton("Регистрация")
                markup.add(item1)
                markup.add(item2)
                bot.send_message(message.chat.id, "Вы успешно вышли из аккаунта",reply_markup=markup)
            if message.text == "Назад":
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Играть")
                item2 = types.KeyboardButton("Профиль")
                item3 = types.KeyboardButton("Выход")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                bot.send_message(message.chat.id, "Назад", reply_markup=markup)


        else:
            bot.send_message(message.chat.id, "Вы ещё не зашли")

def login(message):
    message_text = (message.text).split()
    if len(message_text) == 2:
        con = sqlite3.connect("progress_bd.db")
        cur = con.cursor()
        result = cur.execute(f"""SELECT * FROM progress WHERE login = '{message_text[0]}'""").fetchone()
        con.close()
        if result != None:
            if message_text[0] == result[1] and str(result[2])== message_text[1]:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Играть")
                item2 = types.KeyboardButton("Профиль")
                item3 = types.KeyboardButton("Выход")
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                bot.send_message(message.chat.id, f"Вы успешно зашли под логином {message_text[0]}", reply_markup=markup)
                id_login[message.chat.id] = message_text[0]
            else:
                bot.send_message(message.chat.id, "Неправильный пароль")
        else:
            bot.send_message(message.chat.id, "Неправильный логин")
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода")


def registration(message):
    message_text = (message.text).split()
    if len(message_text) == 3 and message_text[1] == message_text[2]:
        con = sqlite3.connect("progress_bd.db")
        cur = con.cursor()
        if cur.execute(f"""SELECT * FROM progress WHERE login = '{message_text[0]}'""").fetchone() == None:
            cur.execute(f"""INSERT INTO progress(login,password) VALUES ('{message_text[0]}', '{message_text[1]}')""")
            con.commit()
            con.close()
            bot.send_message(message.chat.id,
                             f"Вы успешно зарегестрировались, ваш \nЛогин: {message_text[0]} \nПароль: {message_text[1]}")
        else:
            bot.send_message(message.chat.id, "Такой логин уже занят")
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода")


bot.polling()
