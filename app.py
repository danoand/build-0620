# Standard imports
import os
import re
import pickle
import pandas as pd
import numpy  as np

# Modeling/vectorizing imports
import sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
import spacy

# Flask imports
from flask import Flask
from flask import request
from flask import jsonify

app = Flask(__name__)

# Read environment variables
is_heroku = os.environ.get("IS_HEROKU", default=False)
loc_df    = os.environ.get("URL_DATAFRAME", default="df.csv")
loc_tfidf = os.environ.get("URL_MODEL_TFIDF", default="tfidf_model.pkl")
loc_nn    = os.environ.get("URL_MODEL_NN", default="nn_model.pkl")

# Use the spacy library to generate strain description tokens
# Instantiate a spacy object
nlp = spacy.load("en_core_web_sm")

# Regular expressions used to remove non-standard characters
rgxNotStdChars = re.compile(r'[^a-zA-z0-9.,!?/:;\"\'\s]')
rgxMultWhtSpce = re.compile(r'\s{2,}')

# 'retain_std_chars' takes a string and returns that string with non-standard characters removed
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
# Load the model from the web if deployed to Heroku
if is_heroku:
  print(f'INFO: not using Heroku as this time. Terminating.')
  quit()

# Load the model from disk if deployed other than Heroku
if not is_heroku:
  pkl_file = open(loc_nn, 'rb')
  nn       = pickle.load(pkl_file)
  pkl_file.close()

# Read the TF-IDF model 
print(f'INFO: loading the word vectorization model')
pkl_tfidf_file = open(loc_tfidf, 'rb')
tfidf          = pickle.load(pkl_tfidf_file)
pkl_tfidf_file.close()

# Read in the dataframe from disk
print(f'INFO: loading the modeled dataset')
df = pd.read_csv(loc_df)
print(f'INFO: loaded {len(df.index)} dataframe rows')

# Convert the dataframe to a dict
print(f'INFO: generating a map of dataframe rows/elements')
dict_df = df.to_dict('records')

# /status can be used to verify that the Flask app is running and responding
@app.route('/status')
def test():
  num_strains = len(dict_df)
  ret_dict = {}
  ret_dict["msg"] = "app.py is up and running"
  ret_dict["note"] = "the number of strains in the dataset is: " + str(num_strains)

  return jsonify(ret_dict)

# /get_recommendation accepts a string of text and returns a collection of strain recommendations
#     and associated metadata
@app.route('/get_recommendation', methods = ['POST'])
def get_recommendation():
  # Get the request's body as json
  jsn      = request.get_json(force=True)
  ret_dict = {}

  # Validate the inbound json body parameters
  tmp_string = jsn["text"]
  if len(tmp_string) == 0:
    # missing text value
    ret_dict["msg"] = "missing text value"
    return jsonify(ret_dict), 400

  # Process the inbound text and generate a list of tokens
  tmp_text = retain_std_chars(jsn["text"])
  tmp_list = tnkize_text(tmp_text) 

  # Score the list of tokens
  tmp_score = tfidf.transform([tmp_list])
  tmp_rslt  = nn.kneighbors(tmp_score.todense())

  # Grab the reccomendation scores/rankings and references
  rel_ranks = tmp_rslt[0][0]
  rel_docs  = tmp_rslt[1][0]

  # Iterate through the document references
  ret_list = []
  for idx, elm in np.ndenumerate(rel_docs):
    tmp_dict = dict_df[rel_docs[idx[0]]]

    # Construct a temporary map
    ret_dict = {}
    ret_dict['description']       = tmp_dict['Description']
    ret_dict['effects']           = tmp_dict['Effects']
    ret_dict['flavor']            = tmp_dict['Flavor']
    ret_dict['symptoms_diseases'] = tmp_dict['symptoms_diseases']
    ret_dict['rating']            = tmp_dict['Rating']
    ret_dict['strain']            = tmp_dict['Strain']
    ret_dict['type']              = tmp_dict['Type']
    ret_dict['df_index']          = int(rel_docs[idx[0]])
    ret_dict['score']             = round(rel_ranks[idx[0]], 3)
    
    ret_list.append(ret_dict)

  # Construct the return object
  return_object = {}
  return_object["msg"]              = "your recommendations"
  return_object["text"]             = jsn["text"]
  return_object["recommendations"]  = ret_list
  return_object["length"]           = len(ret_list)

  return jsonify(return_object)

# Start the flask listening on localhost:5000
if __name__ == '__main__':
  app_domain = 'localhost'
  app_port   = 5000
  print(f'INFO: starting web api server on {app_domain}:{app_port}')
  app.run(host='localhost', port=5000)
