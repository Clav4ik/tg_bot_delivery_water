# This is a sample Python script.

#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys

import telebot
from telebot import types
from telebot import apihelper
from Checkers import isvalid_phone_number, isvalid_order, isvalid_address, isvalid_count
from models import User, Address, Phone_Number, Black_List, Token_Unblock

#CHAT_OUTPUT = -1002141829518
CHAT_OUTPUT = -4125418031
ADMIN_GROUP_ID = -4192581904
ADMIN_ID = [1333538265, 1006078469, 775207817]
apihelper.ENABLE_MIDDLEWARE = True

bot = telebot.TeleBot("")
#775207817

#questions another
#картинка на лого
#картинка на wlcome msg первое стартовое
#текст на первое стартовое welcome msg сам
#как будет ссылка на бота выглядеть
#
#
@bot.middleware_handler(update_types=['message'])
def modify_message(bot_instance, message):
    if not message.text:
        return stock(message)
    # modifying the message before it reaches any other handler
    user_tg_id = Black_List.select().where(Black_List.user_tg_id == str(message.from_user.id.numerator))
    if user_tg_id:
        if message.chat.id == ADMIN_GROUP_ID or message.chat.id == CHAT_OUTPUT:
            return stock(message)

        bot.clear_step_handler(message)
        #bot.clear_step_handler_by_chat_id(message.chat.id)
        msg = message.text.strip()
        if  msg[0:7] == "unblock":
            key = msg.split("\n")
            if  len(key) == 2:
                return unblock(message, key[1].strip())

        bot.delete_message(message.chat.id, message.id)
        bot.send_message(message.chat.id, "Ви заблоковані", reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, "Для розблокування зв'яжитесь з менеджером\n0557777888")
        bot.register_next_step_handler(message, stock)

def stock(message):
    pass
def stock_to_fast_reg(message):
    if message.text == None:
        return stock(message)
    msg = message.text.strip()
    if msg == "/start" or msg == "/stock":
        return stock(message)
    bot.register_next_step_handler(message, send_welcome)

def unblock(message, key):
    if key:
        token = Token_Unblock.get(Token_Unblock.token == key)
        if token and token.used == False:
            try:
                record = Black_List.get(Black_List.user_tg_id == str(message.from_user.id.numerator))
                token.used = True
                token.save()
                record.delete_instance()
            except Exception as e:
                print(e)

@bot.message_handler(commands=['bred'])
def test(message):
    bot.send_message(message.chat.id, "Чтобы у тебя всё сложилось в жизни, нужно хорошо учиться")
@bot.message_handler(commands=['send_msg_id'])
def msg_id_all(message):
    bot.send_message(message.chat.id, "your id = " + str(message.from_user.id.numerator))
    bot.send_message(message.chat.id, "id group = "+str(message.chat.id))
@bot.message_handler(commands=['stock'])
def helper_out_msg_branch(message):
    return stock(message)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    #work info all realese
    if message == None:
        return stock(message)
    with open("FirstPictureInfo.jpeg", "rb") as file:
        bot.send_photo(message.chat.id, photo=file.read())

    pin_msg = bot.send_message(message.chat.id, '0973477073 - номер Романа'
                                                '\n0669450677 - підтримка(програміст, якщо щось працює не так)')

    try:
        bot.unpin_all_chat_messages(chat_id=message.chat.id)
    except:
        pass
    bot.pin_chat_message(chat_id=message.chat.id, message_id=pin_msg.message_id)
    print(dir(bot))
    print(dir(message.from_user))
    print(dir(message.chat))
    print("Chat id =="+str(message.chat.id))

    #тоже релиз но потом
    text = "Текст текст много о воде Текст текст много о воде Текст текст много о воде" \
           "Текст текст много о воде Текст текст много о воде Текст текст много о воде" \
           "Текст текст много о воде Текст текст много о воде Текст текст много о воде"
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    bcBtn = types.KeyboardButton('🏢бізнес центр')
    cBtn = types.KeyboardButton("☕кав'ярня")
    othersBtn = types.KeyboardButton('Інше')


    markup.add(bcBtn, cBtn, othersBtn)
    bot.send_message(message.chat.id, "Welcome msg", reply_markup=markup)
    bot.register_next_step_handler(message, fast_reg)


