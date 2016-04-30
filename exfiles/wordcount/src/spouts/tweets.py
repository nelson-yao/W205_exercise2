from __future__ import absolute_import, print_function, unicode_literals

import itertools, time
import tweepy, copy
import Queue, threading

from streamparse.spout import Spout

################################################################################
# Twitter credentials
################################################################################
twitter_credentials = {
    "consumer_key" :"VVpYG8R4YOYUnW7fM2SipPK2u",
    "consumer_secret":"ogCCg7mZh5Ae0NWhTrNBvCBsYkpeGfw9K0p9wam8JImpkMPUiF",
    "access_token" :"1228832528-wIfynVzsvZkbgfEir8UOJl5Yh5RJ8iek880pm74",
    "access_token_secret" :"Syl4hF4IEQIbyrKwOu3jfiBntER60dRHyJIgcSl9s1E1y",
}

def auth_get(auth_key):
    if auth_key in twitter_credentials:
        return twitter_credentials[auth_key]
    return None

################################################################################
# Class to listen and act on the incoming tweets
################################################################################
class TweetStreamListener(tweepy.StreamListener):

    def __init__(self, listener):
        self.listener = listener
        super(self.__class__, self).__init__(listener.tweepy_api())

    def on_status(self, status):
        self.listener.queue().put(status.text, timeout = 0.01)
        return True

    def on_error(self, status_code):
        return True # keep stream alive

    def on_limit(self, track):
        return True # keep stream alive

class Tweets(Spout):

    def initialize(self, stormconf, context):
        self._queue = Queue.Queue(maxsize = 100)

        consumer_key = auth_get("consumer_key")
        consumer_secret = auth_get("consumer_secret")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

        if auth_get("access_token") and auth_get("access_token_secret"):
            access_token = auth_get("access_token")
            access_token_secret = auth_get("access_token_secret")
            auth.set_access_token(access_token, access_token_secret)

        self._tweepy_api = tweepy.API(auth)

        # Create the listener for twitter stream
        listener = TweetStreamListener(self)

        # Create the stream and listen for english tweets
        stream = tweepy.Stream(auth, listener, timeout=None)
        stream.filter(languages=["en"], track=["a", "the", "i", "you", "u"], async=True)

    def queue(self):
        return self._queue

    def tweepy_api(self):
        return self._tweepy_api

    def next_tuple(self):
        try:
            tweet = self.queue().get(timeout = 0.1)
            if tweet:
                self.queue().task_done()
                self.emit([tweet])

        except Queue.Empty:
            self.log("Empty queue exception ")
            time.sleep(0.1)

    def ack(self, tup_id):
        pass  # if a tuple is processed properly, do nothing

    def fail(self, tup_id):
        print("Delivery Failure")  # if a tuple fails to process, do nothing
