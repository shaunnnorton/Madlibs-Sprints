from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/madlibsdb"
mongo = PyMongo(app)
'''mongo.db.madlibs.insert_one({
    'theme':'animals',
    'length':'short',
    'answers':['adjective','animal','animal','noun','adjective','noun','adjective','adjective','noun'],
    'text':f"Camping is {0}. You might see {1} and {2}. The food which is cooked over the {3} is very {4}.                 The best part of camping is using the {5} which is very {6}. At night, the tent is extreamly {7}. It's always best to take a {8} camping with you."
})'''
@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/Create/Classic')
def classicCreate():
    theme = request.args.get('theme')
    length = request.args.get('length')
    if theme and length:
        madlib_results = mongo.db.madlibs.find_one({'theme':theme,'length':length})
    else:
        madlib_results = {'answers':[]}
    context = {
        'answers': madlib_results['answers']

    }
    
    return render_template('classic-create.html', **context)


if __name__ == "__main__":
    app.run(debug=True)