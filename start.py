import telepot

token = '5414010081:AAFHzRIjpEJK6UOVn7h_N7xKOMrXMUjxA8Q'
bot = telepot.Bot(token)

address = 'https://7939-176-98-25-131.ngrok.io'
bot.deleteWebhook()
bot.setWebhook(f'{address}/oldman/ex1')