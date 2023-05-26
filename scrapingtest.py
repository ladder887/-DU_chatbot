import requests
from bs4 import BeautifulSoup

url = "https://comic.naver.com/webtoon/weekday"
response = requests.get(url)
response.raise_for_status()

soup = BeautifulSoup(response.text, "lxml")

print(soup.title)