def fast_reg(message):
    if not User.select().where(User.user_tg_id == str(message.from_user.id.numerator)):
        User.create(
            user_tg_id=str(message.from_user.id.numerator)
        )
#Скопіюйте шаблон та введіть свої дані обов'язково з нового рядка та двокрапкою
    bot.send_message(message.chat.id, "Скопіюйте шаблон та введіть свої дані обов'язково з нового рядка та двокрапкою. \nШаблон")
    context = {}
    if message.text == "☕кав'ярня":
        context.update({"object": "К"})
        bot.send_message(message.chat.id, "Телефон: 0661116699\nНазва: Аврора\nВулиця: Академіка Комарова"
                                          "\nДім: 62а\nКількість: 3",
                         reply_markup=types.ReplyKeyboardRemove())

        # bot.send_message(message.chat.id,
        #                  "Будь ласка, як у прикладі з нового рядка значення \nі обов'язково=> : <=щоб було двокрапка",
        #                  reply_markup=types.ReplyKeyboardRemove())

    elif message.text == '🏢бізнес центр':
        context.update({"object": "БЦ"})
        bot.send_message(message.chat.id, "Телефон: 0661116699\nНазва: Аврора \nВулиця: Академіка Комарова"
                                          "\nДім: 62а \n№Офіса: 6н\nКількість: 3",
                         reply_markup=types.ReplyKeyboardRemove())


        # bot.send_message(message.chat.id, "Телефон: \n Название: \n Количество: \n Улица: \n Дом: \n №Офиса: ")

    elif message.text == 'Інше':
        context.update({"object": "other"})
        bot.send_message(message.chat.id, "Телефон: 0661116699\nНазва: Аврора \nВулиця: Академіка Комарова"
                                          "\nДім: 62а \nКількість: 3",
                         reply_markup=types.ReplyKeyboardRemove())

    else:
        bot.reply_to(message, "Спробуйте ще")
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.send_message(message.chat.id, "Переходимо до початку", reply_markup=markup)
        return stock_to_fast_reg(message)

    bot.register_next_step_handler(message, test_coplete_order, context)


