import telepot


class FileService_class:
    @staticmethod
    def downloadDocument(bot, file_id):
        bot.download_file(file_id, f'C:\\Users\\Admin\\PycharmProjects\\DocConverterBot'
                                   f'\\mysite\\tgbot\\commands_service\\downloads\\{file_id}.doc')