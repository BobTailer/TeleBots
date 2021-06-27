import telebot
import random
import pickle
import requests
from bs4 import BeautifulSoup
import threading


TOKEN = '1855653370:AAGIJf1cj-QYeaS_6z1Ik8K4pFRakRZgI4E'
bot = telebot.TeleBot(TOKEN)

eVALORANT_title_list = []
def eVALORANT():
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

    #Достаю статьи из киберспорта VALORANT
    eVALORANT_news = []
    for i in eVALORANT_link_list:
        page = requests.get('https://rus.egamersworld.com/valorant/news/' + i)
        soup = BeautifulSoup(page.content, 'html.parser')
        elements = str(soup.find_all(class_='content'))
        elements = elements[1:len(elements) - 1]
        res_elements = ''
        while len(elements) > 0:
            if elements[0] == '<':
                elements = elements[elements.find('>') + 1:]
            else:
                res_elements += elements[:elements.find('<')]
                elements = elements[elements.find('<'):]
        eVALORANT_news.append(res_elements)
    #print('tick')
    threading.Timer(120, eVALORANT).start()
    res_list = [eVALORANT_title_list, eVALORANT_link_list, eVALORANT_news]
    return res_list

res_list = eVALORANT()
eVALORANT_title_list = res_list[0]
eVALORANT_link_list = res_list[1]
eVALORANT_news = res_list[2]



#Создаю кючи проверки выбранных тем для каждого пользователя
games_list = ['VALORANT']
game_check_list = []
for i in range(len(games_list)):
    game_check_list.append(False)
game_check_dict = {}

themes_list = ['eSports']
themes_check_list = []
for i in range(len(themes_list)):
    themes_check_list.append(False)
themes_check_dict = {}

#Создаю файл с пользователями для регестрации
users = []
with open('users.pickle', 'rb') as f:
    users = pickle.load(f)

for i in users:
    game_check_dict[i] = []
    for j in game_check_list:
        game_check_dict[i].append(j)

for i in users:
    themes_check_dict[i] = []
    for j in themes_check_list:
        themes_check_dict[i].append(j)

#Команда /start и приветствие
@bot.message_handler(commands=['start'])
def start(message):
    for i in range(len(game_check_dict[message.chat.id])):
        game_check_dict[message.chat.id][i] = False
    for i in range(len(themes_check_dict[message.chat.id])):
        themes_check_dict[message.chat.id][i] = False
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
    bot.send_message(message.chat.id, f"Вы выбрали игру VALORANT.\n"
                                      f"Выберите наиболее интересующую Вас тему:"
                                      f"Киберспорт - /eSports")

#Выибор киберспорта
@bot.message_handler(commands=['eSports'])
def eSports(message):
    if game_check_dict[message.chat.id][0] == True:
        themes_check_dict[message.chat.id][0] = True
        mes = 'Выберите новость из мира киберспорта:\n'
        for i in range(len(eVALORANT_title_list)):
            mes += f'{eVALORANT_title_list[i]} - /{i + 1}\n'
        bot.send_message(message.chat.id, mes)


#Вывожу статью, которую выбрал пользователь
@bot.message_handler(commands=['1'])
def n1(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[0])

@bot.message_handler(commands=['2'])
def n2(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[1])

@bot.message_handler(commands=['3'])
def n3(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[2])

@bot.message_handler(commands=['4'])
def n4(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[3])

@bot.message_handler(commands=['5'])
def n5(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[4])

@bot.message_handler(commands=['6'])
def n6(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[5])

@bot.message_handler(commands=['7'])
def n7(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[6])

@bot.message_handler(commands=['8'])
def n8(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[7])

@bot.message_handler(commands=['9'])
def n9(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[8])

@bot.message_handler(commands=['10'])
def n10(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[9])

#Команда для выхода на стартовое меню
@bot.message_handler(commands=['exit'])
def exit(message):
    for i in range(len(game_check_dict[message.chat.id])):
        game_check_dict[message.chat.id][i] = False
    for i in range(len(themes_check_dict[message.chat.id])):
        themes_check_dict[message.chat.id][i] = False
    userid = message.chat.id
    for i in users:
        if userid == int(i):
            bot.send_message(message.chat.id, f"Выберите игру, по которой я буду отбирать для вас новости:\n"
                                              f"VALORANT - /VALORANT")
            return
    bot.send_message(message.chat.id, f"Добро пожаловать в наш телеграм бот.\n"
                                      f"Тут вы сможете выбрать актуальные новости на нужные вам темы!\n"
                                      f"К сожалению, Вы ещё не зарегестрированы в системе(\n"
                                      f"Для регестрации введите команду - /reg")


if __name__ == '__main__':
    bot.polling()