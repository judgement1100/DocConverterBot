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

        elif messageText == '/images_to_pdf':
            Answers.send_message(chat_id, "Сеанс створення pdf відкрито. Надішліть фото")

        elif messageText == '/create':
            Answers.send_message(chat_id, "Створюється pdf...")
            FileService.process_creating_pdf_from_images(chat_id, user_name)
            Answers.send_message(chat_id, "Натисніть /end_session для завершення сеансу")

        elif messageText == '/end_session':
            Answers.send_message(chat_id, "Сеанс створення pdf закрито.")

        elif messageText == '/rename_pdf':
            Answers.send_message(chat_id, "Надішліть pdf-файл")

        elif messageText is not DataExtractor.is_command(messageText):
            Answers.send_message(chat_id, 'hi')
            file_name, file_id = DataExtractor.find_last_document(request_body)
            Answers.send_message(chat_id, 'succeed')
            Answers.send_message(chat_id, file_name)
            Answers.send_message(chat_id, file_id)
            # zip_path, zipObj = FileService.download_document(file_id, messageText)
            # Answers.send_document(chat_id, messageText, zipObj)




