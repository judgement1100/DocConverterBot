import os.path
import sys
from . import tgbot_file_service
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import telepot

sys.path.append(f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot')
from start import bot
from zipfile import ZipFile

FileService = tgbot_file_service.FileService_class


class Answers_class:
    @staticmethod
    def say_hello(chat_id, user_name):
        bot.sendMessage(chat_id, f'Слава Україні, {user_name}!')

    @staticmethod
    def send_message(chat_id, message_text):
        bot.sendMessage(chat_id, message_text)

    @staticmethod
    def send_document(chat_id, file_name, zipObj: ZipFile):
        bot.sendDocument(chat_id, zipObj.open(file_name, mode='r'))

    @staticmethod
    def reply_with_buttons(chat_id):
        bot.sendMessage(chat_id, 'Deleting keyboard', reply_markup=ReplyKeyboardRemove())

        # bot.sendMessage(chat_id, 'test', reply_markup=ReplyKeyboardMarkup(keyboard=[[
        #     KeyboardButton(text="/images_to_pdf"), KeyboardButton(text="/convert_document")]]))
