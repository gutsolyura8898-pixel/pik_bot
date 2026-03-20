import requests
from bs4 import BeautifulSoup
import time
import re

BOT_TOKEN = "8586891464:AAF0tZILu0kZ6-GNx9umDNE0VwcLRwCshs0"
CHAT_ID = "457933336"

URL = "https://www.pik.ru/commercial/947655"

def send_message(text):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })


def get_price():

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(URL, headers=headers)

    soup = BeautifulSoup(r.text, "html.parser")

    text = soup.get_text()

    price = re.search(r"\d[\d\s]+₽", text)

    if price:
        return price.group()

    return None


last_price = None

# сообщение при запуске
send_message("Бот запущен и проверяет цену")

while True:

    try:

        price = get_price()

        if price:

            print("Цена сейчас:", price)

            # отправляем цену в Telegram
            send_message(f"Актуальная цена: {price}")

            # уведомление если цена изменилась
            if last_price and price != last_price:
                send_message(f"⚠️ Цена изменилась: {last_price} → {price}")

            last_price = price

        else:
            print("Цена не найдена")

    except Exception as e:
        print("Ошибка:", e)

    time.sleep(600)