#!/usr/bin/python

from tensorflow import keras as ks
from nltk import PorterStemmer
import sys
import pickle
import cgi
import cgitb
import re
import sys

MAXLEN=500

with open("vocab") as file:
  vocab = pickle.load(file)
with open("stopwords.txt") as file:
  stopwords = file.read().splitlines()
  
text = cgi.FieldStorage()['text'].value
#print(text, file=sys.stderr)
#print >> sys.stderr, text

ps = PorterStemmer()
x = re.sub('[^a-z ]', '', text.lower()).split()
x = list(map(ps.stem, filter(lambda w : w not in stopwords, x)))
x = filter(lambda w:w in vocab, x)
x = ks.preprocessing.sequence.pad_sequences([[vocab.index(word) for word in x]], maxlen=MAXLEN) #change?

model = ks.models.load_model("W_gender")
gender = "male" if model.predict(x)[0] > 0.5 else "female"

model = ks.models.load_model("W_age")
age = round(model.predict(x)[0])

print("Content-Type:text/html")
print("")
print("<http>")
print("<head><style>")
print("* {")
print("  box-sizing: border-box;")
print("}")
  
print("  .half {")
print("  	float: left;")
print("  	width: 50%;")
print("  }")
print("</style></head>")

print("<div class=\"half\">")
print("  <form action=\"/cgi-bin/frontend.py\" method=\"post\">")
print("    <textarea rows=10 cols=50 name='text'>%s</textarea><br>" % text)
print("    <input type='submit' value='Predict' />")
print("  </form>")
print("</div>")

print("<div class='half'>")
print("  <strong>&nbsp;&nbsp;Predicted gender: </strong>")
print("  <p style='display:inline' id='gender'>%s</p>" % gender)
print("  <br><br>")
print("  <strong name='age'>&nbsp;&nbsp;Predicted age: </strong>")
print("  <p style='display:inline' id='age'>%d</p>" % age)
print("</div>")
print("</http>")