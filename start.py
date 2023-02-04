import telepot
import dotenv

# here is dev branch
dotenv.load_dotenv()
bot = telepot.Bot(dotenv.dotenv_values('.env')['TOKEN'])
address = 'some_address'

bot.deleteWebhook()
bot.setWebhook(f'{address}/oldman')