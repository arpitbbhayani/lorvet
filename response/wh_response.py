import random
from processor import utils

WH_TYPES = {
    'WHAT': ['what', 'wht'],
    'WHO': ['who'],
    'WHERE': ['where', 'whr'],
    'WHY': ['why'],
    'WHEN': ['whn', 'when'],
    'HOW': ['how', 'hw'],
    'WHICH': ['which', 'whch'],
    'WHOSE': ['whose', 'whse'],
    'WHOM': ['whom', 'whn'],
    'CAN': ['can']
}

WH_RESPONSES = {
    'WHAT': {
        0: ['Sorry, I tried but I could not find anything :disappointed:'],
        10: ['Okay, let me get back to you in some time.']
    },
    'WHO': {
        0: [],
        10: []
    },
    'WHERE': {
        0: [],
        10: []
    },
    'WHY': {
        0: [],
        10: []
    },
    'WHEN': {
        0: [],
        10: []
    },
    'HOW': {
        0: [],
        10: []
    },
    'WHICH': {
        0: [],
        10: []
    },
    'WHOSE': {
        0: [],
        10: []
    },
    'WHOM': {
        0: [],
        10: []
    },
    'CAN': {
        0: ['Sorry, I am currently unable to do this :disappointed:.'],
        10: ['Yeah sure, I can :simple_smile:.']
    }
}


def find_wh(text):
    """ Given text, returns WH type """
    text_s = text.lower().strip()
    words = utils.tokenizer(text_s)

    wh_categories = set([])
    for wh_type, keywords in WH_TYPES.iteritems():
        temp_categories = [wh_type for keyword in keywords if keyword in words]
        wh_categories = wh_categories.union(set(temp_categories))

    category_weights = dict((category, 100) for category in wh_categories)

    if category_weights:
        return max(category_weights, key=category_weights.get)
    return None


def response(text, yesno):
    """ Returns response based on text and if it was successfully answered """
    wh_type = find_wh(text)
    if not wh_type:
        return None

    all_wh_responses = WH_RESPONSES.get(wh_type)
    if all_wh_responses is None:
        return None

    responses = all_wh_responses.get(yesno)
    if not responses:
        return None

    return random.choice(responses)
