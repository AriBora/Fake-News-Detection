import requests
from bs4 import BeautifulSoup
import json
import os
import sys
from dotenv import load_dotenv
load_dotenv()
google_search_api_key = os.environ['GOOGLE_SEARCH_API_KEY']

from src.exception import CustomException
from src.logger import logging

url = "https://google.serper.dev/news"

def search(news):
    payload = json.dumps({"q": news,"gl": "in","num":10})
    headers = {'X-API-KEY': google_search_api_key,'Content-Type': 'application/json'}
    response = requests.request("POST", url, headers=headers, data=payload)

    res = response.json()
    n = res['news']
    links =[]
    for i in range(len(n)):
        links.append(n[i]['link'])

    return links

def scrape(news):
    # links = search(news)
    links = [
            'https://www.firstpost.com/explainers/delhi-air-quality-pollution-what-is-artificial-rain-iit-kanpur-cloud-seeding-13358812.html',
            'https://www.hindustantimes.com/india-news/iitkanpur-ready-to-tackle-delhi-ncr-air-pollution-with-artificial-rain-report-101699232424683.html',
            'https://english.jagran.com/india/artificial-rain-to-tackle-delhi-air-pollution-iit-kanpur-readies-quick-fix-for-choking-delhiites-what-is-cloud-seeding-explained-10112072',
            'https://www.ndtv.com/india-news/controlling-pollution-through-cloud-seeding-is-not-a-permanent-solution-says-iit-kanpur-professor-4559962',
            'https://www.thehindu.com/news/national/artificial-rain-to-fix-pollution-remains-a-nebulous-science/article67522010.ece',
            'https://timesofindia.indiatimes.com/city/delhi/delhi-to-explore-possibility-of-artificial-rain-rai/articleshow/105081890.cms',
            'https://timestech.in/using-of-artificial-rain/',
            'https://auto.economictimes.indiatimes.com/news/industry/odd-even-scheme-deferred-delhi-plans-cloud-seeding-ban-on-app-based-cabs-from-other-states-to-fight-smog/105082158',
            'https://www.indiatoday.in/education-today/news/story/artificial-rain-test-successful-in-iit-kanpur-2397097-2023-06-23',
            'https://indianexpress.com/article/cities/delhi/delhi-news-live-updates-pollution-aqi-arvind-kejriwal-mcd-9018341/']
    logging.info(f"Loaded all links. {len(links)} links found.")
    other_news = []

    for url in links:
        try:
            page= requests.get(url)
            logging.info(url)
            if (page.status_code != 200):
                logging.info("Page could not be loaded.")
                continue
            soup = BeautifulSoup(page.text, 'lxml')
            logging.info("Successfully loaded page.")
            paragraphs = soup.find_all('p')
            texts=[]
            for i in range(len(paragraphs)):
                para = paragraphs[i].text
                texts.append(para)
            new_text = ' '
            new_text = new_text.join(texts)
            other_news.append(new_text)
        except Exception as e:
            raise CustomException(e, sys)
    return other_news

if __name__=="__main__":
    news = "IIT Kanpur develops artificial rain through cloud seeding technology"
    links = search(news)
    other_news = scrape(links)
    print(links)
