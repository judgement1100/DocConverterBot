import os
import json
from . import auxiliary_stuff


Message_Type = auxiliary_stuff.Message_Type


class DataExtractor_class:

    def get_chat_id(self, request_body):
        return request_body['message']['chat']['id']


    def get_user_name(self, request_body):
        if self.detect_message_type(request_body) == Message_Type.callback_query:
            return request_body['callback_query']['from']['username']
        else:
            return request_body['message']['from']['username']


    def get_message_text(self, request_body):
        return request_body['message']['text']


    def get_file_id(self, request_body):
        return request_body['message']['document']['file_id']


    def get_file_extension(self, request_body):
        file_name = request_body['message']['document']['file_name']
        return os.path.splitext(file_name)[1]


    def get_file_name(self, request_body):
        return request_body['message']['document']['file_name']


    def get_message_date(self, request_body):
        if self.detect_message_type(request_body) == Message_Type.callback_query:
            return request_body['callback_query']['message']['date']
        else:
            return request_body['message']['date']


    def get_file_id_sticker(self, request_body):
        return request_body['message']['sticker']['file_id']


    def get_chat_id_from_callback(self, request_body):
        return request_body['callback_query']['message']['chat']['id']


    def get_user_name_from_callback(self, request_body):
        return request_body['callback_query']['message']['chat']['username']


    def get_callback_data(self, request_body):
        return request_body['callback_query']['data']


    def get_callback_query_id(self, request_body):
        return request_body['callback_query']['id']


    def get_chatID_and_username(self, request_body):
        if 'message' in request_body:
            chat_id = self.get_chat_id(request_body)
            user_name = self.get_user_name(request_body)
            return chat_id, user_name
        elif 'callback_query' in request_body:
            chat_id = self.get_chat_id_from_callback(request_body)
            user_name = self.get_user_name_from_callback(request_body)
            return chat_id, user_name


    def find_last_command(self, user_name):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
            data_list: list = json.load(rd)
            data_list.reverse()
            for i in range(0, len(data_list)):
                if user_name == self.get_user_name(data_list[i]):
                    if self.detect_message_type(data_list[i]) is Message_Type.text:
                        return data_list[i]['message']['text']
        return 'ERROR'


    def find_last_document(self, user_name):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
            data_list: list = json.load(rd)
            data_list.reverse()

            for i in range(0, len(data_list)):
                if user_name == self.get_user_name(data_list[i]):
                    print(data_list[i])
                    if self.detect_message_type(data_list[i]) == Message_Type.pdf_document:
                        print('ok')
                        return data_list[i]['message']['document']['file_name'], data_list[i]['message']['document'][
                            'file_id']

        return -1


    def is_command(self, text):
        if '/' in text:
            return True
        else:
            return False


    def get_message_text_before_previous(self, user_name):
        with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
            data_list: list = json.load(rd)
            data_list.reverse()

            for i in range(0, len(data_list)):
                if user_name == self.get_user_name(data_list[i]):
                    if (self.detect_message_type(data_list[i]) == Message_Type.text and
                        self.is_command(data_list[i]['message']['text'])):
                        if self.detect_message_type(data_list[i + 1]) == Message_Type.text:
                            return data_list[i + 1]['message']['text']

        return -1


    def detect_message_type(self, request_body):
        if 'callback_query' in request_body:
            return Message_Type.callback_query

        elif 'text' in request_body['message']:
            return Message_Type.text

        elif 'document' in request_body['message']:
            if 'thumb' in request_body['message']['document']:
                file_name = self.get_file_name(request_body)
                if os.path.splitext(file_name)[1] == '.jpg' or os.path.splitext(file_name)[1] == '.png' or \
                        os.path.splitext(file_name)[1] == '.jpeg':
                    return Message_Type.compressed_image
                elif os.path.splitext(file_name)[1] == '.pdf':
                    return Message_Type.pdf_document
                else:
                    return Message_Type.garbage
            else:
                return Message_Type.document

        elif 'photo' in request_body['message']:
            return Message_Type.image
        elif 'sticker' in request_body['message']:
            return Message_Type.sticker
        else:
            return Message_Type.garbage