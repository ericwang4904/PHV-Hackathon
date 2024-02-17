#referenced by https://stackoverflow.com/questions/63718559/finding-most-similar-sentences-among-all-in-python

import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

sentences = [
    "The cat sits outside",
    "The cat plays in the garden",
    "The cat lives in the courtyard",
    "My dog lives in the front yard",
    "The cat sleeps on the porch"
]

df = pd.DataFrame(columns=["sentence"], data=sentences)

corpus = list(df["sentence"].values)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(corpus)

threshold = 0.4

for x in range(0,X.shape[0]): #X.shape returns tuple - number of questions, number of words
  for y in range(x,X.shape[0]):
    if(x!=y):
      if(cosine_similarity(X[x],X[y])>threshold):
        print("Cosine similarity:",cosine_similarity(X[x],X[y]))
        print(corpus[x])
        print(corpus[y])
        print()