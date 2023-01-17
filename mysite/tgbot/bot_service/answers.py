import os.path
from . import file_service, extract_data
from start import bot
from zipfile import ZipFile

FileService = file_service.FileService_class()
DataExtractor = extract_data.DataExtractor_class()


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
        bot.sendMessage(chat_id, "Цей бот дозволяє конвертувати зображення у pdf-файл.\n\n"
                                 "Введіть команду /images_to_pdf та робіть усе згідно з наданими інструкціями\n"
                                 "͡° ͜ʖ ͡°")
