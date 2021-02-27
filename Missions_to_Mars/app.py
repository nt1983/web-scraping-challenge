from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/Mars_DB")

 #Route to render index.html template using data from Mongo
@app.route("/")
def home():
    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()
    return render_template("index.html", mars=mars_dict)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    mars_dict=mongo.db.mars_dict
    mdata=scrape_mars.scrape()
    mars_dict.update({}, mdata, upsert=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)






