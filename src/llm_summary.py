import numpy as np
import pandas as pd
from src.perplexity_api import Client
from src.CONFIG import API_KEY

client = Client(API_KEY)

def cluster_summaries(cluster_dict):
    params = {
        'temperature': 0.2,
    }
    
    summary = []
    for cluster in cluster_dict:
        summary.append(llm_query(cluster, params))
    
    return summary

def llm_query(cluster, params):
    prompt = make_prompt(cluster)
    context = make_context()
    query = make_query(context, prompt, params)

    response = client.generate_response(query)
    return response

def make_query(context, prompt, params):
    query = {
        'model': 'pplx-7b-chat',
        'messages': [
            {'role': 'system', 'content': context},
            {'role': 'user', 'content': prompt}
        ],
        'stream': False,
    }
    query.update(**params)

    return query

def make_prompt(cluster):
    # one sentence cluster
    prompt = ""
    for i, sent in enumerate(cluster):
        prompt = prompt + f"{i}. {sent}\n"

    return prompt


def make_context():
    context = """
        Summarize a list of questions into a single question to the best of your ability and output the summarized question.\n
        Format: "Summary: [summarized text]"
    """

    return context
