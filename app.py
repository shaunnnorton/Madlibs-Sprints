from flask import Flask, request, render_template
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/madlibsdb"
mongo = PyMongo(app)
'''mongo.db.madlibs_image.insert_one({
    'theme':'animals',
    'length':'long',
    'answers':['adjective','animal','animal-2','noun','adjective-2','noun-2','adjective-3','adjective-4','noun-3'],
    'text':"Camping is {0}. You might see {1} and {2}. The food which is cooked over the {3} is very {4}.                 The best part of camping is using the {5} which is very {6}. At night, the tent is extreamly {{7}}. It's always best to take a {8} camping with you."
})'''
@app.route('/')
def homepage():
    return render_template("home.html")

@app.route('/Create/Classic')
def classicCreate():
    theme = request.args.get('theme')
    length = request.args.get('length')
    if theme and length:
        madlib_results = mongo.db.madlibs_classic.find_one({'theme':theme,'length':length})
    else:
        madlib_results = {'answers':[]}
    context = {
        'answers': madlib_results['answers'],
        'theme':theme,
        'length':length
    }  
    return render_template('classic-create.html', **context)

@app.route('/Classic')
def finishedClassic():
    results = []
    for result in request.args:
        results.append(request.args.get(result))
    madlib_text_raw = mongo.db.madlibs_classic.find_one({'theme':request.args.get('theme'),'length':request.args.get('length')})['text']
    madlib_text = ''
    current_result = 0 
    for result in results:
        madlib_text_raw = madlib_text_raw.replace(f'{{{current_result}}}',result)
        current_result+=1
    context = {
        
        'madlib':madlib_text_raw,
        'results':results
    }
    return render_template('classic-completed.html',**context)

@app.route('/Create/Image')
def imageCreate():
    theme = request.args.get('theme')
    length = request.args.get('length')
    if theme and length:
        madlib_results = mongo.db.madlibs_image.find_one({'theme':theme,'length':length})
    else:
        madlib_results = {'answers':[]}
    context = {
        'answers': madlib_results['answers'],
        'theme':theme,
        'length':length
    }  
    return render_template('image-create.html', **context)


@app.route('/Image')
def finishedImage():
    results = []
    for result in request.args:
        results.append(request.args.get(result))
    madlib_text_raw = mongo.db.madlibs_image.find_one({'theme':request.args.get('theme'),'length':request.args.get('length')})['text']
    madlib_text_split = madlib_text_raw.split()
    print(madlib_text_split)
    current_result = 0 
    for result in results:
        if current_result >= len(results)-2:
            break
        index_of_result = madlib_text_split.index(f'{{{current_result}}}')
        madlib_text_split[index_of_result] = result
        
        
        current_result+=1
    print(madlib_text_split)
    context = {
        
        'madlib':madlib_text_split,
        'results':results
    }
    return render_template('image-completed.html',**context)



if __name__ == "__main__":
    app.run(debug=True)