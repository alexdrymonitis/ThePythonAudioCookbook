import tweepy
from vaderSentiment.vaderSentiment \
import SentimentIntensityAnalyzer
from twitter_api_credentials import *
from google.cloud import translate_v2 as translate
import pyo

RAMPTIME = .5

s = pyo.Server(audio="jack").boot()
s.start()

neg_amp = pyo.SigTo(0, time=RAMPTIME)
neg = pyo.SuperSaw(freq=50, detune=0.8, bal=0.9, mul=neg_amp)
neu_amp = pyo.SigTo(0, time=RAMPTIME)
neu = pyo.SineLoop(freq=pyo.MToF(pyo.Sig([55,60,62])),
feedback=.1, mul=neu_amp)
pos_amp = pyo.SigTo(0, time=RAMPTIME)
pos = pyo.Sine(freq=pyo.MToF(pyo.Sig([62,66,69])),
               mul=pos_amp)

mixer = pyo.Mixer(outs=1, chnls=7)
mix = pyo.Mix(mixer, voices=2, mul=.5).out()
# add inputs and set amps for the mixer
mixer.addInput(0, neg)
mixer.setAmp(0, 0, .133)
for i in range(3):
	mixer.addInput(i+1, neu[i])
	mixer.addInput(i+4, pos[i])
	mixer.setAmp(i+1, 0, .133)
	mixer.setAmp(i+4, 0, .133)


class TweetDownloader(tweepy.StreamingClient):
	def __init__(self, bearer_token, api, **kwargs):
		self._api = api
		self.sent = SentimentIntensityAnalyzer()
		self.translator = translate.Client()
		super().__init__(bearer_token, **kwargs)

	def on_tweet(self, tweet):
		is_retweet = False
		is_translated = False
		status = self._api.get_status(tweet.id,
									  tweet_mode="extended")
		try: # if it is a retweet
			full_tweet = status.retweeted_status.full_text
			is_retweet = True
		except AttributeError: # otherwise it is a tweet
			full_tweet = status.full_text
		if status.lang != "en":
			translator = self.translator.translate(
							full_tweet,
							target_language="en"
						 )
			sent = self.sent.polarity_scores(
					translator['translatedText']
				   )
			is_translated = True
		else:
			sent = self.sent.polarity_scores(full_tweet)
		if is_retweet:
			print(f"retweet: {full_tweet}")
		else:
			print(f"tweet: {full_tweet}")
		if is_translated:
			print(f"translated sentiment: {sent}\n")
		else:
			print(f"sentiment: {sent}\n")
		neg_amp.setValue(sent['neg'])
		neu_amp.setValue(sent['neu'])
		pos_amp.setValue(sent['pos'])


if __name__ == "__main__":
	# Authenticate to Twitter
	auth = tweepy.OAuth1UserHandler(CONSUMER_KEY,
									CONSUMER_SECRET,
									ACCESS_TOKEN,
									ACCESS_TOKEN_SECRET)

	# Create Twitter API object
	api = tweepy.API(auth)

	# make sure the app’s credentials are correct
	# otherwise exit
	try:
		api.verify_credentials()
		print("Authentication OK")
	except:
		print("Error during authentication")
		exit()

	tweets_client = TweetDownloader(BEARER_TOKEN, api)
	# delete previous rules so we can set new ones anytime
	current_rules = tweets_client.get_rules().data
	for rule in current_rules:
		tweets_client.delete_rules(rule.id)
	# set whatever keywords (including hashtags)
	# you want to download
	tweets_client.add_rules(
		[tweepy.StreamRule(value="#hashtag1"), tweepy.StreamRule(value="#hashtag2")]
	)
	tweets_client.filter()
