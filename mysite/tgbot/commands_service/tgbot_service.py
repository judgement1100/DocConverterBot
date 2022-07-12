from . import tgbot_answers, extract_data
import enum


Answers = tgbot_answers.Answers_class
DataExtractor = extract_data.DataExtractor_class


class Message_Type(enum.Enum):
    text = 1
    document = 2
    image = 3
    garbage = 4


def detect_message_type(request_body):
    if 'text' in request_body['message']:
        return Message_Type.text
    elif 'document' in request_body['message']:
        return Message_Type.document
    elif 'photo' in request_body['message']:
        return Message_Type.image
    else:
        return Message_Type.garbage


def execute_command(request_body):
    chat_id = DataExtractor.get_chat_id(request_body)

    if detect_message_type(request_body) is Message_Type.text:
        Answers.send_message(chat_id, "You've sent a text:\n" + f'{DataExtractor.get_message_text(request_body)}')
    elif detect_message_type(request_body) is Message_Type.document:
        Answers.send_message(chat_id, "You've sent a document")
    elif detect_message_type(request_body) is Message_Type.image:
        Answers.send_message(chat_id, "You've sent an image")
    elif detect_message_type(request_body) is Message_Type.garbage:
        Answers.send_message(chat_id, "Cannot detect the type of file :(")










