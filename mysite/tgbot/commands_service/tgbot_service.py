import os
from pprint import pprint
from . import tgbot_answers, extract_data, tgbot_file_service
import enum
import json

Answers = tgbot_answers.Answers_class
DataExtractor = extract_data.DataExtractor_class
FileService = tgbot_file_service.FileService_class


class Message_Type(enum.Enum):
    text = 1
    document = 2
    image = 3
    sticker = 4
    garbage = 5


class Extensions(enum.Enum):
    pdf = 1
    doc = 2
    txt = 3
    fb2 = 4


def detect_message_type(request_body):
    if 'text' in request_body['message']:
        return Message_Type.text
    elif 'document' in request_body['message']:
        return Message_Type.document
    elif 'photo' in request_body['message']:
        return Message_Type.image
    elif 'sticker' in request_body['message']:
        return Message_Type.sticker
    else:
        return Message_Type.garbage


def process_document(file_name, file_id, chat_id, new_extension: Extensions):
    new_extension = f'.{new_extension.name}'

    try:
        file_path = FileService.download_document(file_id, file_name)

        new_file_path = FileService.convert(new_extension, file_path)
        zip_path, zipObj = FileService.push_into_zip(new_file_path)

        new_file_name = os.path.splitext(file_name)[0] + new_extension
        Answers.send_document(chat_id, new_file_name, zipObj)

        print('file_path = ' + file_path)
        print('zip_path = ' + zip_path)
        print('new_file_path = ' + new_file_path)

        os.remove(file_path)
        zipObj.close()
        os.remove(zip_path)

        if file_path != new_file_path:
            os.remove(new_file_path)

    except Exception as e:
        print(f'{str(e)}')
        Answers.send_message(chat_id, 'Sorry, some error occured :(')


def save_to_json(request_body):
    with open('mysite\\tgbot\\commands_service\\downloads\\data.json', 'r') as rd:
        data_list = json.load(rd)

    data_list.append(request_body)

    with open('mysite\\tgbot\\commands_service\\downloads\\data.json', 'w') as fp:
        json.dump(data_list, fp, indent=4)


def find_last_command(user_name):
    with open('mysite\\tgbot\\commands_service\\downloads\\data.json', 'r') as rd:
        data_list: list = json.load(rd)
        data_list.reverse()
        for i in range(0, len(data_list)):
            if user_name == DataExtractor.get_user_name(data_list[i]):
                if detect_message_type(data_list[i]) is Message_Type.text:
                    return data_list[i]['message']['text']
    return 'ERROR'


def find_last_document(user_name):
    with open('mysite\\tgbot\\commands_service\\downloads\\data.json', 'r') as rd:
        data_list: list = json.load(rd)
        data_list.reverse()

        for i in range(0, len(data_list)):
            if user_name == DataExtractor.get_user_name(data_list[i]):
                if detect_message_type(data_list[i]) == Message_Type.document:
                    return data_list[i]['message']['document']['file_name'], data_list[i]['message']['document']['file_id']

    return -1


def clear_data_file():
    with open('mysite\\tgbot\\commands_service\\downloads\\data.json', 'w') as fp:
        data_list = []
        json.dump(data_list, fp, indent=4)


# __14.07.2022__  <-->  Ivan (⓿_⓿)

def need_asking(user_name):
    import datetime

    with open('mysite\\tgbot\\commands_service\\downloads\\data.json', 'r') as rd:
        data_list: list = json.load(rd)
        data_list.reverse()

        for i in range(0, len(data_list)):
            if DataExtractor.get_user_name(data_list[i]) == user_name and DataExtractor.get_user_name(
                    data_list[i + 1]) == user_name:
                message_date_1 = datetime.datetime.fromtimestamp(DataExtractor.get_message_date(data_list[i]))
                message_date_2 = datetime.datetime.fromtimestamp(DataExtractor.get_message_date(data_list[i + 1]))
                time_difference = message_date_1 - message_date_2
                if time_difference > datetime.timedelta(0, 1):
                    return True
                else:
                    return False

    return False


def execute_command(request_body):
    save_to_json(request_body)
    chat_id = DataExtractor.get_chat_id(request_body)
    user_name = DataExtractor.get_user_name(request_body)

    if detect_message_type(request_body) == Message_Type.text:

        # Main commands:
        if DataExtractor.get_message_text(request_body) == '/images_to_pdf' or DataExtractor.get_message_text(
                request_body) == '/convert_document':

            if DataExtractor.get_message_text(request_body) == '/images_to_pdf':
                Answers.send_message(chat_id, "Waiting for images")

            elif DataExtractor.get_message_text(request_body) == '/convert_document':
                Answers.send_message(chat_id, "Waiting for document")

        # Secondary commands:
        else:
            if DataExtractor.get_message_text(request_body) == '/end':
                Answers.send_message(chat_id, "Creating pdf...")

            else:
                if find_last_command(user_name) == f'/{Extensions.pdf.name}':
                    file_name, file_id = find_last_document(user_name)
                    Answers.send_message(chat_id, 'Processing document. New extension - .pdf')
                    process_document(file_name, file_id, chat_id, Extensions.pdf)

                elif find_last_command(user_name) == f'/{Extensions.doc.name}':
                    file_name, file_id = find_last_document(user_name)
                    Answers.send_message(chat_id, 'Processing document. New extension - .doc')
                    process_document(file_name, file_id, chat_id, Extensions.doc)

                elif find_last_command(user_name) == f'/{Extensions.txt.name}':
                    file_name, file_id = find_last_document(user_name)
                    Answers.send_message(chat_id, 'Processing document. New extension - .txt')
                    process_document(file_name, file_id, chat_id, Extensions.txt)

                elif find_last_command(user_name) == f'/{Extensions.fb2.name}':
                    file_name, file_id = find_last_document(user_name)
                    Answers.send_message(chat_id, 'Processing document. New extension - .fb2')
                    process_document(file_name, file_id, chat_id, Extensions.fb2)

    elif detect_message_type(request_body) == Message_Type.image:
        if need_asking(user_name):
            Answers.send_message(chat_id, "Press /end to create pdf file")

    elif detect_message_type(request_body) == Message_Type.document:
        Answers.send_message(chat_id, "Choose 1 of the following extensions:")
        Answers.send_message(chat_id, "/pdf\n/doc\n/txt\n/fb2 (this one I need to fix)")