import numpy as np
import pandas as pd
from src.cluster_model import cluster, cluster_df_to_dict
from src.llm_summary import cluster_summaries

corpus = [
   #"What is a banana?",
   #"What is an apple?",
   #"How old are you?",
   #"Can you provide resources for this?",
   #"Can you give me food?",
   "The \"ds is the magnitude of the derivative (times dt)\" paragraf ends with a little \"proof\" if you will. This proof ends with sqrt( dx²+ dx²), shouldn't it be sqrt( dx²+ dy²)dt ?",
   "Should be ds = |r'(t)|dt ?",
   "In the Step 1 answer, you've taken the derivative of (1/t) as (-1/t^2), but shouldn't it be ln | t | ?."
   "Is there any way to do these integrals faster, perhaps a pattern to look for of some sort? What about numerical integration? Thanks!",
   "I thought line integration was not for computing area surely we would use double integration or this. So in the first example why is the answer 8 and not pl ?",
   "Can scalar line integrals have a negative signed area if the \"curtain\" between the curve and the function is below the xy plane?",
   "In the first example why we took the multivariable function f(x,y) = x + y ?",
]

df = pd.DataFrame()
df['sent']= corpus
df = cluster(df, 1.2)
cluster_dict = cluster_df_to_dict(df)
summaries = cluster_summaries(cluster_dict)

for i,sum in enumerate(summaries):
    print("-"*10)
    print(cluster_dict[i])
    print(sum)



