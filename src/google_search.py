import requests
from bs4 import BeautifulSoup
import json
import os
from dotenv import load_dotenv
load_dotenv()
google_search_api_key = os.environ['GOOGLE_SEARCH_API_KEY']

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

def scrape(links):
    other_news = []
    for url in links:
        try:
            page= requests.get(url)
            if (page.status_code != 200):
                continue
            soup = BeautifulSoup(page.text, 'lxml')
            paragraphs = soup.find_all('p')
            texts=[]
            for i in range(len(paragraphs)):
                para = paragraphs[i].text
                texts.append(para)
            other_news.append(texts)
        except:
            continue

    return other_news

if __name__=="__main__":
    news = "IIT Kanpur develops artificial rain through cloud seeding technology"
    links = search(news)
    other_news = scrape(links)
    print(links)
