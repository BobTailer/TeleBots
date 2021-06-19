import telebot
import random
import pickle

TOKEN = '1855653370:AAGIJf1cj-QYeaS_6z1Ik8K4pFRakRZgI4E'
bot = telebot.TeleBot(TOKEN)


users = []
b = 1

with open('users.pickle', 'rb') as f:
     users = pickle.load(f)

# РЕГИСТРАЦИЯ
@bot.message_handler(commands=['reg'])
def reg(message):
    userid = message.chat.id
    for i in users:
        if userid == int(i):
            bot.send_message(message.chat.id, "Вы уже зарегестрированы")
            return

    users.append(userid)
    bot.send_message(message.chat.id, f'Ваш ID - {userid}')
    with open('users.pickle', 'wb') as f:
        pickle.dump(users, f)

#print(users)

if __name__ == '__main__':
    bot.polling()
