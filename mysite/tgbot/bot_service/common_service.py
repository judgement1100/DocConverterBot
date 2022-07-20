from . import answers, extract_data, file_service, commands_executor, auxiliary_stuff
import json


Message_Type = auxiliary_stuff.Message_Type
Answers = answers.Answers_class()
DataExtractor = extract_data.DataExtractor_class()
FileService = file_service.FileService_class()
CommandsExecutor = commands_executor.Commands_executor()


def need_asking(user_name):
    import datetime

    with open('mysite\\tgbot\\bot_service\\downloads\\data.json', 'r') as rd:
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
    FileService.save_to_json(request_body)
    FileService.clean_data_file()
    chat_id, user_name = DataExtractor.get_chatID_and_username(request_body)

    if DataExtractor.detect_message_type(request_body) == Message_Type.text:
        Answers.reply_with_inline_keyboard(chat_id)

    elif DataExtractor.detect_message_type(request_body) == Message_Type.callback_query:
        CommandsExecutor.execute_callback(request_body)




