from telebot import TeleBot, types
from keys import BOT_TOKEN
from weather import get_weather, get_location_weather

city = 'Saint Petersburg'
with open('city.txt') as city_file:
    city = city_file.read()

def update_city(new_city):
    global city
    with open('city.txt', 'w') as city_file:
        city_file.write(new_city)
    city = new_city

bot = TeleBot(BOT_TOKEN, parse_mode='html')
sending_city = False

welcome_message = """Hello, my name is <u>Weatel</u> (/vˈætəl/) - weather Telegram bot 🌤. \n• I will help you to get desirable <b>weather information</b>, including: temperature 🌡, humidity and pressure by typing /weather 🌩. \n• By default weather city name is "Saint Petersburg" but you can change using /setcity command and the name of the city. \n• Send me a geographic location (Telegram -> Add -> Location) 🌍 or allow me use yours 🏠 and you will receive the most precise weather data ⭐️. \n• You can also use me in-line , from the input key wield by typing @weatelbot space <i>city name</i> 🗺."""

@bot.message_handler(commands=['start'])
def start(mes):
    bot.send_message(mes.chat.id, welcome_message)

@bot.message_handler(commands=['weather'])
def send_weather(mes):
    ''' Send weather to the user on /weather command.
    '''
    bot.send_message(mes.chat.id, get_weather(city))

@bot.message_handler(commands=['setcity'])
def set_city(mes):
    ''' Sets the default city name to search by /weather. 
    '''
    global sending_city
    bot.send_message(mes.chat.id, 'Send me new default city:')
    sending_city = True

@bot.message_handler(func=lambda q: globals()['sending_city'])
def get_sent_city(mes):
    update_city(mes.text)
    bot.send_message(mes.chat.id, 'Default weather city successfully changed to ' + mes.text + '.')

@bot.message_handler(content_types=['location'])
def send_localtion_weather(mes):
    ''' Send weather information based on the user-sent location.
    '''
    lon = mes.location.longitude
    lat = mes.location.latitude
    weather = get_location_weather(lon, lat)
    bot.send_message(mes.chat.id, weather)

@bot.inline_handler(func=lambda q: q.query == '')
def inline_weather(inline_query):
    ''' Send default city weather information when no city is provided. 
    '''
    weather = get_weather(inline_query.query)
    if weather == 'City not found':
        return
    weather_result = types.InlineQueryResultArticle('1', 'Weather for ' + str(city), input_message_content=types.InputTextMessageContent(weather))
    bot.answer_inline_query(inline_query.id, [weather_result])

@bot.inline_handler(func=lambda q: q.query != '')
def inline_city_weather(inline_query):
    ''' Send weather information of the entered city.
    '''
    weather = get_weather(inline_query.query)
    if weather == 'City not found':
        return
    weather_result = types.InlineQueryResultArticle('1', 'Weather for ' + str(inline_query.query), input_message_content=types.InputTextMessageContent(weather))
    bot.answer_inline_query(inline_query.id, [weather_result])

if __name__ == '__main__':
    bot.infinity_polling()
