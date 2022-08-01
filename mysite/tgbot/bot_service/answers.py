import os.path
import sys
from . import file_service, auxiliary_stuff, extract_data
from start import bot
from zipfile import ZipFile
import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

FileService = file_service.FileService_class()
DataExtractor = extract_data.DataExtractor_class()
KeyboardStatus = auxiliary_stuff.InlineKeyboard_Status


class Answers_class:

    def send_message(self, chat_id, message_text):
        bot.sendMessage(chat_id, message_text)


    def send_document(self, chat_id, file_name, zipObj: ZipFile):
        bot.sendDocument(chat_id, zipObj.open(file_name, mode='r'))


    def send_дуля(self, chat_id):
        zip_path, zipObj = FileService.push_into_zip(f'mysite\\tgbot\\bot_service\\downloads\\_дуля.WEBP')
        self.send_document(chat_id, '_дуля.WEBP', zipObj)
        zipObj.close()
        os.remove(zip_path)


    def send_help_list(self, chat_id):
        bot.sendMessage(chat_id, "Опис команд:\n"
                                 "1) /images_to_pdf: конвертація стиснених і нестиснених фотографій у pdf файл.\n"
                                 "2) /convert_document: конвертація текстових файлів у одне з наступних розширень:\n"
                                 ".pdf, .doc, .txt, .fb2, .epub, .mobi.\n\n"
                                 "Порядок виконання дій:\n"
                                 "1) Оберіть команду серед запропонованих у списку\n"
                                 "2) Робіть, що вказано в інструкції\n"
                                 "3) У разі недотримання вказівок існує ймовірність отримати дулю\n"
                                 "͡° ͜ʖ ͡°")


    def reply_with_inline_keyboard(self, chat_id, text, keyboardStatus: KeyboardStatus):
        if keyboardStatus == KeyboardStatus.after_end:
            bot.sendMessage(chat_id, text,
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Продовжити створення', callback_data="continue_creating_pdf")
                                    ],
                                    [
                                        InlineKeyboardButton(text='Створити новий pdf', callback_data="images_to_pdf")
                                    ],
                                    [
                                        InlineKeyboardButton(text='Завершити створення pdf', callback_data="finish_creating_pdf")
                                    ]
                                ]
                            ))
