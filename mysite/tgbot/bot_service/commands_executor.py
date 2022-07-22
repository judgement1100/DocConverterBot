from . import answers, extract_data, file_service, auxiliary_stuff
import os
from start import bot


Extensions = auxiliary_stuff.Extensions
FileService = file_service.FileService_class()
Answers = answers.Answers_class()
DataExtractor = extract_data.DataExtractor_class()

KeyboardStatus = auxiliary_stuff.InlineKeyboard_Status


class Commands_executor:

    def process_creating_pdf_from_images(self, chat_id, user_name):
        try:
            photos_list = FileService.download_images(user_name)
            if len(photos_list) > 0:
                pdf_path = FileService.create_pdf_from_images(photos_list)
                zip_path, zipObj = FileService.push_into_zip(pdf_path)
                Answers.send_document(chat_id, 'file.pdf', zipObj)

                zipObj.close()
                os.remove(zip_path)
                os.remove(pdf_path)
                for i in range(0, len(photos_list)):
                    os.remove(photos_list[i])
            else:
                Answers.send_message(chat_id, "Помилка. Можливо, ви не надіслали фото")
        except Exception as e:
            print("Error occured in function <process_creating_pdf_from_images>\n" + str(e))


    def process_convertation_secondary_commands(self, chat_id, user_name):
        if DataExtractor.find_last_command(user_name) == f'/{Extensions.pdf.name}':
            file_name, file_id = DataExtractor.find_last_document(user_name)
            Answers.send_message(chat_id, f'Опрацьовується документ <{file_name}>. Нове розширення - .pdf')
            FileService.process_document(file_name, file_id, chat_id, Extensions.pdf)

        elif DataExtractor.find_last_command(user_name) == f'/{Extensions.doc.name}':
            file_name, file_id = DataExtractor.find_last_document(user_name)
            Answers.send_message(chat_id, f'Опрацьовується документ <{file_name}>. Нове розширення - .doc')
            FileService.process_document(file_name, file_id, chat_id, Extensions.doc)

        elif DataExtractor.find_last_command(user_name) == f'/{Extensions.txt.name}':
            file_name, file_id = DataExtractor.find_last_document(user_name)
            Answers.send_message(chat_id, f'Опрацьовується документ <{file_name}>. Нове розширення - .txt')
            FileService.process_document(file_name, file_id, chat_id, Extensions.txt)

        elif DataExtractor.find_last_command(user_name) == f'/{Extensions.fb2.name}':
            file_name, file_id = DataExtractor.find_last_document(user_name)
            Answers.send_message(chat_id, f'Опрацьовується документ <{file_name}>. Нове розширення - .fb2')
            FileService.process_document(file_name, file_id, chat_id, Extensions.fb2)


    def execute_text_command(self, request_body):
        chat_id = DataExtractor.get_chat_id(request_body)
        user_name = DataExtractor.get_user_name(request_body)

        # Main commands:
        if DataExtractor.get_message_text(request_body) == '/images_to_pdf' or \
                DataExtractor.get_message_text(request_body) == '/convert_document' or \
                DataExtractor.get_message_text(request_body) == '/help' or \
                DataExtractor.get_message_text(request_body) == '/start':

            if DataExtractor.get_message_text(request_body) == '/images_to_pdf':
                Answers.send_message(chat_id, "Надішліть фото")

            elif DataExtractor.get_message_text(request_body) == '/convert_document':
                Answers.send_message(chat_id, "Надішліть документ")

            elif DataExtractor.get_message_text(request_body) == '/help':
                Answers.send_message(chat_id,
                                     "Опис команд:\n"
                                     "1) /images_to_pdf: конвертація стиснених і нестиснених фотографій у pdf файл.\n"
                                     "У разі недотримання вказівок, які надає бот, існує ймовірність отримати непогану таку дулю у відповідь.\n"
                                     "2) /convert_document: конвертація текстових файлів у одне з наступних розширень:\n"
                                     ".pdf, .doc, .txt, .fb2, .epub, .mobi.\n"
                                     "Зауваження про дулю досі актуальне.\n\n"
                                     "Порядок виконання дій:\n"
                                     "1) Оберіть команду серед запропонованих у списку\n"
                                     "2) Робіть, що вказано в інструкції  ͡° ͜ʖ ͡°")

            elif DataExtractor.get_message_text(request_body) == '/start':
                Answers.send_message(chat_id, "Вітаю! Оберіть команду із списку.\n"
                                              "/images_to_pdf - створити pdf із фото\n"
                                              "/convert_document - конвертація документа\n"
                                              "/help - додаткова інформація.")

        # Secondary commands:
        else:
            if DataExtractor.get_message_text(request_body) == '/end':
                Answers.send_message(chat_id, "Створюється pdf...")
                Commands_executor.process_creating_pdf_from_images(chat_id, user_name)

            else:
                Commands_executor.process_convertation_secondary_commands(chat_id, user_name)


    def process_document(self, file_name, file_id, chat_id, new_extension: Extensions):
        new_extension = f'.{new_extension.name}'

        try:
            file_path = FileService.download_document(file_id, file_name)

            new_file_path = FileService.convert(new_extension, file_path)
            zip_path, zipObj = FileService.push_into_zip(new_file_path)

            new_file_name = os.path.splitext(file_name)[0] + new_extension
            Answers.send_document(chat_id, new_file_name, zipObj)

            os.remove(file_path)
            zipObj.close()
            os.remove(zip_path)

            if file_path != new_file_path:
                os.remove(new_file_path)

        except Exception as e:
            print(f'{str(e)}')
            Answers.send_message(chat_id, 'Виникла помилка :(')
            Answers.send_дуля(chat_id)
            os.remove(file_path)


    def execute_callback(self, request_body):
        query_id = DataExtractor.get_callback_query_id(request_body)
        chat_id, user_name = DataExtractor.get_chatID_and_username(request_body)

        if DataExtractor.get_callback_data(request_body) == "images_to_pdf":
            Answers.send_message(chat_id, "Сеанс створення pdf відкрито. Надішліть фото")

        elif DataExtractor.get_callback_data(request_body) == "convert_document":
            Answers.send_дуля(chat_id)

        elif DataExtractor.get_callback_data(request_body) == "end":
            Answers.send_message(chat_id, "Створюється pdf...")
            self.process_creating_pdf_from_images(chat_id, user_name)
            Answers.reply_with_inline_keyboard(chat_id, "Що робимо далі?", KeyboardStatus.after_end)

        elif DataExtractor.get_callback_data(request_body) == "continue_creating_pdf":
            Answers.send_message(chat_id, "Сеанс створення pdf продовжено. Надішліть фото")

        elif DataExtractor.get_callback_data(request_body) == "finish_creating_pdf":
            Answers.send_message(chat_id, "Сеанс створення pdf завершено.")
            Answers.reply_with_inline_keyboard(chat_id, "Оберіть одну із наступних команд:", KeyboardStatus.initial)

        bot.answerCallbackQuery(callback_query_id=query_id)