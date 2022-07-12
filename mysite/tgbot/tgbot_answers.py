import telepot

token = '5414010081:AAFHzRIjpEJK6UOVn7h_N7xKOMrXMUjxA8Q'
bot = telepot.Bot(token)


class Answers_class:
    def say_hello(self, chat_id, user_name):
        bot.sendMessage(chat_id, f'Слава Україні, {user_name}!')

    def repeat_message_text(self, chat_id, message_text):
        bot.sendMessage(chat_id, message_text)