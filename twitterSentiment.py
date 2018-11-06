import re
import tweepy
from tweepy import OAuthHandler
from textblob import textblob

class TwitterClient(object) :
	''' 
    Generic Twitter Class for sentiment analysis. 
    '''

    def __init__(self):
    	''' 
        Class constructor or initialization method. 
        ''' 
        #these are the keys and tokens given to me by twitter from development kit
        
        consumer_key = 'fnCLHxyQsavxDJNqXY9EfPMHx'
        consumer_secret = 'qJDgTQjMWaUW1pj3AEDI4BXwuW8FtuoUlMozG8SkVMaFsDTd14'
        access_token = '3060277270-I8yqtQHS60RgvFvTgiqTJBrcczr6QdYQYmjYACq'
        access_token_secret = 'RTiliI8HwGHP9WeLlf3u2Vr9G1CoR7xMcC0mprWmTDOiS'

        #authentication attempt
        
        try: 
        	# create OAuthHandler object
        	self.auth = OAuthHandler(consumer_key, consumer_secret)
        	#set access token and secret
        	self.auth.set_access_token(access_token, access_token_secret)
        	#create the tweepy API object to fetch tweets
        	self.api = tweepy.API(self.auth)
        except:
        	print("Error: Twitter Authentication Failed")

    def clean_tweet(self, tweet): 
        ''' 
        Utility function to clean tweet text by removing links, special characters 
        using simple regex statements. 
        '''
        return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t]) |(\w+:\/\/\S+)", " ", tweet).split())


    def get_tweet_sentiment(self, tweet):
    	#this is a function to classify the sentiment of a passed in tweet with a range of -1 to 1
    	#based on polarity, the more negative it is, the more negative the tweet and vice versa
    	
    	#creat a TextBlob object of passed in tweet's text
    	analysis = TextBlob(self.clean_tweet(tweet))

    	#this calcualtes negativity/positivity of passed in tweet
    	polarity = analysis.sentiment.polarity
    	#set sentiment
    	if 0 < polarity <= .2:
    		return 'slightly positive'
    	elif .2 < polarity <= .6:
    		return 'positive'
    	elif .6 < polarity <= 1:
    		return 'very positive'
    	elif -.2 <= polarity < 0:
    		return 'slightly negative'
    	elif -.6 <= polarity < -.2:
    		return 'negative'
    	elif -1 <= polarity < -.6:
    		return 'very negative'
    	elif polarity == 0:
    		return 'neutral'

    def get_tweet_subjectivity(self, tweet):
    	#this is a function to classify how subjective the bias is in a passed in tweet
    	#based on subjectivity which is between 0 and 1, the closer to 0 it is
    	#the more objective it is and vice versa
    	
    	analysis = TextBlob(self.clean_tweet(tweet))

    	#this calcualtes subjectivity of passed in tweet
    	subjectivity = analysis.sentiment.subjectivity

    	#set subjectivity
    	if subjectivity == 0:
    		return 'no bias'
    	if 0 < subjectivity <= .3:
    		return 'slight bias'
    	if .3 < subjectivity <= .6:
    		return 'bias'
    	if .6 < subjectivity <= 1:
    		return 'heavy bias'

    def get_sentiment(self, tweet):
    	#this function gets the sentiment of a tweet
    	#in numerical form and returns it in a dictionary
    	
    	analysis = TextBlob(self.clean_tweet(tweet))

    	#this gets the polarity and subjectivity of
    	#passed in tweet
    	polarity = analysis.sentiment.polarity
    	subjectivity = analysis.sentiment.subjectivity

    	#creates a dict to store the sentiment values
    	sentiment = {}

    	#adds them to the dictionary
    	sentiment['polarity'] = polarity
    	sentiment['subjectivity'] = subjectivity

    	return sentiment
	
	def get_tweets(self, query, count):
		#this is main function that will query for 
		#a specified number of tweets
		
		#an empty list to store parsed tweets
		tweets = []

		try:
			#call the api to fetch tweets
			fetched = self.api.search(q = query, rpp = count)

			#parsing tweets one by one
			for tweet in fetched:
				#empty dictionary to store required params of a tweet
				parsed_tweet = {}

				#saving text of tweet in dictionary
				parsed_tweet['text'] = tweet.text
				#saving the sentiments of the tweet
				parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)
				parsed_tweet['subjectivity'] = self.get_tweet_subjectivity(tweet.text)

				#appending parsed tweet to tweets list
				#and only append once if there are rebtweets
				if tweet.retweet_count > 0:
					if parsed_tweet not in tweets:
						tweets.append(parsed_tweet)
				else:
					tweets.append(parsed_tweet)

			return tweets

		except tweepy.TweepError as e:
			print("Error : " + str(e))




