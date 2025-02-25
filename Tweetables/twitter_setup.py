import tweepy

#twitter API credentials
API_KEY = "ej6yjnQT1SsTbGy83GHOJ3GQw"
API_SECRET ="8LxcAIO0BEXzRYbhUIKm97AyFHLtazVqhZ7MF4EDd8vfKs958z"
ACCESS_TOKEN = "1886917504972533760-wW2msDaM25BL9yDpjR3ZlMpHpLsk9o"
ACCESS_SECRET = "ALfQdUiRv6jxwojiseNNxtQtDdI5MvbLaysk5zLle4owG"
BEARER_TOKEN = "AAAAAAAAAAAAAAAAAAAAAEoCywEAAAAAhSTrbfIgPKOqNPR7QTxUFhfQbYI%3DC7a17wd41zooYPuPGfVTYEYGtxKQJgCTFh23tDW2aXjJ6eyqXV" # needed for API v2

#print(f"API_KEY: {API_KEY}")
#print(f"API_SECRET: {API_SECRET}")
#print(f"ACCESS_TOKEN: {ACCESS_TOKEN}")
#print(f"ACCESS_SECRET: {ACCESS_SECRET}")
#print(f"BEARER_TOKEN: {BEARER_TOKEN}")

#authenticate to twitter
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# create API object
api = tweepy.API(auth, wait_on_rate_limit = True)

#authenticate using API v2 (for fetching tweets)
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# test authentication
try:
    user = api.verify_credentials()
    print(f"Authentication successful! Logged in as: {user.name}")
except Exception as e:
    print(f"Authentication failed: {e}")