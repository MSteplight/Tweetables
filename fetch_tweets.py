import tweepy
import re
import string
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import nltk
from twitter_setup import client # import the APIv2 client 

#initialize stemmer
stemmer = PorterStemmer()

#define stopwords list from NLTK
stop_words = set(stopwords.words('english'))

print("fetch_tweets.py has started running...")

def clean_tweet(tweet_text):
    #convert text to lowercase
    tweet_text = tweet_text.lower()

    #removes any unwanted characters such as URLs, mentions, hashtags, punctuation, stopwords, extra spacing, emojis, special characters, and performs stemming'
    #remove URLs
    tweet_text = re.sub(r"http\S+|www\S+|https\S+", "", tweet_text)

    #remove hashtags 
    tweet_text = re.sub(r'#\S+', '', tweet_text)

    #remove mentions
    tweet_text = re.sub(r'@\S+', '', tweet_text)

    #remove punctuation
    tweet_text = tweet_text.translate(str.maketrans("", "",string.punctuation))

    #remove emojis using regex pattern (unicode ranges for emojis)
    tweet_text = re.sub(r'[^\x00-\x7F]+', '', tweet_text) #this removes non-ASCII characters (like emojis)

    #optionally, remove extra spaces and clean up
    tweet_text = ' '.join(tweet_text.split())

    #remove stopwords (common words like 'the')
    tweet_text = ' '.join([word for word in tweet_text.split() if word not in stop_words])

    #perform stemming to reduce words to their root form (e.g., "running" -> "run")
    tweet_text = ' '.join([stemmer.stem(word) for word in tweet_text.split()])

    return tweet_text

def fetch_tweets_v2(keyword, count=11):
    #fetching tweets using APIv2
    try:
        # Ensure the count is between 10 and 100
        count = max(10, min(count, 100))
        
        # Fetch tweets with the provided keyword
        response = client.search_recent_tweets(query=keyword, max_results=count)
        
        if response:
            print(f"Fetched {len(response)} tweets for keyword: {keyword}")
            for i, tweet in enumerate(response.data, start=1):
                cleaned_text = clean_tweet(tweet.text)
                print(f"{i}. {cleaned_text}\n")
        else:
            print("No tweets found.")

    except Exception as e:
        print(f"Error fetching tweets: {e}")


#test with a keyword
fetch_tweets_v2("horror", count=11)


