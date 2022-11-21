import requests
from twilio.rest import Client

# ------------------- Twilio Info -------------------
# Enter your info here!!!
account_sid = ""
auth_token = ""
twilio_number = ""
personal_number = ""

# ------------------- Choose Stock -------------------
STOCK = "TSLA"
COMPANY_NAME = "Tesla"

# ------------------- Retrieve Stock Data -------------------
av_api_key = 'Y8I9YRJW55WITA96'
av_url = ("https://www.alphavantage.co/query?"
          "function=TIME_SERIES_DAILY_ADJUSTED&"
          f"symbol={STOCK}&"
          f"apikey={av_api_key}")
av_r = requests.get(av_url)
av_data = av_r.json()['Time Series (Daily)']

recent_close = float(list(av_data.values())[0]['4. close'])
recent_date = list(av_data.items())[0][0]
second_close = float(list(av_data.values())[1]['4. close'])
delta = (recent_close-second_close)/second_close * 100

# ------------------- Retrieve News Data -------------------
news_api_key = "412ede77796f4e378d7b65642e3682c5"
news_url = ('https://newsapi.org/v2/everything?'
            f'q={COMPANY_NAME}&'
            f'from={recent_date}&'
            'sortBy=popularity&'
            f'apiKey={news_api_key}')
news_r = requests.get(news_url)
news_data = news_r.json()['articles']
message = ""
for i in range(3):
    message += (f"{news_data[i]['title']}\n"
               f"{news_data[i]['url']}\n\n"
                )

# ------------------- Decide Whether to Send Message -------------------
sign = ""
if delta > 0:
    sign = "⬆️"
else:
    sign = "⬇️"

if abs(delta) > 1:
    client = Client(account_sid, auth_token)
    message = client.messages \
        .create(
            body=(f"{STOCK}: {sign}{abs(round(delta, 2))}\n\n"
                  f"{message}"),
            from_=twilio_number,
            to=personal_number
        )
    print(message.status)
