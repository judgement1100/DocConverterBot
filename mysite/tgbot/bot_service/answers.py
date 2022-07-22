import os.path
import sys
from . import file_service, auxiliary_stuff
from start import bot
from zipfile import ZipFile
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton

FileService = file_service.FileService_class()
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
                                 "У разі недотримання вказівок, які надає бот, існує ймовірність отримати непогану таку дулю у відповідь.\n"
                                 "2) /convert_document: конвертація текстових файлів у одне з наступних розширень:\n"
                                 ".pdf, .doc, .txt, .fb2, .epub, .mobi.\n"
                                 "Зауваження про дулю досі актуальне.\n\n"
                                 "Порядок виконання дій:\n"
                                 "1) Оберіть команду серед запропонованих у списку\n"
                                 "2) Робіть, що вказано в інструкції  ͡° ͜ʖ ͡°")


    def reply_with_inline_keyboard(self, chat_id, text, keyboardStatus: KeyboardStatus):
        if keyboardStatus == KeyboardStatus.initial:
            bot.sendMessage(chat_id, text,
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Створити pdf із зображень', callback_data="images_to_pdf")
                                    ],
                                    [
                                        InlineKeyboardButton(text='Конвертувати текстовий документ', callback_data="convert_document")
                                    ]
                                ]
                            ))

        elif keyboardStatus == KeyboardStatus.asking_for_end:
            bot.sendMessage(chat_id, text,
                            reply_markup=InlineKeyboardMarkup(
                                inline_keyboard=[
                                    [
                                        InlineKeyboardButton(text='Так', callback_data="end")
                                    ]
                                ]
                            ))

        elif keyboardStatus == KeyboardStatus.after_end:
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
