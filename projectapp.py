# Necessary Imports


from logger import Lg
from MongoDB_file import MongoDBconnect
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
from sitescrapped_data import Sitescrapper

app = Flask(__name__) #Initializing flask app with name app

logger = Lg('flasklog').getlog()

@app.route('/', methods=['GET']) #route with allowed methods GET
@cross_origin()
def homepage():
    """Function that renders homepage"""
    return render_template("index.html")

@app.route('/scrap', methods=['POST', 'GET']) #route with allowed methods POST & GET
@cross_origin()
def index():
    if request.method == 'POST':
        try:
            search_input = request.form['content'].replace(" ", "")
            client = MongoDBconnect(username='manjunath',password='manjunath')
            logger.info("MongoDB Connection Established")
            if client.iscollectionpresent(db_name='INSprojectDB', collection_name='scrapped_data'):
                response = client.findallrecords(db_name='INSprojectDB', collection_name='scrapped_data')
                responses = [i for i in response]
                logger.info("Database and Collection Exists")
                return render_template("results.html", output_data=responses)
            else:
                sitescrapper = Sitescrapper("https://courses.ineuron.ai/")
                course_details = sitescrapper.course_details()
                client.createcollection(db_name='INSprojectDB', collection_name='scrapped_data')
                client.insertrecords(db_name='INSprojectDB', collection_name='scrapped_data', records=course_details)
                logger.info("Data Inserted into MongoDB successfully")
                return render_template("results.html", output_data=course_details)

        except Exception as e:
            logger.error("(index()) Error occurred" + str(e))

    else:
        return render_template("index.html")

if __name__ == "__main__":
    app.run(port=8000, debug=True)
    # app.run(debug=True)
