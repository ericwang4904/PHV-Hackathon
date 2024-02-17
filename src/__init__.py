import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer, util

sent_model = SentenceTransformer("all-MiniLM-L6-v2")
