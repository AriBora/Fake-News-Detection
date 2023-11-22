from flask import Flask,request,render_template
from src.google_search import scrape
from src.get_named_entity import get_important_texts
from src.calc_similiarity import calculate_similarity
from src.logger import logging

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/check_news',methods=['GET','POST'])
def check_news():
    if request.method == 'GET':
        return render_template('home.html')
    
    news = request.form.get('searchInput')
    logging.info(f"Collected news: {news}")

    related_news = scrape(news)
    logging.info(f"Scraped all links. {len(related_news)} links could be scraped.")
    imp_news = get_important_texts(related_news, news)
    result = calculate_similarity(news, imp_news)
    # result = []
    # for i in range(len(related_news)):
    #     result.append([i+1,related_news[i]])
    return render_template('home.html', results=result)


if __name__=="__main__":
    app.run(host="0.0.0.0",port='8000',debug=True)