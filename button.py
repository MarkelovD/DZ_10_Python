import telebot
from telebot import types
import datetime

bot = telebot.TeleBot("token") # токен бота

typeNums = 0

@bot.message_handler(commands=["start"])
def calc(message):
    mrk = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key1 = types.KeyboardButton('Рациональные')
    key2 = types.KeyboardButton('Комплексные')
    mrk.add(key1, key2)
    bot.send_message(message.chat.id, f'Калькулятор \nСделайте выбор, с какими числами работать', reply_markup=mrk)
@bot.message_handler(content_types=['text'])
def buttons(message):
    global typeNums
    a = types.ReplyKeyboardRemove()
    if message.text == 'Рациональные':
        bot.send_message(message.chat.id, f'Выбран режим рациональных чисел', reply_markup=a)
        bot.send_message(message.chat.id, f'Введите выражение без пробелов')
        bot.register_next_step_handler(message, controller)
        typeNums = 0
    elif message.text == 'Комплексные':
        bot.send_message(message.chat.id, f'Выбран режим комплексных чисел', reply_markup=a)
        bot.send_message(message.chat.id, f'Введите выражение без пробелов')
        bot.register_next_step_handler(message, controller.controller)
        typeNums = 1


def controller(message):
    collection = ["+","-","*","/","%"]
    vir = message.text
    write_log(message)
    for i in vir:
        if "//" in vir:
            razd = "//"
        elif i in collection:
            razd = i
    line = message.text.split(razd)
    znak = razd
    if typeNums == 0:
        a = int(line[0])
        b = int(line[1])
    else:
        a = complex(line[0])
        b = complex(line[1])

    if znak == '+':
        res = summ_nums(a, b)
    elif znak == '-':
        res = sub_nums(a, b)
    elif znak == '*':
        res = mult_nums(a, b)
    elif znak == '/':
        res = div_nums(a, b)
    elif typeNums == 1 and (znak == '//' or znak == '%'):
        bot.send_message(message.chat.id, f'Неверный ввод, повторите')
        write_log(message)
        bot.register_next_step_handler(message, controller)
        return
    elif znak == '//':
        res = div_int(a, b)
    elif znak == '%':
        res = div_rem(a, b)
    bot.send_message(message.chat.id, str(res))
    calc(message)

def summ_nums(a, b):
    return a + b


def sub_nums(a, b):
    return a - b


def mult_nums(a, b):
    return a * b


def div_nums(a, b):
    return a / b

def div_int(a, b):
    return a // b


def div_rem(a, b):
    return a % b

def write_log(message):
    file = open("log.txt", "a+",encoding="utf-8" )
    file.write(f"| Name: {message.from_user.first_name} | Last_name: {message.from_user.last_name} | time: {datetime.datetime.now()} | message: {message.text} |\n")
    file.close()
bot.infinity_polling()
