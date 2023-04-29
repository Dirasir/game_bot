import telebot
from telebot import types
import sqlite3
import requests
from data import db_session
from data.users import User

token = '6162234981:AAFFNXWvL5Kn4vxG8muF1s3AXwFK4CA2pDo'
bot = telebot.TeleBot(token)

db_session.global_init("db/progress_bd.db")

queue_gorod = list()
rooms_gorod = list()
id_login = dict()

@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Войти")
    item2 = types.KeyboardButton("Регистрация")
    markup.add(item1)
    markup.add(item2)

    bot.send_message(message.chat.id,
                     "Приветсвую тебя. Прежде чем начать пожалуйста войдите в аккаунт, либо создайте его",
                     reply_markup=markup)


@bot.message_handler(content_types='text')
@bot.message_handler(content_types=['photo'])
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
                markup = PlayWindow()
                bot.send_message(message.chat.id, "Выберите игру из выпадающего списка",reply_markup=markup)

            if message.text == "Профиль":
                db_sess = db_session.create_session()
                for user in db_sess.query(User).filter(User.login.like(id_login[message.chat.id])):
                    stroka = f"Имя: {user.login}"
                    str2 = f"ммр: {user.mmr}"
                    bot.send_message(message.chat.id, stroka)
                    bot.send_message(message.chat.id, str2)

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

            if message.text == "Города":
                queue_gorod.append(message.chat.id)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton("Отмена игры в города")
                markup.add(item1)
                bot.send_message(message.chat.id, 'Поиск.....', reply_markup=markup)
                if len(queue_gorod) == 2:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton("Сдаться в городах")
                    markup.add(item1)
                    rooms_gorod.append([queue_gorod[0],[], queue_gorod[1], [] ])
                    mess1 = bot.send_message(queue_gorod[0], 'Игра нашлась!Вы ходите первым', reply_markup=markup)
                    mess2 = bot.send_message(queue_gorod[1], 'Игра нашлась!Вы ходите вторым', reply_markup=markup)
                    queue_gorod.clear()
                    bot.register_next_step_handler(mess1, Goroda)
                print(queue_gorod)
                print(rooms_gorod)

            if message.text == "Отмена игры в города":
                queue_gorod.remove(message.chat.id)
                markup = PlayWindow()
                bot.send_message(message.chat.id, "Выберите игру из выпадающего списка", reply_markup=markup)

            if message.text == "Шелли и Кольт":
                bot.send_message(message.chat.id, "https://www.youtube.com/watch?v=PhzV2kodm0I")

            if message.text == "Геншин импакт":
                photo_url = "https://yandex.ru/images/search?from=tabbar&img_url=http://i.ytimg.com/vi/KIkww1il8Sg/maxresdefault.jpg&lr=239&pos=2&rpt=simage&text=аниме говно"
                bot.send_photo(message.chat.id, photo=photo_url, caption="зря...")
        else:
            bot.send_message(message.chat.id, "Вы ещё не зашли")
def PlayWindow():
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
    return markup

def Goroda(message, last_bykva=None):
    ban = ['ь', 'й', 'ы', 'ъ']
    if last_bykva == None:
        last_bykva = message.text[0]
    for i in rooms_gorod:
        toponym_address = ""
        if message.chat.id in i:
            geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode='{message.text}',+1&format=json"
            response = requests.get(geocoder_request)
            try:

                if response:
                    json_response = response.json()
                    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
                    toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["kind"]

            except IndexError:
                bot.register_next_step_handler(message, Goroda, last_bykva)
                bot.send_message(message.chat.id,
                                 "ошибка, проверьте правильно ли вы ввели название города. 1")
                break
            if last_bykva.lower() == message.text[0].lower() and toponym_address == "locality" and message.text not in i[1]:
                i[1].append(message.text)
                mess2 = bot.send_message(i[i.index(message.chat.id) - 2], message.text)
                if mess2.text[-1] in ban:
                    last_bykva = mess2.text[-2]
                else:
                    last_bykva = mess2.text[-1]
                bot.register_next_step_handler(mess2, Goroda, last_bykva)
                break
            elif message.text == "Сдаться в городах":
                markup = PlayWindow()
                db_sess = db_session.create_session()
                bot.send_message(message.chat.id, "Вы проиграли", reply_markup=markup)
                for user in db_sess.query(User).filter(User.login.like(id_login[message.chat.id])):
                    user.mmr -= 10
                    db_sess.commit()
                for i in rooms_gorod:
                    if message.chat.id in i:
                        for user in db_sess.query(User).filter(User.login.like(id_login[i[i.index(message.chat.id) - 2]])):
                            user.mmr += 10
                            db_sess.commit()
                        bot.send_message(i[i.index(message.chat.id) - 2], "Вы выйграли", reply_markup=markup)
                        rooms_gorod.remove(i)
                        break
            else:
                bot.register_next_step_handler(message, Goroda, last_bykva)
                bot.send_message(message.chat.id, "ошибка, проверьте правильно ли вы ввели название города или же этот город уже использовался.")
                break

def login(message):
    message_text = (message.text).split()
    if len(message_text) == 2:
        db_sess = db_session.create_session()
        for user in db_sess.query(User).filter(User.login.like(message_text[0])):
            if message_text[0] == user.login and user.password == message_text[1]:
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
            break
        else:
            bot.send_message(message.chat.id, "Неправильный логин")
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода")


def registration(message):
    message_text = (message.text).split()
    if len(message_text) == 3 and message_text[1] == message_text[2]:
        db_sess = db_session.create_session()
        for user in db_sess.query(User).filter(User.login.like(message_text[0])):
            bot.send_message(message.chat.id, "Такой логин уже занят")
        else:
            user = User()
            user.login = message_text[0]
            user.password = message_text[1]
            user.mmr = 0
            db_sess.add(user)
            db_sess.commit()
            bot.send_message(message.chat.id,
                             f"Вы успешно зарегестрировались, ваш \nЛогин: {message_text[0]} \nПароль: {message_text[1]}")
    else:
        bot.send_message(message.chat.id, "Неправильный формат ввода")


bot.polling()
