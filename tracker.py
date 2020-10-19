from datetime import datetime
import requests
from bs4 import BeautifulSoup as bs
import telegram
from dotenv import load_dotenv
import os
import time

load_dotenv()

PERSONAL_ID = os.getenv("PERSONAL_ID")
PASSWORD = os.getenv("PASSWORD")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
bot = telegram.Bot(token=TELEGRAM_TOKEN)

url = "https://track.ucas.com/"
login_data = {
	'PersonalId': PERSONAL_ID,
	'Password': PASSWORD,
}


def send_message(text):
	return bot.send_message(chat_id=CHAT_ID, text=text)


def main():
	send_message("The bot's up and running, waiting for an update from UCAS.")
	while True:
		try:
			with requests.Session() as s:
				today = datetime.now().strftime("%d %B %Y")
				response = s.get(url)
				login_content = bs(response.content, 'html.parser')
				token = login_content.find("input", {"name": "__RequestVerificationToken"})
				login_data["__RequestVerificationToken"] = token["value"]

				response = s.post(url, data=login_data)
				track_page = bs(response.content, 'html.parser')
				update = track_page.find("h2", string="Latest update")
				date = update.parent.find("p").get_text().split(',')[0]

				if date == today:
					message = update.parent.findAll("p")[1]
					send_message("Update to UCAS profile!" + "\n" + message.get_text())
				time.sleep(1500)
		except Exception as e:
			send_message(f"Bot's down with such error: {e}")
			time.sleep(5)
			continue


if __name__ == "__main__":
	main()
