from . import answers, extract_data, file_service, commands_executor, auxiliary_stuff
import json


Answers = answers.Answers_class()
DataExtractor = extract_data.DataExtractor_class()
FileService = file_service.FileService_class()
CommandsExecutor = commands_executor.Commands_executor()

Message_Type = auxiliary_stuff.Message_Type
KeyboardStatus = auxiliary_stuff.InlineKeyboard_Status


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

        if DataExtractor.get_message_text(request_body) == '/show_commands':
            Answers.reply_with_inline_keyboard(chat_id, "Оберіть одну із наступних команд:", KeyboardStatus.initial)

        elif DataExtractor.get_message_text(request_body) == '/start':
            Answers.reply_with_inline_keyboard(chat_id, "Оберіть одну із наступних команд:", KeyboardStatus.initial)

        elif DataExtractor.get_message_text(request_body) == '/help':
            Answers.send_help_list(chat_id)
            Answers.reply_with_inline_keyboard(chat_id, "Оберіть одну із наступних команд:", KeyboardStatus.initial)

    elif DataExtractor.detect_message_type(request_body) == Message_Type.image:
        if need_asking(user_name):
            Answers.reply_with_inline_keyboard(chat_id, "Створити pdf?", KeyboardStatus.asking_for_end)

    elif DataExtractor.detect_message_type(request_body) == Message_Type.compressed_image:
        if need_asking(user_name):
            Answers.reply_with_inline_keyboard(chat_id, "Виявлено стиснені фото. Створити pdf?", KeyboardStatus.asking_for_end)

    elif DataExtractor.detect_message_type(request_body) == Message_Type.callback_query:
        CommandsExecutor.execute_callback(request_body)