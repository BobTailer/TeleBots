import telebot
import random
import pickle
import requests
from bs4 import BeautifulSoup

TOKEN = '1855653370:AAGIJf1cj-QYeaS_6z1Ik8K4pFRakRZgI4E'
bot = telebot.TeleBot(TOKEN)

#Достаю заголовки и ссылки статей по киберспорту Valorant
page = requests.get('https://rus.egamersworld.com/valorant/news')
soup = BeautifulSoup(page.content, 'html.parser')
title_list = []
link_list = []
soup = str(soup)
def find_in_soup(st_start_copy, list):
    soup_copy = soup
    while soup_copy.find(st_start_copy) > -1:
        soup_copy = soup_copy[soup_copy.find(st_start_copy) + len(st_start_copy):]
        name = soup_copy[:soup_copy.find('"')]
        list.append(name)
        soup_copy = soup_copy[soup_copy.find('"'):]

find_in_soup(',"title":"', title_list)
find_in_soup('"game_slug":"valorant","slug":"', link_list)
for i in range(2):
    title_list.pop(-1)


#Создаю файл с пользователями для регестрации
users = []
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