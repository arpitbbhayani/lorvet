from mongoengine import (StringField, IntField, DateTimeField,
                         Document, DictField)


class NewsTweet(Document):
    text = StringField()
    tweet_id = IntField(unique=True)
    created_at = DateTimeField()
    source = StringField()
    profile_image = StringField()

    meta = {'collection': 'news_tweets'}


class MetaInfo(Document):
    key = StringField(unique=True)
    value = DictField()

    meta = {'collection': 'meta_info'}
