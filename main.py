import requests
import os

#_________________FUNCTIONS________________________________#
def telegram_bot_sendtext(bot_message):
    '''Sends message through TG.'''
    bot_token = os.environ["BOT_TOKEN"]
    bot_chatID = os.environ["BOT_CHAT_ID"]
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
STOCK_API_KEY = os.environ["STOCK_API_KEY"]

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = os.environ["NEWS_API_KEY"]

#___________________STOCK API____________________#
stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
stock_data_list = [value for (key, value) in stock_data.items()]

#Compare yesterday and day_before_yesterday's closing prices.
closing_price_yesterday = float(stock_data_list[0]["4. close"])
closing_price_dby = float(stock_data_list[1]["4. close"])
difference = closing_price_yesterday - closing_price_dby
percentage = abs(round((difference/closing_price_yesterday) * 100))

#If increase is greater than 5%, load news data.
news_parameters = {
    "q": "tesla",
    "apiKey": NEWS_API_KEY,
}

if percentage > 5:
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response.raise_for_status()
    news_data = response.json()
    news_slice = news_data["articles"][:3]
    for news in news_slice:
        sym = symbol(difference)
        telegram_bot_sendtext(f"{STOCK_NAME}: {sym}{percentage}%\nHeadline: {news['title']}\n Brief: {news['description']}")