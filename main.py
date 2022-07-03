from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import pickle as pkl
import keras 
import tensorflow as tf
import numpy as np
from keras.preprocessing.sequence import pad_sequences
import nltk
import re
from nltk.corpus import wordnet as wn
import time

app = Flask(__name__)
CORS(app)

stop_words = set(nltk.corpus.stopwords.words('english'))
lemmatizer = nltk.stem.WordNetLemmatizer()
words = set(nltk.corpus.words.words())
adj_words = set([x for x in words if len(wn.synsets(x)) > 0 and wn.synsets(x)[0].pos() in ['n', 'v', 'a', 's']])

def clean_text(text):
  if type(text)!=str:
    return str(text)
  return re.sub(r'[^0-9A-Za-z" "]','',text)

def create_response(output, modelTime):

    percent_positive = int(output[0][0] * 100)
    
    response = {
        "status" : "success",
        "positive" : percent_positive,
        "negative" : 100 - percent_positive,
        "responseTime" : modelTime
    }
    return response
   
def predict_imdb_data(text):

    start = time.time()
    
    text = clean_text(text)
    text_to_array = []

    for word in text.split(" "):

        curword = word.lower().strip()
        curword = lemmatizer.lemmatize(curword)

        if curword in stop_words:
            continue

        if curword not in adj_words:
            continue

        if curword in word_index_imdb:
            text_to_array.append(word_index_imdb[curword])

        else:
            text_to_array.append(0)

    while len(text_to_array)<20:
        text_to_array.append(0)      

    text_to_array = text_to_array[:20]

    vectoredInput = [word_embeddings_imdb[x] for x in text_to_array]
    inp = np.array(vectoredInput)
    inp = np.reshape(inp, (1,20,50,1))
    out = imdb_model.predict(inp)

    end = time.time()

    return create_response(out, end - start)

def predict_twitter_data(text):

    start = time.time()

    text = clean_text(text)
    text_to_array = []
    
    for word in text.split(" "):

        curword = word.lower().strip()
        curword = lemmatizer.lemmatize(curword)

        if curword in stop_words:
            continue

        if curword not in words:
            continue

        if curword in word_index_twitter:
            text_to_array.append(word_index_twitter[curword])

        else:
            text_to_array.append(0)

    while len(text_to_array)<10:
        text_to_array.append(0)      

    text_to_array = text_to_array[:10]

    vectoredInput = [word_embeddings_twitter[x] for x in text_to_array]
    inp = np.array(vectoredInput)
    inp = np.reshape(inp, (1,10,30,1))
    out = twitter_model.predict(inp)

    end = time.time()

    return create_response(out, end - start)

@app.route('/')
def mainpage():
    return {"status" : "working"}

@app.route('/predict', methods=['POST'])
def calculate():
    
    failed_response = {"status" : "failed"}

    try:
        data = request.get_json(force=True)
    
        if data['model'] == "imdb" : 
            prediction = predict_imdb_data(data['text'])
            return jsonify(prediction)

        elif data['model'] == "twitter":
            prediction = predict_twitter_data(data['text'])
            return jsonify(prediction)

        else:
            return jsonify(failed_response)

        return jsonify(prediction) 
    
    except Exception as e:
        print(str(e))
        return jsonify(failed_response)

if __name__ == '__main__':
    
    imdb_model = pkl.load(open('save_model_imdb.pkl','rb'))
    word_embeddings_imdb = pkl.load(open('word_embeddings_imdb.pkl','rb'))
    word_index_imdb = pkl.load(open('word_index_imdb.pkl','rb'))

    twitter_model = pkl.load(open('save_model_twitter.pkl','rb'))
    word_embeddings_twitter = pkl.load(open('word_embeddings_twitter.pkl','rb'))
    word_index_twitter = pkl.load(open('word_index_twitter.pkl','rb'))
    
    app.run("0.0.0.0",5000)