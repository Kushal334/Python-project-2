import datetime

import telebot
from telebot.types import Message
from telebot import types
from pytube import YouTube
import os

# initialization

api = '2133317357:AAEAEsYGXuZqD0psX-GapGh1YjCrFcNkToU'  # api key from telegram @BotFather
bot = telebot.TeleBot(api)

link = []

# emojis
audio_emoji = u'\U0001F3B5'
video_emoji = u'\U0001F3AC'
error_emoji = u'\U00002716'
download_emoji = u'\U00002B07'
done_emoji = u'\U00002714'


@bot.message_handler(commands=['start'])  # Welcome message
def send_welcome(message):
    log_and_print(message.from_user.username, message.from_user.id, message.text, message.chat.id)
    bot.reply_to(message, "To download audio or video from YouTube or YouTube Music send me a link.")


@bot.message_handler(content_types=['text'])
def url_handler(message):
    text = message.text  # Checking the link
    if 'https://www.youtube.com/' in text or 'https://youtube.com/' in text \
            or 'https://music.youtube.com/' in text or 'https://youtu.be/' in text \
            or 'https://m.youtube.com/' in text:
        link.append(text)
        save_buttons(message)
    else:
        log_and_print(message.from_user.username, message.from_user.id, message.text, message.chat.id)
        bot.send_message(message.chat.id, 'Please, send me a YouTube link.')


def save_buttons(message):  # Buttons added for user choices
    keyboard = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton(text='Audio' + audio_emoji, callback_data='save_audio')
    button2 = types.InlineKeyboardButton(text='Video' + video_emoji, callback_data='save_video')
    keyboard.add(button1, button2)
    log_and_print(message.from_user.username, message.from_user.id, message.text, message.chat.id)
    bot.send_message(message.chat.id, 'What do you want to download?', reply_markup=keyboard)


def log_and_print(user, user_id, message, chat_id):
    with open(str(user_id) + '.log', 'a') as f:
        f.write('{0} ({1})  -  {2}\n'.format(user_id, user, str(datetime.datetime.now())))
        f.write('-----------------------------------------------------------\n')
        f.write(message + '\n')
        if user == 'Bot':
            bot.send_message(chat_id, message)
        f.write('-----------------------------------------------------------\n')


@bot.callback_query_handler(func=lambda call: True)
def buttons(call):
    if call.data == 'save_audio':
        save_audio(call.message)

    elif call.data == 'save_video':
        save_video(call.message)


def save_audio(message):
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text='Audio download has started.' + download_emoji)
        url = link  # link = message text
        yt = YouTube(str(url))
        ys = yt.streams.get_audio_only()
        audio = ys.download()  # audio download
        name = yt.title  # saving video title to rename the file
        os.rename(audio, 'audio.mp3')  # file renaming for correct deletion

        audio = open('audio.mp3', 'rb')
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text='Download completed successfully.' + done_emoji)
        log_and_print(message.from_user.username, message.from_user.id, message.text, message.chat.id)
        bot.send_audio(message.chat.id, audio, title=name)
        audio.close()
        os.remove('audio.mp3')  # removing file from the server
        link.clear()  # link clearing for the next url
    except:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text='Failed to upload audio.' + error_emoji)
        link.clear()


def save_video(message):
    try:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text='Video download has started.' + download_emoji)
        url = link  # link = message text
        yt = YouTube(str(url))
        ys = yt.streams.get_highest_resolution()
        video = ys.download()  # video download
        os.rename(video, 'video.mp4')  # file renaming for correct deletion

        video = open('video.mp4', 'rb')
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text='Download completed successfully.' + done_emoji)
        log_and_print(message.from_user.username, message.from_user.id, message.text, message.chat.id)
        bot.send_video(message.chat.id, video)
        video.close()
        os.remove('video.mp4')  # removing file from the server
        link.clear()  # link clearing for the next url

    except:
        bot.edit_message_text(chat_id=message.chat.id, message_id=message.message_id,
                              text='Failed to upload video.' + error_emoji)
        link.clear()


if __name__ == '__main__':
    bot.polling(True)
