import telepot

token = '5414010081:AAFHzRIjpEJK6UOVn7h_N7xKOMrXMUjxA8Q'
bot = telepot.Bot(token)
address = 'https://6a0a-176-98-31-129.ngrok.io'

bot.deleteWebhook()
bot.setWebhook(f'{address}/oldman')