import telepot

token = '5414010081:AAFHzRIjpEJK6UOVn7h_N7xKOMrXMUjxA8Q'
bot = telepot.Bot(token)
address = 'https://serene-reef-36940.herokuapp.com'

bot.deleteWebhook()
bot.setWebhook(f'{address}/oldman')