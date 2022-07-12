import telepot

token = '5414010081:AAFHzRIjpEJK6UOVn7h_N7xKOMrXMUjxA8Q'
bot = telepot.Bot(token)


class Answers_class:
    @staticmethod
    def say_hello(chat_id, user_name):
        bot.sendMessage(chat_id, f'Слава Україні, {user_name}!')

    @staticmethod
    def send_message(chat_id, message_text):
        bot.sendMessage(chat_id, message_text)