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
    threading.Timer(1800, eVALORANT).start()
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

#список репортов
report_list = []
with open('report.pickle', 'rb') as f:
    report_list = pickle.load(f)

#Команда /help
@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Приветствую Вас в нашем боте.\n'
                                      f'В этом буте, буквально за пару кликов, Вы сможете узнать последние игровые новости, кторые вам интересны!\n'
                                      f'Похоже Вы не знаете как пользоваться этим ботом. Позвольте я Вам всё разложу пополочкам) Вот список команд, которые поддерживает наш бот:\n'
                                      f'/start - Главное меню. Тут Вы выбираете интересующую Вас игру, по которой Вы хотите узнать новости.\n'
                                      f'/eSport - Данная команда будет доступна после выбора игры из команды /start. Она вам предложит список новостей. Рядом с новостью Вы увидете ее номер. Нажмите на него и получите желаемую статью.\n'
                                      f'/report - Используте данную команду для отправки жалоб на баги и оштибки, с которыми Вы столкнулись. Отправлять жалобу через пробел в том же сообщении, где и вызываете эту команду.\n'
                                      f'Если остались ещё вопросы или предложения, то напишите моему создателю. Получить его контакты можно с помощью команды /contacts\n'
                                      f'Желаю Вам приятного пользования. Надеюсь теперь Вам будет легче и проще пользоваться ботом)')

#Команда /report
@bot.message_handler(commands=['report'])
def report(message):
    message_text = message.text
    report_list.append(message_text)
    with open('report.pickle', 'wb') as f:
        pickle.dump(report_list, f)
    bot.send_message(message.chat.id, "Благодарим за помощь в разработке. Мы обязательно рассмотрим ваше проблему и сделаем всё возможное для ее исправления.")
    print(report_list)
print(report_list)

#Команда /contacts
@bot.message_handler(commands=['contacts'])
def contacts(message):
    bot.send_message(message.chat.id, 'Контакты:\n'
                                      'Мой VK - https://vk.com/vladgolovichpk\n'
                                      'Почта - bot_gamer_info@mail.ru\n'
                                      'ВНИМАНИЕ! Писать только по делу. Любой спам или информация, не косающаяся бота будет банится. Надеюсь на понимание)')

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
                                      f"Тут вы сможете выбрать актуальные игровые новости на нужные вам темы!\n"
                                      f"К сожалению, Вы ещё не зарегестрированы в системе(\n"
                                      f"Для регестрации введите команду - /reg")



#РЕГИСТРАЦИЯ
@bot.message_handler(commands=['reg'])
def reg(message):
    userid = message.chat.id
    for i in users:
        if userid == int(i):
            bot.send_message(message.chat.id, "Вы уже зарегестрированы.\n"
                                              "Для помощи напишите команду /help")
            return

    users.append(userid)
    bot.send_message(message.chat.id, f"Поздравляю, Вы успешно зарегстрировались в системе!\n" 
                                      f"Выберите игру, по которой я буду отбирать для вас новости:\n"
                                      f"VALORANT - /VALORANT\n"
                                      f"Для помощи напишите команду /help")
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