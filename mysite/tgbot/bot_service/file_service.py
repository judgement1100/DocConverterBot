import sys
from zipfile import ZipFile
from os.path import basename
from PIL import Image, ImageOps
sys.path.append(f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot')
from start import bot
import os
import json
from . import auxiliary_stuff, extract_data, common_service, answers


DataExtractor = extract_data.DataExtractor_class()

Message_Type = auxiliary_stuff.Message_Type


class FileService_class:

    def download_document_zip(self, file_id, file_name):
        file_path = f'/mysite/tgbot/bot_service\\downloads\\{file_name}'
        bot.download_file(self, file_id, file_path)
        zip_path = f'/mysite/tgbot/bot_service\\downloads\\{os.path.splitext(file_name)[0]}.zip'

        zipObj = ZipFile(zip_path, 'w')
        zipObj.write(file_path, basename(file_path))

        os.remove(file_path)

        return zip_path, zipObj


    def download_document(self, file_id, file_name):
        file_path = f'mysite\\tgbot\\bot_service\\downloads\\{file_name}'
        bot.download_file(file_id, file_path)
        return file_path


    def push_into_zip(self, file_path):
        file_name = basename(file_path)
        zip_path = f'mysite\\tgbot\\bot_service\\downloads\\{os.path.splitext(file_name)[0]}.zip'

        zipObj = ZipFile(zip_path, 'w')
        zipObj.write(file_path, basename(file_path))

        return zip_path, zipObj


    def process_creating_pdf_from_images(self, chat_id, user_name):
        Answers = answers.Answers_class()

        try:
            photos_list = self.download_images(user_name)
            if len(photos_list) > 0:
                pdf_path = self.create_pdf_from_images(photos_list)
                zip_path, zipObj = self.push_into_zip(pdf_path)
                Answers.send_document(chat_id, 'file.pdf', zipObj)

                zipObj.close()
                os.remove(zip_path)
                os.remove(pdf_path)
                for i in range(0, len(photos_list)):
                    os.remove(photos_list[i])
            else:
                Answers.send_message(chat_id, "Помилка. Можливо, ви не надіслали фото")
        except Exception as e:
            print("Error occured in function <process_creating_pdf_from_images>\n" + str(e))


    def download_images(self, user_name):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
            data_list = json.load(rd)
            data_list.reverse()
            photos_list = []
            counter = 1
            for i in range(0, len(data_list)):
                if DataExtractor.get_user_name(data_list[i]) == user_name:
                    if DataExtractor.detect_message_type(data_list[i]) == Message_Type.text:
                        if DataExtractor.get_message_text(data_list[i]) == '/images_to_pdf':
                            break
                        elif DataExtractor.get_message_text(data_list[i]) == '/end_session':
                            break

                    else: #TODO redo following if state. Must be 2 functions.
                        if DataExtractor.detect_message_type(data_list[i]) == Message_Type.image:
                            array = data_list[i]['message']['photo']
                            len1 = len(array)
                            dict1: dict = data_list[i]
                            file_id = dict1['message']['photo'][len1 - 1]['file_id']
                            file_name = f'image{counter}.jpg'
                            file_path = f'mysite\\tgbot\\bot_service\\downloads\\{file_name}'
                            counter += 1
                            photos_list.append(file_path)
                            bot.download_file(file_id, file_path)
                        elif DataExtractor.detect_message_type(data_list[i]) == common_service.Message_Type.compressed_image:
                            file_id = data_list[i]['message']['document']['file_id']
                            file_name = f'image{counter}.jpg'
                            file_path = f'mysite\\tgbot\\bot_service\\downloads\\{file_name}'
                            counter += 1
                            photos_list.append(file_path)
                            bot.download_file(file_id, file_path)

        return photos_list


    def create_pdf_from_images(self, photos_list: list):
        photos_count = len(photos_list)
        image_list = []

        for i in range(photos_count - 1, -1, -1):
            image = Image.open(f'mysite\\tgbot\\bot_service\\downloads\\image{i + 1}.jpg')
            image = ImageOps.exif_transpose(image)
            image_list.append(image)

        image_list[0].save(f'mysite\\tgbot\\bot_service\\downloads\\file.pdf', resolution=100.0, save_all=True,
                           append_images=image_list[1:])

        return f'mysite\\tgbot\\bot_service\\downloads\\file.pdf'


    def rename_file(self, file_path, new_filename):
        old_name = os.path.splitext(file_path)[0]
        os.rename(old_name, new_filename)


    def download_sticker(self, request_body):
        path = f'mysite\\tgbot\\bot_service\\downloads\\sticker.WEBP'
        bot.download_file(DataExtractor.get_file_id_sticker(request_body), path)
        return path


    def save_to_json(self, request_body):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
            data_list = json.load(rd)

        data_list.append(request_body)

        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'w') as fp:
            json.dump(data_list, fp, indent=4)


    def clean_data_file(self):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
            data_list: list = json.load(rd)
            if len(data_list) > 150:
                del data_list[:10]

        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'w') as fp:
            json.dump(data_list, fp, indent=4)


    def get_data_list(self):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
            data_list: list = json.load(rd)
            return data_list


    def set_data(self, data_list: list):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'w') as fp:
            json.dump(data_list, fp, indent=4)