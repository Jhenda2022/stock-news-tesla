import requests
import datetime

#_________________FUNCTIONS________________________________#
def telegram_bot_sendtext(bot_message):
    '''Sends message through TG.'''
    bot_token = '5740117726:AAEPxOKvfD_cYIwLc6H0RjsWUfazcXz3-jo'
    bot_chatID = '5506904417'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + \
                '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def symbol(difference):
    if difference > 0:
        return "🔺"
    return "🔻"

#________________GLOBAL VARIABLES____________________________#
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "UQODA4DL3J37VEV1"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "6e8838559f86468aa8f174284b32a8a3"

#___________________STOCK API____________________#
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()

#Compare yesterday and day_before_yesterday's closing prices.
today = datetime.date.today()
yesterday = str(today - datetime.timedelta(days=1))
closing_price_yesterday = float(stock_data["Time Series (Daily)"][yesterday]["4. close"])

day_before_yesterday = str(today - datetime.timedelta(days=2))
closing_price_dby = float(stock_data["Time Series (Daily)"][day_before_yesterday]["4. close"])

difference = closing_price_yesterday - closing_price_dby
percentage = abs(int((difference/closing_price_yesterday) * 100))
print(percentage)

#If increase is greater than 5%, load news data.
news_parameters = {
    "q": "tesla",
    "apiKey": NEWS_API_KEY,
}

response = requests.get(NEWS_ENDPOINT, params=news_parameters)
response.raise_for_status()
news_data = response.json()
news_slice = news_data["articles"][:3]
for news in news_slice:
    sym = symbol(difference)
    telegram_bot_sendtext(f"TSLA: {sym}{percentage}%\nHeadline: {news['title']}\n Brief: {news['description']}")


