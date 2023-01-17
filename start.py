import telepot

# here is dev branch
token = '5414010081:AAFHzRIjpEJK6UOVn7h_N7xKOMrXMUjxA8Q'
bot = telepot.Bot(token)
address = 'https://2cc6-176-98-8-129.ngrok.io'
# asdfasf

bot.deleteWebhook()
bot.setWebhook(f'{address}/oldman')