import os.path
import sys
from . import file_service
from start import bot
from zipfile import ZipFile
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

FileService = file_service.FileService_class()


class Answers_class:

    def send_message(self, chat_id, message_text):
        bot.sendMessage(chat_id, message_text)


    def send_document(self, chat_id, file_name, zipObj: ZipFile):
        bot.sendDocument(chat_id, zipObj.open(file_name, mode='r'))


    def send_дуля(self, chat_id):
        zip_path, zipObj = FileService.push_into_zip(f'mysite\\tgbot\\commands_service\\downloads\\_дуля.WEBP')
        Answers_class.send_document(chat_id, '_дуля.WEBP', zipObj)
        zipObj.close()
        os.remove(zip_path)


    def reply_with_inline_keyboard(self, chat_id):
        bot.sendMessage(chat_id, 'some text',
                        reply_markup=InlineKeyboardMarkup(
                            inline_keyboard=[
                                [
                                    InlineKeyboardButton(text='button1', callback_data="one")
                                ]
                            ]
                        ))


