import tweepy
from tweepy import OAuthHandler
from datetime import datetime
from optparse import OptionParser
from mongoengine import connect
from ConfigParser import ConfigParser

from models import NewsTweet, MetaInfo

consumer_key = 'xxxx'
consumer_secret = 'xxxx'
access_token = 'xxxx'
access_secret = 'xxxx'

news_handles = [
    'timesofindia'
]


def replace_mentions(text, j):
    for mention in j['entities']['user_mentions']:
        text = text.replace('@' + mention['screen_name'], mention['name'])
    return text


def process_tweet(j):
    if j.get('created_at') and 'retweeted_status' not in j:
        text = j['text']
        text = replace_mentions(text, j)

        created_at = j['created_at']
        ts = datetime.strptime(created_at, '%a %b %d %H:%M:%S +0000 %Y')
        screen_name = j['user']['screen_name']
        user_image = j['user']['profile_image_url_https']

        return {
            'id': j['id'],
            'text': text,
            'created_at': ts,
            'source': screen_name,
            'user_image': user_image
        }
    return None


def save_tweet(tweet, host, port, db, collection):
    news_tweet = NewsTweet(text=tweet['text'],
                           tweet_id=tweet['id'],
                           created_at=tweet['created_at'],
                           source=tweet['source'],
                           profile_image=tweet['user_image'])

    try:
        news_tweet.save()
    except:
        return False

    return True


def process(event, host, port, db, collection):
    connect(db, host=host, port=int(port))

    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_secret)

    meta_info = MetaInfo.objects(key='news_tweets_meta').first()
    last_tweet_id = None if not meta_info else meta_info.value['toi']

    for news_handle in news_handles:
        tweets = tweepy.API(auth).user_timeline(screen_name=news_handle,
                                                since_id=last_tweet_id,
                                                count=50)
        last_tweet_id = None
        for tweet in tweets:
            tweet = tweet._json
            tweet = process_tweet(tweet)
            if not tweet:
                continue

            if not last_tweet_id:
                last_tweet_id = tweet.get('id')

            status = save_tweet(tweet, host, port, db, collection)
            if status:
                print 'Tweet with id %d saved' % tweet.get('id')
            else:
                print 'Error while saving tweet %d ' % tweet.get('id')

    if last_tweet_id:
        obj = MetaInfo.objects(key='news_tweets_meta')
        obj.update_one(set__value__toi=last_tweet_id, upsert=True)


if __name__ == '__main__':
    parser = OptionParser("usage='usage: %prog [options] arguments'")
    parser.add_option("--config", dest="config_file",
                      help="Config File")
    parser.add_option("--event", dest="event", default="update",
                      help="possible value is 'update'")
    parser.add_option("--host", dest="mongo_host",
                      help="MongoDB host: default 'localhost'",
                      default='localhost')
    parser.add_option("--port", dest="mongo_port",
                      help="MongoDB port: default 27017", default='27017')
    parser.add_option("--db", dest="db",
                      help="MongoDB database name: default piez",
                      default='lorvet')
    parser.add_option("--collection", dest="collection",
                      help="MongoDB collection name: default news",
                      default='news')

    (options, args) = parser.parse_args()

    if not options.config_file:
        print 'You forgot to mention the config file path'
        exit()

    config = ConfigParser()
    config.read(options.config_file)

    consumer_key = config.get('twitter', 'consumer_key')
    consumer_secret = config.get('twitter', 'consumer_secret')
    access_token = config.get('twitter', 'access_token')
    access_secret = config.get('twitter', 'access_secret')

    process(options.event, options.mongo_host, options.mongo_port,
            options.db, options.collection)
