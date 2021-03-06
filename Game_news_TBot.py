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

    # Достаю заголовки и ссылки статей по Valorant
    page = requests.get('https://www.playground.ru/valorant/news')
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = str(soup.find_all(class_='post-title'))
    elements_copy = elements[1:len(elements) - 1]
    res_elements = ''
    VALORANT_title_list = []
    VALORANT_link_list = []
    while len(elements_copy) > 0:
        if elements_copy[0] == '<':
            elements_copy = elements_copy[elements_copy.find('>') + 1:]
        else:
            res_elements = elements_copy[:elements_copy.find('<')]
            if (res_elements != '\n' and res_elements != ', '):
                VALORANT_title_list.append(res_elements)
            elements_copy = elements_copy[elements_copy.find('<'):]
    VALORANT_title_list = VALORANT_title_list[0:10]
    elements_copy = elements[1:len(elements) - 1]
    while len(elements_copy) > 0:
        if elements_copy.find('href="') == -1:
            elements_copy = ''
        else:
            elements_copy = elements_copy[elements_copy.find('href="') + 6:]
            res_elements = elements_copy[:elements_copy.find('"')]
            VALORANT_link_list.append(res_elements)
    VALORANT_link_list = VALORANT_link_list[0:10]

    # Достаю статьи из VALORANT
    VALORANT_news = []
    for i in VALORANT_link_list:
        page = requests.get(i)
        soup = BeautifulSoup(page.content, 'html.parser')
        elements = str(soup.find_all(class_='article-content js-post-item-content'))
        elements = elements[1:len(elements) - 1]
        res_elements = ''
        while len(elements) > 0:
            if elements[0] == '<':
                elements = elements[elements.find('>') + 1:]
            else:
                res_elements += elements[:elements.find('<')]
                elements = elements[elements.find('<'):]
        VALORANT_news.append(res_elements)

    # Достаю заголовки и ссылки патчей по Valorant
    page = requests.get('https://xn--80aae1bleos.xn--p1ai/patch/')
    soup = BeautifulSoup(page.content, 'html.parser')
    elements = str(soup.find_all(class_='post-title entry-title'))
    elements_copy = elements[1:len(elements) - 1]
    res_elements = ''
    VALORANT_Patch_title_list = []
    VALORANT_Patch_link_list = []
    while len(elements_copy) > 0:
        if elements_copy[0] == '<':
            elements_copy = elements_copy[elements_copy.find('>') + 1:]
        else:
            res_elements = elements_copy[:elements_copy.find('<')]
            if (res_elements != '\n' and res_elements != ', '):
                VALORANT_Patch_title_list.append(res_elements)
            elements_copy = elements_copy[elements_copy.find('<'):]
    VALORANT_Patch_title_list = VALORANT_Patch_title_list[0:1]
    elements_copy = elements[1:len(elements) - 1]
    while len(elements_copy) > 0:
        if elements_copy.find('href="') == -1:
            elements_copy = ''
        else:
            elements_copy = elements_copy[elements_copy.find('href="') + 6:]
            res_elements = elements_copy[:elements_copy.find('"')]
            VALORANT_Patch_link_list.append(res_elements)
    VALORANT_Patch_link_list = VALORANT_Patch_link_list[0:1]

    # Достаю патчи VALORANT
    VALORANT_Patch_news = []
    for i in VALORANT_Patch_link_list:
        page = requests.get(i)
        soup = BeautifulSoup(page.content, 'html.parser')
        elements = str(soup.find_all(class_='post-inner group'))
        elements = elements[1:len(elements) - 1]
        res_elements = ''
        while len(elements) > 0:
            if elements[0] == '<':
                elements = elements[elements.find('>') + 1:]
            else:
                res_elements += elements[:elements.find('<')]
                elements = elements[elements.find('<'):]
        res_elements = res_elements[res_elements.find('Добавлен'):res_elements.find('Чуть менее краткий список изменений:')]
        VALORANT_Patch_news.append(res_elements)
    #print('tick')
    threading.Timer(1800, eVALORANT).start()
    res_list = [eVALORANT_title_list, eVALORANT_link_list, eVALORANT_news, VALORANT_title_list, VALORANT_link_list, VALORANT_news, VALORANT_Patch_title_list, VALORANT_Patch_link_list, VALORANT_Patch_news]
    return res_list

res_list = eVALORANT()
eVALORANT_title_list = res_list[0]
eVALORANT_link_list = res_list[1]
eVALORANT_news = res_list[2]
VALORANT_title_list = res_list[3]
VALORANT_link_list = res_list[4]
VALORANT_news = res_list[5]
VALORANT_Patch_title_list = res_list[6]
VALORANT_Patch_link_list = res_list[7]
VALORANT_Patch_news = res_list[8]



#Создаю кючи проверки выбранных тем для каждого пользователя
games_list = ['VALORANT']
game_check_list = []
for i in range(len(games_list)):
    game_check_list.append(False)
game_check_dict = {}

