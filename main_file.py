import tweepy
from textblob import TextBlob
import preprocessor
import matplotlib.pyplot as plt

import twitter_credentials

def percentage(part, whole):
    return 100 * float(part)/float(whole)

auth = tweepy.OAuthHandler(consumer_key = twitter_credentials.CONSUMER_KEY, consumer_secret = twitter_credentials.CONSUMER_SECRET)
auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth)

searchTerm = input("Enter Keyword/Hashtag to search about : ")
noOfSearchTerm = int(input("Enter number of tweets that need to be analyzed : "))

tweets_list = []
tweets_clean = []

for tweet in tweepy.Cursor(api.search, q=searchTerm, tweet_mode = 'extended', lang = 'en').items(noOfSearchTerm):
    tweets_list.append(tweet.full_text)
    tweets_clean.append(preprocessor.clean(tweet.full_text))

#for tweet in tweets_list:
#    tweets_clean.append(preprocessor.clean(tweet))

#for i in range(len(tweets_list)):
#    print("----------------------------")
#    print("tweets_list: ", i , " : ", tweets_list[i])
#    print("tweets_clean: ", i , " : ", tweets_clean[i])
#    print("----------------------------")

positive_polarity = 0
positive_votes = 0
negative_polarity = 0
negative_votes = 0
neutral_polarity = 0
neutral_votes = 0
polarity = 0


for tweet in tweets_clean:
    analysis = TextBlob(tweet)
    polarity += analysis.sentiment.polarity

    if(analysis.sentiment.polarity == 0):
        neutral_votes += 1
    elif(analysis.sentiment.polarity < 0.00):
        negative_votes += 1
    elif(analysis.sentiment.polarity > 0.00):
        positive_votes += 1


positive_percentage = percentage(positive_votes, noOfSearchTerm)
negative_percentage = percentage(negative_votes, noOfSearchTerm)
neutral_percentage = percentage(neutral_votes, noOfSearchTerm)

positive_percentage = format(positive_percentage, '.2f')
negative_percentage = format(negative_percentage, '.2f')
neutral_percentage = format(neutral_percentage, '.2f')

print("positive_percentage : ", positive_percentage)
print("negative_percentage : ", negative_percentage)
print("neutral_percentage : ", neutral_percentage)

labels = ['Positive [' + str(positive_percentage) + '%]', 'Neutral [' + str(neutral_percentage) + '%]', 'Negative [' + str(neutral_percentage) + '%]' ]
sizes = [positive_percentage, neutral_percentage, negative_percentage]
colors = ['yellowgreen', 'gold', 'red']
patches, texts = plt.pie(sizes, colors = colors, startangle = 90)
plt.legend(patches, labels, loc = 'best')
plt.title('People Reaction On ' + searchTerm + ' By Analyzing ' + str(noOfSearchTerm) + ' Tweets.')
plt.axis('equal')
plt.tight_layout()
plt.show()