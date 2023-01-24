import telepot

# here is master branch
token = '5414010081:AAFHzRIjpEJK6UOVn7h_N7xKOMrXMUjxA8Q'
bot = telepot.Bot(token)
address = 'https://347e-176-98-31-129.ngrok.io'

bot.deleteWebhook()
bot.setWebhook(f'{address}/oldman')