def test_coplete_order(message, context):
    msg = message.text.strip()


    if not isvalid_order(msg, context.get("object")):
        bot.send_message(message.chat.id, "Заявка не відповідає шаблону")
        bot.send_message(message.chat.id, "Переходимо до початку")
        return send_welcome(message)

    context.update({"full_ticket": msg})
    arr_values = msg.split("\n")

    if not isvalid_phone_number(str(arr_values[0].split(":")[1]).strip()):
        bot.reply_to(message, "Номер не відповідає формату\n0661116699")
        bot.send_message(message.chat.id,
                         "Скопіюйте Ваше повідомлення та введіть вірний телефоний номер\nВаше попереднє повідомлення",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, context.get("full_ticket"))
        return step_invalid_phone_number(message, context)
    if not isvalid_count(str(arr_values[-1].split(":")[1]).strip()):
        bot.reply_to(message, "Помилку у числі кількості")
        bot.send_message(message.chat.id,
                         "Скопіюйте Ваше повідомлення та введіть вірну кількість бутлів\nВаше попереднє повідомлення",
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_message(message.chat.id, context.get("full_ticket"))
        return step_invalid_count(message, context)

    context.update({"phone_number":str(arr_values[0].split(":")[1]).strip()})

    sub_name = str(arr_values[1].split(":")[1]).strip()
    sub_street = str(arr_values[2].split(":")[1]).strip()
    sub_house_num = str(arr_values[3].split(":")[1]).strip()

    if not (sub_name and sub_street and sub_house_num):
        bot.reply_to(message, "В заявці є порожні поля")
        bot.send_message(message.chat.id, "Переходимо до початку")
        return send_welcome(message)

    context.update({"name" :sub_name})
    context.update({"street":sub_street} )
    context.update({"house_num" :sub_house_num})

    if context.get("object") == "БЦ":
        sub_office_num = str(arr_values[4].split(":")[1]).strip()
        if not sub_office_num:
            bot.reply_to(message, "В заявці порожнє необхідне поле №офису")
            bot.send_message(message.chat.id,
                             "Скопіюйте Ваше повідомлення та введіть вірний №офису\nВаше попереднє повідомлення",
                             reply_markup=types.ReplyKeyboardRemove())

            bot.send_message(message.chat.id, context.get("full_ticket"))
            return step_invalid_office_num(message, context)

        context.update({"office_num": sub_office_num})


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cBtn = types.KeyboardButton('Підтвердити заявку\n(на завтра)')
    chBtn = types.KeyboardButton('Змінити заявку')
    fBtn = types.KeyboardButton('🔥Термінове замовлення🔥\n(на сьогодні)')
    rBtn = types.KeyboardButton('Перейти до початку')
    markup.add(cBtn, chBtn, fBtn ,rBtn)

    bot.send_message(message.chat.id, "Оберіть дію", reply_markup=markup)
    bot.register_next_step_handler(message, coplete_order, context)


def coplete_order(message, context):

    msg = message.text.strip()


    if msg == "Підтвердити заявку\n(на завтра)" or  msg == "🔥Термінове замовлення🔥\n(на сьогодні)":
        user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
        if not Phone_Number.select().where(Phone_Number.phone_number == context.get("phone_number") and Phone_Number.user_id == user):
            Phone_Number.create(
                phone_number=context.get("phone_number"),
                user=user
            )
        Address.create(
            object=context.get("object"),
            name=context.get("name"),
            street=context.get("street"),
            house_num=context.get("house_num"),
            office_num=context.get("office_num"),
            user=user
        )
        message_to_group = "user_tg_id = " + str(message.from_user.id.numerator)+\
                           "\nЗаказ \n" + context.get("full_ticket")
        message_user = "Заказ відправлено"

        if msg == "🔥Термінове замовлення🔥\n(на сьогодні)":
            message_to_group += "\n🔥🔥🔥"
            message_user = "Термінове замовлення відправлено"
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)

        bot.send_message(message.chat.id, message_user, reply_markup=markup)
        bot.send_message(CHAT_OUTPUT, message_to_group)
        bot.send_message(message.chat.id, "Дякуємо, що обрали нас")
    elif msg == "Змінити заявку":
        bot.send_message(message.chat.id,
                         "Добре, скопіюте попереднє повідомлення і введіть коректні значення.\nПопереднє повідомлення")
        bot.send_message(message.chat.id, context.get("full_ticket"), reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, test_coplete_order, context)

    elif msg == 'Перейти до початку':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.send_message(message.chat.id, "Переходимо до початку", reply_markup=markup)
        return stock_to_fast_reg(message)
    else:
        bot.reply_to(message, "Спробуйте ще")
        return send_welcome(message)

def step_invalid_phone_number(message, context):
    bot.register_next_step_handler(message,test_coplete_order, context)
def step_invalid_count(message, context):
    bot.register_next_step_handler(message, test_coplete_order, context)
def step_invalid_office_num(message, context):
    bot.register_next_step_handler(message, test_coplete_order, context)

