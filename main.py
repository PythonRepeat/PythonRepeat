import telebot
from telebot import types
import random

bot = telebot.TeleBot(token="8689687377:AAHE7B4HaNZmGxdNYXi1SttfiZdtRHg5ra8")

exercise = []

user_balance = 0


def math_exercise():
    a = random.choice(range(1, 1001))
    b = random.choice(range(1, 1001))
    moves = ['+', '-']
    if a < 11 or b < 11:
        moves.append('*')
    if a % b == 0:
        moves.append('/')
    move = random.choice(moves)
    question = f'{a} {move} {b} = '
    result = ''
    if move == '+':
        result += f'{a + b}'
    elif move == '-':
        result += f'{a - b}'
    elif move == '*':
        result += f'{a * b}'
    else:
        result += f'{a / b}'
    exercise.append(question)
    exercise.append(str(result))
    return exercise


keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True).add(
    types.KeyboardButton(text='Почати гру'),
    types.KeyboardButton(text='Завершити гру'),
    types.KeyboardButton(text='Мій баланс'),
    types.KeyboardButton(text='Магазин')
)

@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,text='Тебе вітає математична гра',
                     reply_markup=keyboard)


@bot.message_handler(content_types=['text'])
def start_game(message):
    if message.text == 'Почати гру':
        bot.send_message(message.chat.id, text=f'Твій баланс {user_balance}грн\n'
                                               f'За кожну правильну відповідь ти отримуєш 50грн,\n'
                                               f'А за неправильну -> -50\n'
                                               f'Перший приклад')
        math_exercise()
        bot.send_message(message.chat.id, text=f'{exercise[0]}')
        bot.register_next_step_handler(message, check_answer)


def check_answer(message):
    global user_balance
    if str(message.text) == exercise[-1]:
        user_balance = user_balance - 50
        bot.send_message(message.chat.id, text='Правильно, ось наступний приклад')
        exercise.clear()
        math_exercise()
        bot.send_message(message.chat.id, text=f'{exercise[0]}')
    else:
        user_balance -= 100
        bot.send_message(message.chat.id, text=f'Не правильна відповідь\n'
                                               f'Правильна відповідь {exercise[-1]}\n'
                                               f'Ось наступний')
        exercise.clear()
        math_exercise()
        bot.send_message(message.chat.id, text=f'{exercise[0]}')
    bot.register_next_step_handler(message, check_answer)









bot.infinity_polling()
