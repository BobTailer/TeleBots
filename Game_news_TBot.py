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
eVALORANT_title_list = []
eVALORANT_link_list = []
soup = str(soup)
def find_in_soup(st_start_copy, list):
    soup_copy = soup
    while soup_copy.find(st_start_copy) > -1:
        soup_copy = soup_copy[soup_copy.find(st_start_copy) + len(st_start_copy):]
        name = soup_copy[:soup_copy.find('"')]
        list.append(name)
        soup_copy = soup_copy[soup_copy.find('"'):]

find_in_soup(',"title":"', eVALORANT_title_list)
find_in_soup('"game_slug":"valorant","slug":"', eVALORANT_link_list)
for i in range(2):
    eVALORANT_title_list.pop(-1)


games_list = ['VALORANT']
game_check_list = []
for i in range(len(games_list)):
    game_check_list.append(False)

game_check_dict = {}

#Создаю файл с пользователями для регестрации
users = []
with open('users.pickle', 'rb') as f:
    users = pickle.load(f)
for i in users:
    game_check_dict[i] = []
    for j in game_check_list:
        game_check_dict[i].append(j)
print(game_check_dict)
#Команда /start и приветствие
@bot.message_handler(commands=['start'])
def start(message):
    userid = message.chat.id
    for i in users:
        if userid == int(i):
            bot. send_message(message.chat.id, f"Выберите игру, по которой я буду отбирать для вас новости:\n"
                                               f"VALORANT - /VALORANT")
            return
    bot.send_message(message.chat.id, f"Добро пожаловать в наш телеграм бот.\n"
                                      f"Тут вы сможете выбрать актуальные новости на нужные вам темы!\n"
                                      f"К сожалению, Вы ещё не зарегестрированы в системе(\n"
                                      f"Для регестрации введите команду - /reg")



#РЕГИСТРАЦИЯ
@bot.message_handler(commands=['reg'])
def reg(message):
    userid = message.chat.id
    for i in users:
        if userid == int(i):
            bot.send_message(message.chat.id, "Вы уже зарегестрированы. ")
            return

    users.append(userid)
    bot.send_message(message.chat.id, f"Поздравляю, Вы успешно зарегстрировались в системе!\n" 
                                      f"Выберите игру, по которой я буду отбирать для вас новости:\n"
                                      f"VALORANT - /VALORANT\n")
    with open('users.pickle', 'wb') as f:
        pickle.dump(users, f)

#Команда /VALORANT
@bot.message_handler(commands=['VALORANT'])
def VALORANT(message):
    game_check_dict[message.chat.id][0] = True
    bot.send_message(message.chat.id, f"Статус - {game_check_dict}")

if __name__ == '__main__':
    bot.polling()