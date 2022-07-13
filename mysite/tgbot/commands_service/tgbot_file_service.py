import telepot
import sys
from . import extract_data
import aspose.words as aw
import os
from zipfile import ZipFile
from os.path import basename


sys.path.append(f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot')
from start import bot

DataExtractor = extract_data.DataExtractor_class


class FileService_class:
    @staticmethod
    def download_document_zip(file_id, file_name):
        file_path = f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot\\mysite\\tgbot\\commands_service\\downloads\\{file_name}'
        bot.download_file(file_id, file_path)
        zip_path = f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot\\mysite\\tgbot\\commands_service\\downloads\\{os.path.splitext(file_name)[0]}.zip'

        zipObj = ZipFile(zip_path, 'w')
        zipObj.write(file_path, basename(file_path))

        os.remove(file_path)

        return zip_path, zipObj


    @staticmethod
    def download_document(file_id, file_name):
        file_path = f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot\\mysite\\tgbot\\commands_service\\downloads\\{file_name}'
        bot.download_file(file_id, file_path)
        return file_path


    @staticmethod
    def push_into_zip(file_path):
        file_name = basename(file_path)
        zip_path = f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot\\mysite\\tgbot\\commands_service\\downloads\\{os.path.splitext(file_name)[0]}.zip'

        zipObj = ZipFile(zip_path, 'w')
        zipObj.write(file_path, basename(file_path))

        return zip_path, zipObj


    @staticmethod
    def convert(new_extension, file_path):
        full_file_name = basename(file_path)
        row_file_name = os.path.splitext(full_file_name)[0]
        initial_extension = os.path.splitext(full_file_name)[1]
        path = os.path.dirname(file_path)

        doc = aw.Document(f'{path}\{row_file_name}' + initial_extension)
        doc.save(f'{path}\{row_file_name}' + new_extension)

        return f'{path}\{row_file_name}' + new_extension
