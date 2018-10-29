from flask import Flask, request, url_for, redirect
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
import pickle
from keras import backend as K
import requests
import pprint
import re
import json
import urllib
import os
import ast
try:
    import urllib.request as urllib2
except ImportError:
    import urllib2
import tensorflow as tf 
from tensorflow import Graph, Session
import random



model = './Model/my_model.h5'

model_LSTM=load_model(model)

with open('tokenizer.pickle', 'rb') as handle:
    tok = pickle.load(handle)

app = Flask("mood_model")
token = 'deleted'
user = 'deleted'



def model():
    global token
    global user
    token = request.form['token']
    user = request.form['user']
    return_json(user, token)



#data=ast.literal_eval(data)
    #return access_token

def get_message(user,token):
    url = 'https://graph.facebook.com/'+user+ '?fields=feed{message}&access_token='+ token
    htmlContent = requests.get(url, verify=False)
    data = htmlContent.text
    json_file = open('outputfile.json','w')
    json_file.write(data)
    json_file.close()
    data=ast.literal_eval(data)

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
    #K.set_session(session)
    #with graph_glob.as_default():
    prob=model_LSTM.predict(text)   
    return {'sad':prob[0][0],'not_sad':prob[0][1]}

def get_emotion(messages):
    messages=get_message(user,token)
    return [check_sentiment(mess) for mess in messages]

def get_response(user, token):
    messages=get_message(user,token)
    happy_videos =['https://www.youtube.com/embed/E7H1zrTm7z8',
                   'https://www.youtube.com/embed/zJUwio7Xtec',
                   'https://www.youtube.com/embed/eK-v6uek2F4',
                   'https://www.youtube.com/embed/N25is3PifH8']
    counseling_service=['https://www.youtube.com/embed/ZGcFUEnjqe8',
    'https://www.youtube.com/watch?v=U0K3zxHq2Dg&t=25s',
    'https://www.youtube.com/embed/Ln0SCsZPZIc']
    sad=0
    for i in range((len(messages))):
         sad+=get_emotion(messages)[i]['sad']
    #print(sad)
    if 0.64<= sad/float(len(messages)) <0.98:
    #if sad >=0.65:
        return random.choice(happy_videos)
    elif sad/float(len(messages)) >= 0.98:
        return random.choice(counseling_service)
url=get_response(user, token)

@app.route('/', methods=("POST", "GET"))
def return_json():
   result_dict={'url':url
         }
   result_json = json.dumps(result_dict)
   with open('url.json', 'w') as outfile:
       json.dump(result_dict, outfile)
   return result_json

if __name__ == "__main__":
    app.run()
