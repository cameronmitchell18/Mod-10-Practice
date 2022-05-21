from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
from pymongo import MongoClient
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection 

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'

@app.route('/')

def index():

    mars = MongoClient.db.mars.find_one()

    return render_template('index.html' , mars=mars)

@app.route('/scrape')

def scrape():

    mars = MongoClient.db.mars

    mars_data = scraping.scrape_all()

    mars.update_one({} , {"$set":mars_data} , upsert = True)

    return redirect('/', code=302)

if __name__ == '__main__':

    app.run()