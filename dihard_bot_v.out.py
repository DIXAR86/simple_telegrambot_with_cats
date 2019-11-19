import json
import re
import requests
import telebot
import numpy as np

name_dict_of_users = np.load('dict_users.npy').item()
tnl=[]

def init_bot():
    return telebot.TeleBot('put here your Telegram token')
bot = init_bot()



@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Меня зовут dihard_testbot_v.251118")
    bot.send_message(message.chat.id, "Предлагаю познакомиться \n"
                                      "Для этого набери команду: \n"
                                      "/hi")
    bot.send_message(message.chat.id, "Полный список команд можно вызвать \n"
                                      "коммандой /clist")

    bot.send_message(message.chat.id, "А еще я могу напостить фотки котиков, просто попроси меня: \n"
                                      "Пришли мне кота \n"
                                      "Пришли мне N котов (N число от 0 до 9)")


@bot.message_handler(commands=['clist'])
def commands_lost(message):
    bot.send_message(message.chat.id, "/hi - знакомство с ботом. Бот спрашивает ваше имя и потом его запоминает \n"
                                      "/сlsit - вызывает лист команд для данного бота \n"
                                      "/chname - позволяте сменить имя которое бот запомнил раньше \n")



@bot.message_handler(commands=['chname'])
def change_name(message):
    bot.send_message(message.chat.id, 'Введите Ваше имя:')
    tnl.append('1')


@bot.message_handler(commands=['hi','HI','Hi','hI'])
def send_hi_by_name(message):
    if message.chat.id in name_dict_of_users:
        extract_name = name_dict_of_users.get(message.chat.id)
        bot.send_message(message.chat.id, "Привет {}!".format(extract_name))
    elif len(tnl)==0:
        bot.send_message(message.chat.id, "Привет! Как тебя зовут?")
        tnl.append('1')



@bot.message_handler(func=lambda m: 'привет' in m.text.lower())
def echo_all_if_hi(message):
    if message.chat.id in name_dict_of_users:
        extract_name = name_dict_of_users.get(message.chat.id)
        bot.send_message(message.chat.id, "Привет {}!".format(extract_name))
    else:
        bot.send_message(message.chat.id, "Приветсвую тебя человек!")



@bot.message_handler(func=lambda m: 'пришли мне кота' in m.text.lower())
def send_cat(message):
    if message.chat.id in name_dict_of_users:
        extract_name = name_dict_of_users.get(message.chat.id)
        bot.send_message(message.chat.id, 'Вот тебе кот,  {}'.format(extract_name))
        url = 'https://api.thecatapi.com/v1/images/search'
        result = requests.get(url)
        cat_url = json.loads(result.text)[0]['url']
        bot.send_message(message.chat.id, cat_url)
    else:
        bot.send_message(message.chat.id, 'Вот тебе кот,  {}'.format(message.chat.first_name))
        url = 'https://api.thecatapi.com/v1/images/search'
        result = requests.get(url)
        cat_url = json.loads(result.text)[0]['url']
        bot.send_message(message.chat.id, cat_url)



@bot.message_handler(func=lambda m: True)
def send_N_cat(message):
    if re.match('[Пп]ришли мне ([0-9]) кот[ао]*', message.text):
        match = re.findall(r'\d{1}', message.text)
        x=int(*match)
        if match:
            counter = 0
            while counter < x:
                url = 'https://api.thecatapi.com/v1/images/search'
                result = requests.get(url)
                cat_url = json.loads(result.text)[0]['url']
                bot.send_message(message.chat.id, cat_url)
                counter += 1
    elif len(tnl)!=0:
        name_dict_of_users.update({message.chat.id: message.text})
        np.save('dict_users.npy', name_dict_of_users)
        del tnl[0]
    else:
        bot.reply_to(message, message.text)



while True:
    try:
        bot.polling()
    except KeyboardInterrupt:
        break
    except:
        bot = init_bot()