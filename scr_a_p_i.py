#!/usr/bin/env python

# Dependencies and packages.
import pandas as pd
import json
from IPython.display import HTML
from food_scrape import scrape_food
from flask import Flask, render_template
from datetime import datetime

app = Flask(__name__)

# Home
@app.route("/")
def hello():
    return render_template('index.html', timestamp=datetime.now())

@app.route("/scrape")
def scrape():
    call_func = scrape_food()
    scraped_food = pd.DataFrame.to_dict(call_func)
    with open('scrape_storage.json', 'w') as jpath:
        json.dump(scraped_food, jpath)
    return render_template('scrape.html')
    
@app.route("/all")
def all():
    with open('scrape_storage.json', 'r') as jr:
        data = json.load(jr)
        scrape_df = pd.DataFrame(data)
        html_table = HTML(scrape_df.to_html(justify='center', classes='table table-striped', index=False))
    return render_template('all_data.html', data = html_table)

if __name__ == "__main__":
    app.run(debug=True)