"""
My 5th bot.
I don't actually like those films, but that was an order. And, frankly, a very interesting one!
"""
from bs4 import BeautifulSoup
from datetime import datetime
import requests
import telebot
import json


def search_link(name):
    """Find a link for a film"""
    with open("database.json", "r", encoding="utf-8") as f:
        database = json.load(f)
    try:
        return "https://doramalive.ru" + database[name]
    # If there is no such film:
    except:
        return "error"


def parse_dorama_page(link):
    """Parse the film webpage"""
    res = requests.get(link)
    soup = BeautifulSoup(res.text, 'html.parser')
    dorama = {}
    # Put the information into the dictionary
    dorama["link"] = link
    dorama["name"] = " ".join(soup.find("h1").string.split()[1::])
    dorama["rating"] = soup.find("div", class_="vote-detail").get_text()
    dorama["description"] = soup.find("div", class_="detail-more").get_text()
    parametrs = soup.find_all("dl", class_="dl-horizontal")
    for parametr in parametrs:
        par = parametr.find_all("dd")
        dorama["made_in"] = par[1].get_text()
        dorama["made_date"] = par[2].get_text()
    dorama["genres"] = []
    genres = soup.find_all("span", "label label-default genre")
    for genre in genres:
        dorama["genres"].append(" ".join(genre.find("a").get("title").split()[2::]).title())
    return dorama


# BOT STARTS HERE ###
bot = telebot.TeleBot("2133317357:AAEAEsYGXuZqD0psX-GapGh1YjCrFcNkToU")
print("Bot is active!")

@bot.message_handler(commands=["start"])
def command_start(message):
    """Handler of the first command /start"""
    bot.send_message(message.chat.id, "✨")
    bot.send_message(message.chat.id, "Привет! Я помогу вам найти информацию о дорамах. "
                                      "Просто напишите мне название, а всё вам о ней расскажу!")


@bot.message_handler(content_types=['text'])
def reply(message):
    """Handler of any text message. It is supposed to be the name of a film"""
    print(f"Human: {not (message.from_user.is_bot)} || Name: {message.from_user.first_name} "
          f"{message.from_user.last_name} || Id: {message.from_user.id} || Time: {datetime.now().strftime('%H:%M')};")
    link = search_link(message.text.lower())
    # If there is no such film:
    if link == "error":
        bot.send_message(message.chat.id, "К сожаленю такой дорамы нет. Или вы неверно "
                                          "ввели название ☹️ Попробуйте, пожалуйста, ещё раз.")
    # If there is
    else:
        dorama = parse_dorama_page(link)
        n = round(float(dorama["rating"].split()[0]))
        stars = ["⭐" for i in range(n)]
        msg = f"<b>Название:</b> {dorama['name']}\n<b>Производство:</b> {dorama['made_in']}\n<b>Дата премьеры:" \
              f"</b> {dorama['made_date']}\n<b>Рейтинг: {''.join(stars)}</b> {dorama['rating']}\n<b>Жанры: ▫️</b> " \
              f"{'▫️'.join(dorama['genres'])}\n<b>Описание:</b> {dorama['description']}\n<b>Ссылка:</b> " \
              f"{dorama['link']}"
        bot.send_message(message.chat.id, msg, parse_mode="html")


bot.polling(none_stop=True, interval=0)