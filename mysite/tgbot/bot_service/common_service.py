import telepot

from . import answers, extract_data, file_service, commands_executor, auxiliary_stuff
import json
from start import bot


Answers = answers.Answers_class()
DataExtractor = extract_data.DataExtractor_class()
FileService = file_service.FileService_class()
CommandsExecutor = commands_executor.Commands_executor()

Message_Type = auxiliary_stuff.Message_Type


def execute_command(request_body):
    FileService.save_to_json(request_body)
    FileService.clean_data_file()
    chat_id, user_name = DataExtractor.get_chatID_and_username(request_body)

    if DataExtractor.detect_message_type(request_body) == Message_Type.text:
        CommandsExecutor.execute_text_command(request_body)
    elif DataExtractor.detect_message_type(request_body) == Message_Type.callback_query:
        CommandsExecutor.execute_callback_command(request_body)
    elif DataExtractor.detect_message_type(request_body) == Message_Type.image:
        Answers.inline_keyboard_after_receiving_default_photos(chat_id)