@bot.message_handler(content_types=['text'])
def start_order(message):
    if message == None or message.chat.id == CHAT_OUTPUT:
        return stock(message)

    if message.text.strip()=="/admen" and message.chat.id == ADMIN_GROUP_ID:
        return admin_panel(message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    start_order = types.KeyboardButton('Сформувати заявку')
    markup.add(start_order)
    bot.send_message(message.chat.id, "Початок", reply_markup=markup)
    bot.register_next_step_handler(message, ask_phone_number)

def ask_phone_number(message):

    if message.chat.id == ADMIN_GROUP_ID or message.chat.id == CHAT_OUTPUT or message.text.strip() != 'Сформувати заявку':
        return stock(message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    user = User.select().where(User.user_tg_id == str(message.from_user.id.numerator))
    if not user:
        User.create(
            user_tg_id=str(message.from_user.id.numerator)
        )
    phone_numbers = Phone_Number.select().where(Phone_Number.user == user)

    for number in phone_numbers:
        Btn = types.KeyboardButton(number.phone_number)
        markup.add(Btn)

    crudBtn = types.KeyboardButton('Номер телефону (Додати, змінити, видалити)')
    lBtn = types.KeyboardButton('Перейти до початку')
    markup.add(crudBtn, lBtn)
    bot.send_message(message.chat.id, "Оберіть контактний номер телефону", reply_markup=markup)
    if not phone_numbers:
        bot.send_message(message.chat.id, "Порожній список номерів телефону.\nБудь ласка, додайте номер телефону")

    bot.register_next_step_handler(message, ask_address)

def ask_address(message):
    msg = message.text.strip()

    if msg == 'Номер телефону (Додати, змінити, видалити)':
        return choiseCrudPhoneNumber(message)
    if msg == 'Перейти до початку':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.send_message(message.chat.id, "Переходимо до початку", reply_markup=markup)
        return stock(message)

    if not isvalid_phone_number(msg):
        bot.send_message(message.chat.id, "Невірно ведений номер")
        return start_order(message)


    field_ticket = {
        "phone_number" : msg,
        "full_address": "",
        "count": ""
    }

    #msg = bot.reply_to(message, 'How old are you?', reply_markup=markup)

    context ={}
    context.update(field_ticket)
    print(context)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

    user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
    addresses = Address.select().where(Address.user == user)

    context.update({"dict_user_addresses":{}})
    for addresse in addresses:
        full_string=''
        if addresse.object =="БЦ":
            full_string+= addresse.object +" "+ addresse.name +" №оф. "+addresse.office_num+" вул. "+addresse.street+\
                          " "+addresse.house_num
        elif addresse.object =="К":
            full_string += "☕" + " " + addresse.name +" вул. " + addresse.street + " " + addresse.house_num
        elif addresse.object =='other' or addresse.object == None:
            full_string += addresse.name + " вул. " + addresse.street + " " + addresse.house_num
        context.get("dict_user_addresses").update({addresse.id: full_string})
        Btn = types.KeyboardButton(full_string)
        markup.add(Btn)

    crudBtn = types.KeyboardButton('Адреса (Додати, змінити, видалити)')
    markup.add(crudBtn)
    bot.send_message(message.chat.id, "Оберіть Вашу адресу або додайте її до свого списку", reply_markup=markup)

    if not addresses:
        bot.send_message(message.chat.id, "Порожній список адреси.\nБудь ласка, додайте адресу")

    bot.register_next_step_handler(message, ask_count, context)

def ask_count(message, context):
    if message.text.strip() == None:
        return stock(message)

    msg = message.text.strip()
    if not context.get("full_address"):
        context["full_address"] = message.text.strip()

    if msg=='Адреса (Додати, змінити, видалити)':
        return choiseCrudAddress(message)

    if context.get("dict_user_addresses"):
        if not msg in context.get("dict_user_addresses").values():
            bot.send_message(message.chat.id, "Ви не обрали адресу зі списку")
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
            Btn = types.KeyboardButton('Ок')
            markup.add(Btn)
            bot.reply_to(message, "Спробуйте ще", reply_markup=markup)
            return stock(message)

        pk = int(list(context.get("dict_user_addresses").keys())[list(context.get("dict_user_addresses").values()).index(msg)])
        context.update({"pk":pk})

        context.pop('dict_user_addresses')


    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    one = types.KeyboardButton('1')
    two = types.KeyboardButton('2')
    three = types.KeyboardButton('3')
    four = types.KeyboardButton('4')
    five = types.KeyboardButton('5')
    six = types.KeyboardButton('6')
    markup.add(one, two, three, four, five, six)
    bot.send_message(message.chat.id, "Яка кількість? \n"
                                      "Оберіть або впишіть число. Наприклад,\n"
                                      "10",reply_markup=markup)
    print("last before order context")

    bot.register_next_step_handler(message, check_order, context)


def check_order(message, context):
    msg = message.text.strip()
    print(context.get("object"))
    if not isvalid_count(msg):
        bot.reply_to(message, "Не схоже на ціле додатне число")
        return ask_count(message, context)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cBtn = types.KeyboardButton('Підтвердити заявку\n(на завтра)')
    chBtn = types.KeyboardButton('Змінити кількість бутлів')
    fBtn = types.KeyboardButton('🔥Термінове замовлення🔥\n(на сьогодні)')
    rBtn = types.KeyboardButton('Перейти до початку')
    markup.add(cBtn, chBtn, fBtn, rBtn)

    bot.send_message(message.chat.id, "Оберіть дію", reply_markup=markup)

    typ=""
    address = Address.get(Address.id == context.get("pk"))
    if address.object == "БЦ":
        typ = "БЦ"
    elif address.object == "К":
        typ = "☕"
    elif address.object == "other":
        pass
    text_order = "Заявка: \nТелефон: "+context.get("phone_number")+"\nНазва: "+typ+" "+address.name+\
                 "\nВулиця: "+address.street+"\nДім: "+address.house_num

    if context.get("office_num"):
        text_order+= "\n№Офіса: "+address.office_num

    text_order+= "\nКількість: "+msg

    bot.send_message(message.chat.id, text_order,reply_markup=markup)

    context.update({"text":text_order})
    bot.register_next_step_handler(message, complite, context)

def complite(message, context):
    msg = message.text.strip()
    if msg == "Підтвердити заявку\n(на завтра)" or msg == "🔥Термінове замовлення🔥\n(на сьогодні)":
        message_to_group = "user_tg_id = " + str(message.from_user.id.numerator) + "\n" + context.get("text")
        message_user = "Заказ відправлено"

        if msg == '🔥Термінове замовлення🔥\n(на сьогодні)':
            message_to_group += "\n 🔥🔥🔥"
            message_user = "Термінове замовлення відправлено"
        bot.send_message(CHAT_OUTPUT, message_to_group)
        # bot.forward_message(CHAT_OUTPUT, message.chat.id, message.message_id)

        bot.send_message(message.chat.id, message_user)
        bot.send_message(message.chat.id, "Дякуємо, що обрали нас")
        return start_order(message)
    elif msg == 'Змінити кількість бутлів':
        return ask_count(message, context)
    elif msg == 'Перейти до початку':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.send_message(message.chat.id, "Переходимо до початку", reply_markup=markup)
        return stock(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.reply_to(message, "Спробуйте ще", reply_markup=markup)



#CRUD or CRUDs  all

def choiseCrudPhoneNumber(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cBtn = types.KeyboardButton('Додати новий номер')
    uBtn = types.KeyboardButton('Змінити номер')
    dBtn = types.KeyboardButton('Видалити номер')
    lBtn = types.KeyboardButton('Перейти до початку')
    markup.add(cBtn, uBtn, dBtn, lBtn)
    bot.send_message(message.chat.id, "Оберіть дію", reply_markup=markup)
    bot.register_next_step_handler(message, crudPhoneNumber)

def crudPhoneNumber(message):
    msg = message.text.strip()

    if msg == 'Додати новий номер':
        bot.send_message(message.chat.id, "Введіть додатковий номер телефону у форматі. \nНаприклад")
        bot.send_message(message.chat.id, "0661116699", reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, createPhoneNumber)
    elif msg == 'Змінити номер':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
        phone_numbers = Phone_Number.select().where(Phone_Number.user == user)

        for number in phone_numbers:
            Btn = types.KeyboardButton(number.phone_number)
            markup.add(Btn)
        bot.send_message(message.chat.id, "Оберіть номер для заміни", reply_markup=markup)
        bot.register_next_step_handler(message, updatePhoneNumber)
    elif msg == 'Видалити номер':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        rBtn = types.KeyboardButton('Перейти до початку')
        markup.add(rBtn)

        user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
        phone_numbers = Phone_Number.select().where(Phone_Number.user == user)


        for number in phone_numbers:
            Btn = types.KeyboardButton(number.phone_number)
            markup.add(Btn)

        bot.send_message(message.chat.id, "Оберіть номер на видалення", reply_markup=markup)
        bot.register_next_step_handler(message, deletePhoneNumber)
    elif msg == 'Перейти до початку':
        return start_order(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.reply_to(message, "Спробуйте ще", reply_markup=markup)

def createPhoneNumber(message):
    msg = message.text.strip()

    if not isvalid_phone_number(msg):
        bot.send_message(message.chat.id, "Невірно ведений номер")
        return start_order(message)

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Btn = types.KeyboardButton("Ок")
    markup.add(Btn)

    user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
    if not Phone_Number.select().where(Phone_Number.user_id == user.id).where(Phone_Number.phone_number == msg):
        Phone_Number.create(
            phone_number=msg,
            user=user
        )
        bot.send_message(message.chat.id, "Додався новий номер", reply_markup=markup)
    else:
        bot.send_message(message.chat.id, "Цей номер вже існує у Вас", reply_markup=markup)

def updatePhoneNumber(message):
    choise_num = message.text
    bot.send_message(message.chat.id, "Ведіть на який номер Ви змінюєте", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, updatePhoneNumberComplite, choise_num)

def updatePhoneNumberComplite(message, choise_num):
    msg = message.text.strip()
    if not isvalid_phone_number(msg):
        bot.send_message(message.chat.id, "Невірно ведений номер")
        return start_order(message)

    user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
    phone_number = Phone_Number.get(Phone_Number.user == user).get(Phone_Number.phone_number == choise_num)
    phone_number.phone_number = msg
    phone_number.save()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Btn = types.KeyboardButton("Ок")
    markup.add(Btn)
    bot.send_message(message.chat.id, f"Номер {msg}\nЗмінено ", reply_markup=markup)

def deletePhoneNumber(message):
    msg = message.text
    if msg == 'Перейти до початку':
        return start_order(message)
    user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
    try:
        phone_number = Phone_Number.get(Phone_Number.user == user).get(Phone_Number.phone_number == msg)
        phone_number.delete_instance()
    except:
        pass
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Btn = types.KeyboardButton("Ок")
    markup.add(Btn)
    bot.send_message(message.chat.id, f"Номер {message.text.strip()}\nВидалено ", reply_markup=markup)

#CRUD address

def choiseCrudAddress(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    cBtn = types.KeyboardButton('Додати нову адресу')
    uBtn = types.KeyboardButton('Змінити частину адреси (вулицю, №будинку та інше)')
    dBtn = types.KeyboardButton('Видалити адресу')
    lBtn = types.KeyboardButton('Перейти до початку')

    markup.add(cBtn, uBtn, dBtn, lBtn)
    bot.send_message(message.chat.id, "Оберіть дію", reply_markup=markup)
    bot.register_next_step_handler(message, crudAddress)

def crudAddress(message):
    msg = message.text.strip()

    if msg == 'Додати нову адресу':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
        bcBtn = types.KeyboardButton('🏢бізнес центр')
        cBtn = types.KeyboardButton("☕кав'ярня")
        othersBtn = types.KeyboardButton('Інше')

        markup.add(bcBtn, cBtn, othersBtn)
        bot.send_message(message.chat.id, "Оберіть тип об'єкту", reply_markup=markup)

        bot.register_next_step_handler(message, createAddress)
    elif msg == 'Змінити частину адреси (вулицю, №будинку та інше)':
        # ||  частину на кнопках
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

        user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
        addresses = Address.select().where(Address.user == user)

        context = {}

        for addresse in addresses:
            full_string = ''
            if addresse.object == "БЦ":
                full_string += addresse.object + " " + addresse.name + " №оф. " + addresse.office_num + " вул. " + addresse.street + " " + addresse.house_num
            elif addresse.object == "К":
                full_string += "☕" + " " + addresse.name + " вул. " + addresse.street + " " + addresse.house_num
            elif addresse.object == 'other':
                full_string += addresse.name + " вул. " + addresse.street + " " + addresse.house_num
            context.update({addresse.id: full_string})
            Btn = types.KeyboardButton(full_string)
            markup.add(Btn)
        bot.send_message(message.chat.id, "Оберіть адресу для заміни частини", reply_markup=markup)
        bot.register_next_step_handler(message, updateAddress, context)
    elif msg == 'Видалити адресу':

        user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
        addresses = Address.select().where(Address.user == user)

        context = {}

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        lBtn = types.KeyboardButton('Перейти до початку')
        markup.add(lBtn)
        for addresse in addresses:
            full_string = ''
            if addresse.object == "БЦ":
                full_string += addresse.object + " " + addresse.name + " №оф." + addresse.office_num + " вул. " + addresse.street + " " + addresse.house_num
            elif addresse.object == "К":
                full_string += "☕" + " " + addresse.name + " вул. " + addresse.street + " " + addresse.house_num
            elif addresse.object == 'other':
                full_string += addresse.name + " вул. " + addresse.street + " " + addresse.house_num
            context.update({addresse.id:full_string})
            Btn = types.KeyboardButton(full_string)
            markup.add(Btn)
        bot.send_message(message.chat.id, "Оберіть адресу на видалення", reply_markup=markup)
        bot.register_next_step_handler(message, deleteAddress, context)
    elif msg == 'Перейти до початку':

        return start_order(message)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.reply_to(message, "Спробуйте ще", reply_markup=markup)

def createAddress(message):
    bot.send_message(message.chat.id, "Скопіюйте шаблон та введіть свої дані обов'язково з нового рядка та двокрапкою. \nШаблон")
    context = {}
    if message.text.strip() == "☕кав'ярня":
        context.update({"object": "К"})

        bot.send_message(message.chat.id, "Назва: Аврора\nВулиця: Академіка Комарова"
                                          "\nДім: 62а")

    elif message.text.strip() == '🏢бізнес центр':
        context.update({"object": "БЦ"})
        bot.send_message(message.chat.id, "Назва: Аврора \nВулиця: Академіка Комарова"
                                          "\nДім: 62а \n№Офіса: 6н")

    elif message.text.strip() == 'Інше':
        context.update({"object": "other"})
        bot.send_message(message.chat.id, "Назва: Аврора\nВулиця: Академіка Комарова"
                                          "\nДім: 62а")

    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        Btn = types.KeyboardButton('Ок')
        markup.add(Btn)
        bot.reply_to(message, "Спробуйте ще", reply_markup=markup)
        return choiseCrudAddress(message)

    bot.register_next_step_handler(message, copletecreateAddress, context)

def copletecreateAddress(message, context):
    msg = message.text.strip()

    if not isvalid_address(msg, context.get("object")):
        bot.send_message(message.chat.id, "Невірно ведена адреса")
        bot.send_message(message.chat.id, "Скопіюйте повідомлення та введіть свої дані для коректного введення адреси")
        return choiseCrudAddress(message)
    #need valid
    arr_values = msg.split("\n")


    sub_address_name = str(arr_values[0].split(":")[1]).strip()
    sub_address_street = str(arr_values[1].split(":")[1]).strip()
    sub_address_house_num = str(arr_values[2].split(":")[1]).strip()

    if not (sub_address_name and sub_address_street and sub_address_house_num):
        bot.reply_to(message, "В заявці є порожні поля")
        return choiseCrudAddress(message)
    if context.get("object") == "БЦ":
        sub_office_num =str(arr_values[3].split(":")[1]).strip()
        if not sub_office_num:
            bot.reply_to(message, "В заявці порожнє необхідне поле №офису")
            return choiseCrudAddress(message)
        context.update({"office_num": sub_office_num})

    user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
    Address.create(
        object=context.get("object"),
        name=sub_address_name.strip(),
        street=sub_address_street.strip(),
        house_num=sub_address_house_num.strip(),
        office_num=context.get("office_num"),
        user=user
    )
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    rBtn = types.KeyboardButton('Перейти до початку')
    markup.add(rBtn)
    bot.send_message(message.chat.id, "Адреса додана", reply_markup=markup)

def updateAddress(message, context):
    msg = message.text.strip()
    if not msg in context.values():
        bot.send_message(message.chat.id, "Ви не обрали адресу зі списку")
        return choiseCrudAddress(message)

    user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
    address = Address.get(Address.user == user) \
        .get(Address.id == int(list(context.keys())[list(context.values()).index(msg)]))
    context.update({"pk":address.id})

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    bcBtn = types.KeyboardButton('🏢бізнес центр')
    cBtn = types.KeyboardButton("☕кав'ярня")
    othersBtn = types.KeyboardButton('Інше')

    markup.add(bcBtn, cBtn, othersBtn)
    bot.send_message(message.chat.id, "Оберіть тип об'єкту", reply_markup=markup)
    bot.register_next_step_handler(message, stepupdateAddress, context)

def stepupdateAddress(message, context):

    address = Address.get(Address.id == context.get("pk"))

    bot.send_message(message.chat.id, "Скопіюйте повідомлення та введіть коректні дані. Обов'язково з нового рядка та двокрапкою")
    msg = message.text.strip()
    if msg == "🏢бізнес центр":
        #context.get(context.get("pk"))
        context.update({"object":"БЦ"})
        bot.send_message(message.chat.id, f"Назва: {address.name} \nВулиця: {address.street}"
                                          f"\nДім: {address.house_num} \n№Офіса: {address.office_num}",
                     reply_markup=types.ReplyKeyboardRemove())

    elif msg == "☕кав'ярня":
        bot.send_message(message.chat.id, f"Назва: {address.name} \nВулиця: {address.street}"
                                          f"\nДім: {address.house_num}",
                     reply_markup=types.ReplyKeyboardRemove())
        context.update({"object": "К"})
        # bot.send_message(message.chat.id, "Телефон: \n Название: \n Количество: \n Улица: \n Дом: \n №Офиса: ")
    elif msg == "Інше":
        bot.send_message(message.chat.id, f"Назва: {address.name} \nВулиця: {address.street}"
                                          f"\nДім: {address.house_num}",
                     reply_markup=types.ReplyKeyboardRemove())
        context.update({"object": "other"})
    else:
        bot.reply_to(message, "Спробуйте ще")
        return choiseCrudAddress(message)

    bot.register_next_step_handler(message, compliteupdateAddress, context)

def compliteupdateAddress(message, context):
    msg = message.text.strip()

    if not isvalid_address(msg, context.get("object")):
        bot.send_message(message.chat.id, "Невірно ведена адреса")
        return choiseCrudAddress(message)

    address = Address.get(Address.id == context.get("pk"))


    arr_values = msg.split("\n")
    sub_address_name = str(arr_values[0].split(":")[1]).strip()
    sub_address_street = str(arr_values[1].split(":")[1]).strip()
    sub_address_house = str(arr_values[2].split(":")[1]).strip()
    if context.get("object") == "БЦ":
        context.update({"office_num": str(arr_values[3].split(":")[1]).strip()})

    address.object=context.get("object")
    address.name=sub_address_name.strip()
    address.street=sub_address_street.strip()
    address.house_num=sub_address_house.strip()
    address.office_num=context.get("office_num")
    address.save()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Btn = types.KeyboardButton('Оk')
    markup.add(Btn)
    bot.send_message(message.chat.id, "Запис змінений", reply_markup=markup)

def deleteAddress(message, context):
    if message.text.strip() == 'Перейти до початку':
        return start_order(message)

    user = User.get(User.user_tg_id == str(message.from_user.id.numerator))
    address = Address.get(Address.user == user)\
        .get(Address.id == int(list(context.keys())[list(context.values()).index(message.text)]))
    address.delete_instance()

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Btn = types.KeyboardButton("Ок")
    markup.add(Btn)
    bot.send_message(message.chat.id, f"Адреса {message.text.strip()}\nВидалено ", reply_markup=markup)

#admin
def admin_panel(message):

    #bot.clear_step_handler(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    Btn = types.KeyboardButton('Додати у Black List')
    Btnt = types.KeyboardButton('Сгенерувати одноразовий токен')
    markup.add(Btn, Btnt)
    bot.send_message(ADMIN_GROUP_ID, 'Оберіть дію', reply_markup=markup)
    bot.register_next_step_handler(message, choise_admin_action)

def choise_admin_action(message):
    msg = message.text.strip()
    if msg == 'Додати у Black List':
        bot.send_message(ADMIN_GROUP_ID, 'Введіть telegram id користувача для відправки його у Black List.\nШаблон')
        bot.send_message(ADMIN_GROUP_ID, '/admen 463153156', reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, to_ban_acc)

    elif msg == 'Сгенерувати одноразовий токен':
        from get_token import get_unblock_token
        token = get_unblock_token()
        if not Token_Unblock.select().where(Token_Unblock.token == token):
            Token_Unblock.create(token = token)
            bot.send_message(ADMIN_GROUP_ID, "unblock \n"+token)
        else:
            token = get_unblock_token()
            if not Token_Unblock.select().where(Token_Unblock.token == token):
                Token_Unblock.create(token=token)
                bot.send_message(ADMIN_GROUP_ID, "unblock \n" + token)
        bot.send_message(ADMIN_GROUP_ID, "Вот это копируй и отдай правопорушнику")
        return  stock(message)


def to_ban_acc(message):
    bot.send_message(ADMIN_GROUP_ID, "last step block")
    msg = message.text.strip()
    user_id_to_ban = msg.split(" ")[1].strip()
    if not Black_List.select().where(Black_List.user_tg_id == user_id_to_ban):
        if int(user_id_to_ban) in ADMIN_ID:
            bot.send_message(ADMIN_GROUP_ID, "Это свои")
            return stock(message)
        Black_List.create(user_tg_id = user_id_to_ban)
        bot.send_message(ADMIN_GROUP_ID, user_id_to_ban+"\nДодан у Black List")


if __name__ == "__main__":
    # bot.enable_save_next_step_handlers(delay=2)
    # bot.load_next_step_handlers()
    bot.infinity_polling()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
