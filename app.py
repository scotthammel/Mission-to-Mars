# Use Flask to render a template, redirecting to another url, and creating a URL
from flask import Flask, render_template, redirect, url_for
# Use PyMongo to interact with our Mongo database
from flask_pymongo import PyMongo
# Use the scraping code, we will convert from Jupyter notebook to Python
import scraping

# Add the following to set up Flask
app = Flask(__name__)

# Tell Python how to connect to Mongo using PyMongo
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)

# Define the route for the HTML page
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)

# Add the next route and function to our code
# @app.route(“/scrape”) defines the route that Flask will be using
# route, “/scrape”, will run the function that we create just beneath it.
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return redirect('/', code=302)

if __name__ == "__main__":
   app.run()