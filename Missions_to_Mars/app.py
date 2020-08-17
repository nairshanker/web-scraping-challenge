from flask import Flask, render_template

# Import our pymongo library, which lets us connect our Flask app to our Mongo database.
import pymongo
import scrape_mars

# Create an instance of our Flask app.
app = Flask(__name__)

# Create connection variable
conn = 'mongodb://localhost:27017'

# Pass connection to the pymongo instance.
client = pymongo.MongoClient(conn)

# Set route
@app.route('/')
def index():
    mars = client.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():
    mars = client.db.mars

    mars_data = scrape_mars.scrape_all()

    mars.update({},mars_data,upsert = True)
    return "Scraping successful"




if __name__ == "__main__":
    app.run(debug=True)
