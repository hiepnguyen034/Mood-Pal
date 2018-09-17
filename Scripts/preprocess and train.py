
# coding: utf-8

# In[63]:


import re
from sklearn.utils import shuffle
import pandas as pd
import pickle


# In[10]:


string = '0\t\twhats up'
string = re.sub(re.compile('\d*\d*\t'),"",string)
string


# In[45]:


data = pd.read_csv('review.csv',encoding='latin-1', sep='\n',header=None)  
data['label']=data[0].str.extract('(\d)',expand=True)
data[0]=[re.sub(re.compile('\d'),"",string) for string in data[0]]


# In[47]:


data[0]=[re.sub(re.compile('\t'),"",string) for string in data[0]]


# In[48]:


data.columns=['text','label']


# In[49]:


data.tail()


# In[50]:


data_2 = pd.read_csv('train.csv',encoding='latin-1')
data_2['Text']=[re.sub(re.compile('@&*\w+\d*'),"",string) for string in data_2['SentimentText']]


# In[51]:


data_2.tail()


# In[52]:


#data_2['label']=data_2[0].str.extract('(\d)',expand=True)


# In[53]:


#data_2['text']=[re.sub(re.compile('\d*\d*\t'),"",string) for string in data_2[0]]


# In[54]:


data_2=data_2.drop(['ItemID','SentimentText'],axis=1)
data_2.columns=['label','text']


# In[55]:


data_2.head()


# In[56]:


data_2=data_2[['text','label']]


# In[57]:


dataset=pd.concat([data,data_2],axis=0)


# In[58]:


dataset=shuffle(dataset)


# In[59]:


dataset['text']=[re.sub(re.compile('@'),"",string) for string in dataset['text']]


# In[60]:


dataset.reset_index(drop=True)


# In[61]:


import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import Conv1D, GlobalMaxPool1D,InputLayer
from keras import initializers, regularizers, constraints, optimizers, layers
from sklearn.model_selection import train_test_split
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences

from keras.layers import Dense, Input, LSTM, Embedding, Dropout, Activation
from keras.utils import to_categorical


# In[62]:


x_train,x_test,y_train, y_test=train_test_split(data['text'],data['label'],
                                                   test_size=0.2, random_state = 5)


# In[69]:


max_words = 1000
max_len = 150
tok = Tokenizer(num_words=max_words,filters='!"#$%&()*+,-./:;<=>?@[\]^_`{|}~123456789')
tok.fit_on_texts(list(x_train))
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tok, handle)
x_train = tok.texts_to_sequences(x_train)
x_test = tok.texts_to_sequences(x_test)
x_train = pad_sequences(x_train, maxlen=max_len)
x_test = pad_sequences(x_test, maxlen=max_len)
x_train = np.array(x_train)
x_test = np.array(x_test)
y_train = np.array(y_train)
y_test =np.array(y_test)


# In[253]:


y_train=to_categorical(y_train,2)
y_test=to_categorical(y_test,2)

def lstm_model():
    d=0.5
    model=Sequential()
    model.add(InputLayer(input_shape=(x_train.shape[1],)))
    model.add(Embedding(max_words,128))
    model.add(LSTM(128,return_sequences=True,name='lstm_layer'))
    model.add(GlobalMaxPool1D())
    model.add(Dropout(d))
    model.add(Dense(512,activation='relu'))
    model.add(Dropout(d))
    model.add(Dense(256,activation='relu'))
    model.add(Dropout(d))
    model.add(Dense(2,activation='sigmoid'))
    model.summary()
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    return model
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
model=lstm_model()
model.fit(x_train,y_train, batch_size=32, epochs=10, validation_data=(x_test,y_test))


# In[255]:


model.save('my_model.h5')

