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