import re
from nltk import tokenize


def replace_slack_mentions(text):
    return re.sub(r'<@[a-zA-Z0-9]+>', '', text)


def tokenizer(text):
    return tokenize.wordpunct_tokenize(text)
