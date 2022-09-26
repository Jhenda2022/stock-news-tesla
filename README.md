# stock-news
Extracted stock data of TESLA using API.
Used list comprehension to determine yesterday's date and the day before yesterday's date.
Extracted closing stock prices for both yesterday and the day before yesterday from generated stock data, then computes the percentage increase or decrease.
If the increase is greater than 5%, data from news site is extracted using API.
The first three relevant news are sent to telegram using telegram bot to show possible reasons behind the increase of the stock price of TESLA.
