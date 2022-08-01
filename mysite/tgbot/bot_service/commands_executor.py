from . import answers, extract_data, file_service, auxiliary_stuff
import os
from start import bot


Extensions = auxiliary_stuff.Extensions
FileService = file_service.FileService_class()
Answers = answers.Answers_class()
DataExtractor = extract_data.DataExtractor_class()

KeyboardStatus = auxiliary_stuff.InlineKeyboard_Status


class Commands_executor:

    def process_convertation_secondary_commands(self, chat_id, user_name):

        # fb2
        if DataExtractor.find_last_command(user_name) == f'/{Extensions.fb2.name}':
            file_name, file_id = DataExtractor.find_last_document(user_name)
            prev_extension = FileService.get_document_extension(file_name)
            FileService.process_document(file_name, file_id, chat_id, prev_extension, Extensions.fb2)


    def execute_text_command(self, request_body):
        chat_id = DataExtractor.get_chat_id(request_body)
        user_name = DataExtractor.get_user_name(request_body)

        # Main commands:
        if DataExtractor.get_message_text(request_body) == '/images_to_pdf':
            Answers.send_message(chat_id, "Сеанс створення pdf відкрито. Надішліть фото")

        elif DataExtractor.get_message_text(request_body) == '/convert_document':
            Answers.send_message(chat_id, "Надішліть текстовий документ")

        elif DataExtractor.get_message_text(request_body) == '/help':
            Answers.send_help_list(chat_id)

        elif DataExtractor.get_message_text(request_body) == '/start':
            Answers.send_message(chat_id, "Вітаю! Оберіть команду із списку в меню.")

        # Secondary commands:
        if DataExtractor.get_message_text(request_body) == '/end':
            Answers.send_message(chat_id, "Створюється pdf...")
            FileService.process_creating_pdf_from_images(chat_id, user_name)
            Answers.reply_with_inline_keyboard(chat_id, "Що робимо далі?", KeyboardStatus.after_end)

        elif DataExtractor.get_message_text(request_body) == '/fb2':
            self.process_convertation_secondary_commands(chat_id, user_name)


    def execute_callback(self, request_body):
        query_id = DataExtractor.get_callback_query_id(request_body)
        chat_id, user_name = DataExtractor.get_chatID_and_username(request_body)

        if DataExtractor.get_callback_data(request_body) == "continue_creating_pdf":
            Answers.send_message(chat_id, "Сеанс створення pdf продовжено. Надішліть фото")

        elif DataExtractor.get_callback_data(request_body) == "images_to_pdf":
            Answers.send_message(chat_id, "Сеанс створення pdf відкрито. Надішліть фото")

        elif DataExtractor.get_callback_data(request_body) == "finish_creating_pdf":
            Answers.send_message(chat_id, "Сеанс створення pdf завершено.")

        bot.answerCallbackQuery(callback_query_id=query_id)