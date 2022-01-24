import logging
import requests
import telebot
import random
from lxml import html

logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)


def main(genre):
    parsed_data, movie_list, rating_list, img_list, country_list, genre_item_list, url_list = [], [], [], [], [], [], []

    genre_dict = {'боевик': 'action/', 'фантастика': 'sci-fi/', 'драма': 'drama/', 'детектив': 'mystery/',
                  'ужасы': 'horror/', 'фэнтези': 'fantasy/', 'приключения': 'adventure/', 'триллер': 'thriller/',
                  'мелодрама': 'romance/', 'мультфильм': 'animation/',
                  'комедия': 'comedy/', 'криминал': 'crime/'}
    url = f'https://www.kinopoisk.ru/popular/films/{genre_dict.get(genre)}?sort=popularity&tab=all'
    r = requests.get(url)
    print(r.status_code)
    t = html.fromstring(r.content.decode('utf-8'))
    try:
        page = t.xpath("//a[@class='paginator__page-number']/text()")[-1]
    except IndexError:
        page = 1
    for page_index in range(1, int(page) + 1):
        print(f'Page: {page_index}')
        url = f'https://www.kinopoisk.ru/popular/films/{genre_dict.get(genre)}?page={page_index}&sort=popularity&tab=all'
        print(url)
        r1 = requests.get(url)
        t = html.fromstring(r1.content.decode('utf-8'))
        no_movie = t.xpath("//span[@class='rating__value rating__value_positive']/text()")
        for i in range(31):
            genre_list = t.xpath(f"//div[contains(@class,'desktop-rating-selection-film-item')]"
                                 f"[{i}]/div[2]/div[1]/div[1]/div/a/p[3]/span[2]/text()")
            for item in genre_list:
                if genre in item and not '%' in no_movie:
                    name = t.xpath("//p[@class='selection-film-item-meta__name']/text()")[i - 1]
                    img = t.xpath("//img[@class='selection-film-item-poster__image']/@src")[i - 1]
                    country = t.xpath("//span[@class='selection-film-item-meta__meta-additional-item'][1]/text()")[
                        i - 1]
                    item_genre = t.xpath("//span[@class='selection-film-item-meta__meta-additional-item'][2]/text()")[
                        i - 1]
                    url_item = t.xpath("//a[@class='selection-film-item-meta__link']/@href")[i - 1]
                    rating_item = t.xpath("//span[contains(@class,'rating__value')]/text()")[i - 1]

                    movie_list.append(name)
                    img_list.append(img)
                    country_list.append(country)
                    genre_item_list.append(item_genre)
                    url_list.append(url_item)
                    rating_list.append(rating_item)
                else:
                    pass
    for i in range(len(movie_list)):
        parsed_data.append({
            'Movie name': movie_list[i],
            'Country': country_list[i],
            'Genre': genre_item_list[i],
            'Url': url_list[i],
            'Rating': rating_list[i]
        })
    r.close()
    return parsed_data


bot = telebot.TeleBot(token='2133317357:AAEAEsYGXuZqD0psX-GapGh1YjCrFcNkToU')


def keyboard():
    markup = telebot.types.InlineKeyboardMarkup(row_width=3)
    button1 = telebot.types.InlineKeyboardButton(text='Комедия 😂', callback_data='комедия')
    button2 = telebot.types.InlineKeyboardButton(text='Драма 😢', callback_data='драма')
    button3 = telebot.types.InlineKeyboardButton(text='Боевик 🔥', callback_data='боевик')
    button4 = telebot.types.InlineKeyboardButton(text='Фантастика 👽', callback_data='фантастика')
    button5 = telebot.types.InlineKeyboardButton(text='Детектив 🕵', callback_data='детектив')
    button6 = telebot.types.InlineKeyboardButton(text='Ужасы 😱', callback_data='ужасы')
    button7 = telebot.types.InlineKeyboardButton(text='Фэнтези 🧛‍♂', callback_data='фэнтези')
    button8 = telebot.types.InlineKeyboardButton(text='Приключения', callback_data='приключения')
    button9 = telebot.types.InlineKeyboardButton(text='Триллер 😲', callback_data='триллер')
    button10 = telebot.types.InlineKeyboardButton(text='Мелодрама 💑', callback_data='мелодрама')
    button11 = telebot.types.InlineKeyboardButton(text='Мультфильм 🍭', callback_data='мультфильм')
    button12 = telebot.types.InlineKeyboardButton(text='Криминал 🔪', callback_data='криминал')
    markup.add(button1, button2, button3, button4, button5, button6, button7, button8
               , button9, button10, button11, button12)
    return markup


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, f'Здравствуй, {message.from_user.first_name}!\nВыберите жанр.',
                     reply_markup=keyboard())


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    cqd = call.data
    if cqd == 'комедия':
        get_movie(cqd, call)
    elif cqd == 'драма':
        get_movie(cqd, call)
    elif cqd == 'боевик':
        get_movie(cqd, call)
    elif cqd == 'фантастика':
        get_movie(cqd, call)
    elif cqd == 'детектив':
        get_movie(cqd, call)
    elif cqd == 'ужасы':
        get_movie(cqd, call)
    elif cqd == 'фэнтези':
        get_movie(cqd, call)
    elif cqd == 'приключения':
        get_movie(cqd, call)
    elif cqd == 'триллер':
        get_movie(cqd, call)
    elif cqd == 'мелодрама':
        get_movie(cqd, call)
    elif cqd == 'мультфильм':
        get_movie(cqd, call)
    elif cqd == 'криминал':
        get_movie(cqd, call)
    else:
        bot.send_message(call.message.chat.id, text=f'Неизвестная ошибка!')


def get_movie(cqd, call):
    bot.send_message(call.message.chat.id, text='Подбираю фильм')
    result = main(cqd)
    new_result = random.sample(list(result), 5)
    for i in range(len(new_result)):
        bot.send_message(call.message.chat.id, text=f"{i + 1}. \nНазвание: {new_result[i]['Movie name']}"
                                                    f"\nСтрана: {new_result[i]['Country']}\n"f"Жанр: {new_result[i]['Genre']}\n"
                                                    f"Ссылка: https://www.kinopoisk.ru/{new_result[i]['Url']}\n"
                                                    f"Оценка: {new_result[i]['Rating']}")
    bot.send_message(call.message.chat.id, text='\nВыберите жанр', reply_markup=keyboard())


bot.polling()

