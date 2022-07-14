import os


class DataExtractor_class:
    @staticmethod
    def get_chat_id(request_body):
        return request_body['message']['chat']['id']

    @staticmethod
    def get_user_name(request_body):
        return request_body['message']['from']['username']

    @staticmethod
    def get_message_text(request_body):
        return request_body['message']['text']

    @staticmethod
    def get_file_id(request_body):
        return request_body['message']['document']['file_id']

    @staticmethod
    def get_file_extension(request_body):
        file_name = request_body['message']['document']['file_name']
        return os.path.splitext(file_name)[1]

    @staticmethod
    def get_file_name(request_body):
        return request_body['message']['document']['file_name']

    @staticmethod
    def get_message_date(request_body):
        return request_body['message']['date']

    @staticmethod
    def get_file_id_sticker(request_body):
        return request_body['message']['sticker']['file_id']
