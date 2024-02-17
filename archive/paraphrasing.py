from sentence_transformers import SentenceTransformer, util
import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering

embed_model = SentenceTransformer("all-MiniLM-L6-v2")

def cluster(df, radius):
   embed = embed_model.encode(df['sent'])
   embed = embed / np.linalg.norm(embed, axis=1, keepdims=True)

   # Perform kmean clustering
   clustering_model = AgglomerativeClustering(
       n_clusters=None, distance_threshold=radius
   )  # , affinity='cosine', linkage='average', distance_threshold=0.4)
   clustering_model.fit(embed)

   df['cluster'] = clustering_model.labels_
   df = df.set_index('cluster')
   return df

def cluster_df_to_dict(df):
   return df.groupby('cluster')['sent'].apply(list)
#paraphrases = util.paraphrase_mining(embed_model, sentences)
#
#for paraphrase in paraphrases[0:10]:
#    score, i, j = paraphrase
#    if score>0.4:
#        print("{} \t\t {} \t\t Score: {:.4f}".format(sentences[i], sentences[j], score))