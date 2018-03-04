#Import library
import tweepy
import pandas as pd
import numpy as np
import sys
import json
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# to force utf-8 encoding on entire program
reload(sys)
sys.setdefaultencoding('utf8')

# Tweets properties.
class Tweets():

    def __init__(self):
        self.tweets = []              # tweets list
        self.score_tweets = []        # sentiment score list of each tweet
        self.text_tweets = []         # text list of each tweet
        self.neu_tweets = []
        self.pos_tweets = []
        self.neg_tweets = []
        return

    def sentimentScore(self, tweet):
        """
        Calculate the score of each tweets
        """
        text = tweet['text']
        sentiment = analyzing.polarity_scores(text)
        # categorize sentiment
        if(sentiment['compound']) == 0.0:
            return
        elif(sentiment['compound']) > 0.0:
            self.pos_tweets.append(sentiment['pos'])
        else:
            self.neg_tweets.append(sentiment['neg'])
        #print str(sentiment['compound'])
        realTime.count += 1
        self.tweets.append(tweet)
        self.text_tweets.append(text)
        self.score_tweets.append(sentiment['compound'])
        self.stdout(sentiment, text)
        return

    def stdout(self, sentiment, text):
        """
        wrtie to file and print out
        """
        file_sentiment.write(str(len(self.tweets)) + "," + str(sentiment['compound']) + "\n")
        file_text.write(text + "\n\n")
        print "#" + str(len(self.tweets))  # number of tweet at that time
        print text  # the context of Tweet
        print str(sentiment) # sentiment score
        print "*****Current overall positive/negative Tweets*****"
        print("     Percentage of positive tweets: {0:01.1f}%".format(len(self.pos_tweets) * 100 / len(self.score_tweets)))
        print("     Percentage de negative tweets: {0:01.1f}%".format(len(self.neg_tweets) * 100 / len(self.score_tweets)))
        print("\n")
        return


# Basic listener that prints received tweets and record it.
class StdOutListener(tweepy.StreamListener):
    """
    Real-time retrieving data class
    """
    def __init__(self):
        self.count = 0
        self.start_time = time.time()
        self.limit = time_limit

    def on_data(self, data):
        """
        Streamline execution in real time
        """
        tweet = json.loads(data)
        t.sentimentScore(tweet)
        # print json.dumps(tweet, indent=2, sort_keys=True) #to show json file
        # print json.dumps(tweet, indent=2, sort_keys=True) #to show json file
        if (time.time() - self.start_time) >= self.limit:
            print "==========Done, Please see the visualization POP-UP to know the analyzed result==========\n"
            return False
        return

    def on_error(self, status):
        print status
        return

# Utilities
def twitter_setup():
    """
    Function to setup the Twitter's API
    with our access keys provided.
    """
    # Twitter App access keys for @user
    CONSUMER_KEY = "yxoq0vE5I9qZaYzEbztnqPZWi"
    CONSUMER_SECRET = "JUsvc0EfVR4Cs4jqIXuG0kd6DCAE8zHu5saJrhe4rCFOHCmxwV"
    ACCESS_TOKEN = "900174149858897921-Gpkz1IA8gvjw3NblgyT8ZIJxxfmw0iB"
    ACCESS_SECRET = "t3wqiDOKrvZkTDidJTnLdV9MQB5fEd8UMwdgLAdcL9M0B"
    # Authentication and access using keys:
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
    api = tweepy.API(auth)
    return api

def visualize():
    """
    Plot graph and Pie chart
    """
    # --> Graph:
    fig1 = plt.figure(1)
    fig1.suptitle('Sentiment Score', fontsize=20)
    ax1 = plt.subplot(111)
    ax1.set_ylim(ymin=-1, ymax=1)
    data = pd.DataFrame()
    data['Score'] = np.array([score for score in t.score_tweets])
    graph = pd.Series(data=data['Score'].values)
    graph.plot(figsize=(16, 4), color='r')
    # Move left y-axis and bottim x-axis to centre, passing through (0,0)
    ax1.spines['bottom'].set_position('center')
    # Hide the right and top spines
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)

    plt.xticks(np.arange(0, len(data['Score']), len(data['Score'])/2))

    # --> Pie chart:
    fig2 = plt.figure(2)
    fig2.suptitle('Total percentages', fontsize=20)
    labels = ['Positive', 'Negative']
    sizes = [len(t.pos_tweets), len(t.neg_tweets)]
    colors = ['green', 'red']
    explode = (0.0, 0.0)
    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%')

    #Visualize the graph
    plt.show()

# Main
if __name__ == '__main__':

    file_sentiment = open('sentiment.txt', 'w+')
    file_text = open('text.txt', 'w+')
    analyzing = SentimentIntensityAnalyzer()
    # Take input from user
    keyword = raw_input('\nInput keyword(s): ')
    time_limit = input("How long?: ")
    print "\n============================\nProcessing.....\n============================\n"
    # Twitter caller
    api = twitter_setup()
    realTime = StdOutListener()
    stream = tweepy.Stream(api.auth, realTime)
    t = Tweets()
    stream.filter(track=[keyword], languages=['en'])
    # Show result
    visualize()