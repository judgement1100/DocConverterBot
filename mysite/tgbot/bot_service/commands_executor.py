from . import answers, extract_data, file_service


FileService = file_service.FileService_class()
Answers = answers.Answers_class()
DataExtractor = extract_data.DataExtractor_class()


class Commands_executor:

    def execute_text_command(self, request_body):
        chat_id = DataExtractor.get_chat_id(request_body)
        user_name = DataExtractor.get_user_name(request_body)
        messageText = DataExtractor.get_message_text(request_body)

        if messageText == '/help':
            Answers.send_help_list(chat_id)

        elif messageText == '/start':
            Answers.send_message(chat_id, "Вітаю! Оберіть команду із списку в меню.")

        elif messageText == '/create_pdf':
            Answers.send_message(chat_id, 'Сеанс створення pdf відкрито. Надішліть фото')
            Answers.keyboard_while_session_opened(chat_id)


    def execute_callback_command(self, request_body):
        chat_id = DataExtractor.get_chat_id_from_callback(request_body)
        user_name = DataExtractor.get_user_name_from_callback(request_body)
        callback_data = DataExtractor.get_callback_data(request_body)

        if callback_data == 'create_new_pdf_with_automatic_name':
            Answers.delete_inline_keyboard(chat_id, 'Creating autonamed pdf') #TODO

        elif callback_data == 'receiving_pdf_name':
            Answers.send_message(chat_id, 'Як назвати pdf?')













