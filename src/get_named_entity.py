from transformers import pipeline

token_classifier = pipeline("token-classification", model="dslim/bert-base-NER")

def find_named_entities(sentence):
    tokens = token_classifier(sentence)
    return tokens