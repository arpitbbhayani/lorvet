from processor import corrector, utils

category_map = {
    'NEWS': set(['news', 'happen'])
}


def classify(text):
    text = utils.replace_slack_mentions(text)
    text_s = text.lower().strip()

    # Correct all the spelling mistakes
    words = utils.tokenizer(text_s)
    words = [corrector.correct(word) for word in words]

    # find exact matches of keywords
    first_categories = set([])
    for category, keywords in category_map.iteritems():
        temp_categories = set([category for k in keywords if k in words])
        first_categories = first_categories.union(temp_categories)

    category_weights = dict((category, 100) for category in first_categories)

    if category_weights:
        return max(category_weights, key=category_weights.get)
    return None
