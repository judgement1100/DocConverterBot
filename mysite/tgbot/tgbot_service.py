from . import tgbot_answers
from . import extract_data
import telepot

ans = tgbot_answers.Answers_class()


def execute_command(request_body):
    user_data_dict = {'chat_id': extract_data.DataExtractor_class.get_chat_id(request_body),
                      'user_name': extract_data.DataExtractor_class.get_user_name(request_body),
                      'message_text': extract_data.DataExtractor_class.get_message_text(request_body)}

    # ans.say_hello(user_data_dict['chat_id'], user_data_dict['user_name'])
    ans.repeat_message_text(user_data_dict['chat_id'], user_data_dict['message_text'])