themes_list = ['eSports', 'game_news']
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
                                      f'В этом боте, буквально за пару кликов, Вы сможете узнать последние игровые новости, которые вам интересны!\n'
                                      f'Похоже Вы не знаете как пользоваться этим ботом. Позвольте я Вам всё разложу по полочкам) Вот список команд, которые поддерживает наш бот:\n'
                                      f'/start - Главное меню. Тут Вы выбираете интересующую Вас игру, по которой Вы хотите узнать новости.\n'
                                      f'/eSport - Данная команда будет доступна после выбора игры из команды /start. Она вам предложит список новостей из киберспорта. Рядом с новостью Вы увидете ее номер. Нажмите на него и получите желаемую статью.\n'
                                      f'/game_news - Данная команда будет доступна после выбора игры из команды /start. Она вам предложит список игровых новостей. Рядом с новостью Вы увидете ее номер. Нажмите на него и получите желаемую статью.\n'
                                      f'/Patch_Notes - Данная команда будет доступна после выбора игры из команды /start. Она покажет вам список изменений последнего патча выбранной игры.\n'
                                      f'/report - Используте данную команду для отправки жалоб на баги и ошибки, с которыми Вы столкнулись. Отправлять жалобу через пробел в том же сообщении, где и вызываете эту команду.\n'
                                      f'/exit - Выход на главное меню.\n'
                                      f'Если остались ещё вопросы или предложения, то напишите моему создателю. Получить его контакты можно с помощью команды /contacts\n'
                                      f'Желаю Вам приятного пользования. Надеюсь теперь Вам будет легче и проще пользоваться ботом)')

#Команда /report
@bot.message_handler(commands=['report'])
def report(message):
    message_text = message.text
    report_list.append(message_text)
    with open('report.pickle', 'wb') as f:
        pickle.dump(report_list, f)
    bot.send_message(message.chat.id, "Благодарим за помощь в разработке. Мы обязательно рассмотрим вашу проблему и сделаем всё возможное для ее исправления.")


#Команда /contacts
@bot.message_handler(commands=['contacts'])
def contacts(message):
    bot.send_message(message.chat.id, 'Контакты:\n'
                                      'Мой VK - https://vk.com/vladgolovichpk\n'
                                      'Почта - bot_gamer_info@mail.ru.\n'
                                      'ВНИМАНИЕ! Писать только по делу. Любой спам или информация, не косающаяся бота будет банится. Надеюсь на понимание)')

#Команда /start и приветствие
@bot.message_handler(commands=['start'])
def start(message):
    userid = message.chat.id
    for i in users:
        if userid == int(i):
            for j in range(len(game_check_dict[message.chat.id])):
                game_check_dict[message.chat.id][j] = False
            for j in range(len(themes_check_dict[message.chat.id])):
                themes_check_dict[message.chat.id][j] = False
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
    game_check_dict[userid] = []
    for j in game_check_list:
        game_check_dict[userid].append(j)
    themes_check_dict[userid] = []
    for j in themes_check_list:
        themes_check_dict[userid].append(j)
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
    for i in range(len(games_list)):
        game_check_dict[message.chat.id][i] = False
    game_check_dict[message.chat.id][0] = True
    bot.send_message(message.chat.id, f"Вы выбрали игру VALORANT.\n"
                                      f"Выберите наиболее интересующую Вас тему:\n"
                                      f"Киберспорт - /eSports\n"
                                      f"Игровые новости - /game_news\n"
                                      f"Изменения последнего патча - /Patch_Notes\n"
                                      f"\nГлавное меню - /exit")

#Выибор киберспорта
@bot.message_handler(commands=['eSports'])
def eSports(message):
    if game_check_dict[message.chat.id][0] == True:
        for i in range(len(themes_list)):
            themes_check_dict[message.chat.id][i] = False
        themes_check_dict[message.chat.id][0] = True
        mes = 'Выберите новость из мира киберспорта:\n'
        for i in range(len(eVALORANT_title_list)):
            mes += f'{eVALORANT_title_list[i]} - /{i + 1}\n'
        mes += '\nГлавное меню - /exit'
        bot.send_message(message.chat.id, mes)

#Выибор игровых новостей
@bot.message_handler(commands=['game_news'])
def game_news(message):
    if game_check_dict[message.chat.id][0] == True:
        for i in range(len(themes_list)):
            themes_check_dict[message.chat.id][i] = False
        themes_check_dict[message.chat.id][1] = True
        mes = 'Выберите игровую новость:\n'
        for i in range(len(VALORANT_title_list)):
            mes += f'{VALORANT_title_list[i]} - /{i + 1}\n'
        mes += '\nГлавное меню - /exit'
        bot.send_message(message.chat.id, mes)

#Команда /Patch_Notes
@bot.message_handler(commands=['Patch_Notes'])
def Patch_Notes(message):
    if game_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, VALORANT_Patch_news[0] + '\nГлавное меню - /exit')

#Вывожу статью, которую выбрал пользователь
@bot.message_handler(commands=['1'])
def n1(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[0] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[0] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['2'])
def n2(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[1] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[1] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['3'])
def n3(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[2] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[2] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['4'])
def n4(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[3] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[3] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['5'])
def n5(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[4] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[4] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['6'])
def n6(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[5] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[5] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['7'])
def n7(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[6] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[6] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['8'])
def n8(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[7] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[7] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['9'])
def n9(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[8] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[8] + '\nГлавное меню - /exit')

@bot.message_handler(commands=['10'])
def n10(message):
    if themes_check_dict[message.chat.id][0] == True:
        bot.send_message(message.chat.id, eVALORANT_news[9] + '\nГлавное меню - /exit')
    if themes_check_dict[message.chat.id][1] == True:
        bot.send_message(message.chat.id, VALORANT_news[9] + '\nГлавное меню - /exit')

#Команда для выхода на стартовое меню
@bot.message_handler(commands=['exit'])
def exit(message):
    start(message)


if __name__ == '__main__':
    bot.polling()