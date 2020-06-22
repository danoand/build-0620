import os
import pickle
import sklearn
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

# Read environment variables
loc_df    = os.environ.get("URL_DATAFRAME", default="df.csv")
loc_tfidf = os.environ.get("URL_MODEL_TFIDF", default="tfidf_model.pkl")
loc_nn    = os.environ.get("URL_MODEL_NN", default="nn_model.pkl")

# Steps to Clean the Strain Descriptions
import re
import pandas as pd
# Use the spacy library to generate strain description tokens
import spacy

# Instantiate a spacy object
nlp = spacy.load("en_core_web_sm")

# Regular expression used to remove non-standard characters
rgxNotStdChars = re.compile(r'[^a-zA-z0-9.,!?/:;\"\'\s]')
rgxMultWhtSpce = re.compile(r'\s{2,}')

# 'retain_std_chars' takes a string and returns that string with non-standard
#    characters removed
def retain_std_chars(val):
  # Is the passed value NaN?
  if pd.isna(val):
    return 'none'

  # Is the passed not a string?
  if type(val) != str:
    return 'none'

  # Is the value an empty string?
  if val == "":
    return 'none'

  # Lower case the input value
  tmp_lower = val.lower()

  # Is the value "none"?
  if tmp_lower == "none":
    return 'none'

  # Remove non-standard characters
  tmp_std = re.sub(rgxNotStdChars, "", tmp_lower)

  # Convert multiple whitespace characters to one whitespace character
  tmp_wht = re.sub(rgxMultWhtSpce, "", tmp_std)

  # Strip leading and trailing whitespace
  tmp_rtn = tmp_wht.strip()
  
  return tmp_rtn

# tnkize_text takes a string and returns a list of tokens generated via the spacy library
def tnkize_text(val):
  tmp_list = []
  tmp_doc = nlp(val)

  # Iterate through the text's tokenized objects
  for tkn in tmp_doc:
    tmp_list.append(tkn.text)

  return tmp_list

def dummy_func(doc):
    return doc

# Read the Nearest Neighbors model
print(f'INFO: loading the recommendation model')
pkl_file = open(loc_nn, 'rb')
nn       = pickle.load(pkl_file)
pkl_file.close()

# Read the TF-IDF model 
print(f'INFO: loading the word vectorization model')
pkl_tfidf_file = open(loc_tfidf, 'rb')
tfidf          = pickle.load(pkl_tfidf_file)
pkl_tfidf_file.close()

# Read in the dataframe
print(f'INFO: loading the modeled dataset')
df = pd.read_csv(loc_df)
print(f'INFO: loaded {len(df.index)} dataframe rows\n')

@app.route('/test')
def test():
    ret_dict = {}
    new_doc_score = tfidf.transform(["I want to feel super relaxed, yet energetic and creative"])
    mdl_rslt = nn.kneighbors(new_doc_score.todense())

    ret_dict["results"] = int(mdl_rslt[1][0][0])
    return jsonify(ret_dict)

@app.route('/get_recommendation', methods = ['POST'])
def get_recommendation():
    # Get the request's body as json
    jsn = request.get_json(force=True)

    # Score the inbound text 
    tmp_score = tfidf.transform([jsn["text"]])
    tmp_rslt  = nn.kneighbors(tmp_score.todense())

    # Determine the row number of the first result
    rslt = tmp_rslt[1][0]

    # Get the data from dataframe
    # tmp_dict = df.to_dict('records')[first_rslt]

    return jsonify(rslt)


if __name__ == '__main__':
    app.run()
