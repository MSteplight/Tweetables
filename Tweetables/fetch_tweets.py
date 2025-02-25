import tweepy
from twitter_setup import client # import the APIv2 client

def fetch_tweets_v2(keyword, count=10):
    #fetching tweets using APIv2
    try:
        #ensure count is between 10 and 100 (twitter's limit)
        count = max(10, min(count, 100))
        response = client.search_recent_tweets(
            query=keyword, 
            max_results=count, 
            tweet_fields=["author_id", "created_at", "lang"]
            )
        #debug: print the raw response from twitter
        print("Raw Response:", response)

        if response.data:
            for i, tweet in enumerate(response.data, start=1):
                print(f"{i}. {tweet.text}\n")
        else:
            print(f"No tweets found for the keyword:", keyword)
    except Exception as e:
        print(f"Error fetching tweets: {e}")

#test with a keyword
fetch_tweets_v2("action", count=10)


