import os
import pickle
import sklearn
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer

from flask import Flask
from flask import jsonify

app = Flask(__name__)

# Read environment variables
loc_df    = os.environ.get("URL_DATAFRAME", default="df.csv")
loc_tfidf = os.environ.get("URL_MODEL_TFIDF", default="tfidf_model.pkl")
loc_nn    = os.environ.get("URL_MODEL_NN", default="nn_model.pkl")

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
print(f'INFO: loaded {len(df.index)} dataframe rows')

@app.route('/get_recommendation')
def hello():
    ret_dict = {}
    new_doc_score = tfidf.transform(["I want to feel super relaxed, yet energetic and creative"])
    mdl_rslt = nn.kneighbors(new_doc_score.todense())

    ret_dict["results"] = int(mdl_rslt[1][0][0])
    return jsonify(ret_dict)

if __name__ == '__main__':
    app.run()
