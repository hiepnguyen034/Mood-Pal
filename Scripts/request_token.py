from flask import Flask, request, url_for, redirect
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
from bs4 import BeautifulSoup
import requests
import pprint
import re
import json
import urllib
import os
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import time
model_LSTM = load_model('my_model.h5')

with open('tokenizer.pickle', 'rb') as handle:
    tok = pickle.load(handle)

app = Flask("mood_model")
access_token = 'failed'
user = 'failed'

app = Flask("mood_model")

@app.route('/', methods=("POST", "GET"))
def model():
    global access_token
    global user
    if request.method == "POST":
        access_token = request.form['token']
        user = request.form['user']




    #return access_token

def get_message(user,token):
    url = 'https://graph.facebook.com/'+user+ '?fields=feed{message}&access_token='+ token
    htmlContent = requests.get(url, verify=False)
    data = htmlContent.text
    #json_file = open('outputfile.json','w')
    #json_file.write(data)
    #json_file.close()
    messages=[]
    for i in range(5):
        if 'message' in data['feed']['data'][i]:
            messages.append(data['feed']['data'][i]['message'])
    return messages

def check_sentiment(text):
    max_words = 1000
    max_len = 150
    text=tok.texts_to_sequences([text])
    text=pad_sequences(text,maxlen=max_len)
    prob=model_LSTM.predict(text)
    return {'sad':prob[0][0],'not_sad':prob[0][1]}

def get_emotion(messages):
    messages=get_message(user,token)
    return [check_sentiment(mess) for mess in messages]
def get_response(user, token):
    messages=get_message(user,token)
    happy_videos =['https://www.youtube.com/embed/E7H1zrTm7z8',
                   'https://www.youtube.com/embed/zJUwio7Xtec','https://www.youtube.com/embed/eK-v6uek2F4',
                  'https://www.youtube.com/embed/N25is3PifH8']
    sad=0
    for i in range((len(k))):
         sad+=get_emotion(messages)[i]['sad']
    #print(sad)
    if sad/float(len(messages)) >= 0.65:
        return random.choice(happy_videos)
    else:
        return "none"

def return_json():
   url=get_response(messages)
   result_dict={'url':url
         }
   result_json = json.dumps(result_dict)
   with open('url.json', 'w') as outfile:
       json.dump(result_dict, outfile)
   return result_json

@app.route('/delete', methods=('POST','GET'))
def delete_json():
    return ""
app.run(debug=True)
