#test.py
import const
import json
import tweepy
from tweepy import Stream
import urllib
import re
import requests


# authenticate keys
auth = tweepy.OAuthHandler(const.CONSUMER_KEY, const.CONSUMER_SECRET)
auth.set_access_token(const.ACCESS_TOKEN, const.ACCESS_TOKEN_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)



# try:
#     api.verify_credentials()
#     print('Verification Successful.')
# except:
#     print('Authentication Error.')

# A listener handles tweets that are received from the stream. This is a basic listener that prints recieved tweets to standard output
class TweetListener(Stream):
    def onData(self, data): # return data
        print(data)
        return True
    def onError(self, status): # return status on error
        print(status)

# given a user ID and returns the screen name
def get_usernames(ids):
    user_objs = api.lookup_users(user_ids=ids)
    for user in user_objs:
        print(user.screen_name)

# determines whether two people are following each other 
def compareFriendship(a,b):
    status = api.get_friendship(source_screen_name = a, target_screen_name = b)
    if status[0].following == True and status[1].following == True:
        return True
    return False

# searches recent tweets in English given a query
def crawler(query):
    tweetList = []
    tweets = api.search_tweets(q=query, count=50,
                        result_type = "recent",
                        lang = "en") 
    for tweet in tweets:
        tweetList.append(tweet.id)
    return tweetList

# searches recent tweets within a 25 mile radius to Dayton, OH
# returns list of tweet text
def geoCrawler(parameters):
    tweetList = []
    tweets = api.search_tweets(q=' ', count=50, geocode = parameters, result_type = "recent", lang = "en") 
    for tweet in tweets:
        status, location = getTweet(tweet.id)
        tweetList.append([status, location])
    return tweetList

# searches recent tweets within a 25 mile radius to Dayton, OH
# return list of tweets with external links
def geoCrawler2(parameters):
    tweetList = []
    tweets = api.search_tweets(q=' ', count=50, geocode = parameters, result_type = "recent", lang = "en") 
    for tweet in tweets:
        status, userID = getLinkedTweets(tweet.id)
        tweetList.append([status, userID])
    return tweetList

# returns the expanded url and userID of the tweets 
def getLinkedTweets(tweetID):
    tweet = api.get_status(id=tweetID)
    return tweet.text, tweet.user.screen_name

# returns text of status after given a tweet ID
def getTweet(tweetID):
    tweet = api.get_status(id=tweetID)
    return tweet.text, tweet.user.location

# prints information of a user 
def printUserInformation(user):
    print("\n--------------------------------------------------- USER ---------------------------------------------------")
    print("\nUsername: ", user.name)
    print("Screen Name: ", user.screen_name)
    print("User ID: ", user.id)
    print("Location: ", user.location)
    print("User Description: ", user.description)
    print("Number of followers: ", user.followers_count)
    print("Number of friends: ", user.friends_count)
    print("Number of tweets: ", user.statuses_count)
    print("Number of likes: ", user.favourites_count)
    print("User Url: ", user.url)

def main():
    twitterStream = Stream(const.CONSUMER_KEY, const.CONSUMER_SECRET,const.ACCESS_TOKEN, const.ACCESS_TOKEN_SECRET)
    users = api.lookup_users(screen_name = {"denaschaeffer","yummyyummyhippo"})

    for user in users:
        ################# PART 1 #################
        printUserInformation(user)

        ################# PART 2 #################
        first20followersIDs = []
        first20followers = []
        following = [] 
        mutuals = []

        first20followersIDs = tweepy.Cursor(api.get_follower_ids, screen_name=user.screen_name).items(20) # only gets the first 20
        followingSubset = tweepy.Cursor(api.get_friends, screen_name=user.screen_name).items(50)

        for person in followingSubset:
            following.append(person.screen_name)

        # compare relationship between user and its following
        for person in following:
            temp = compareFriendship(user.screen_name, person)
            if temp:
                mutuals.append(person)

        for follower in first20followersIDs:
            followerTemp = api.get_user(user_id = follower)
            first20followers.append(followerTemp.screen_name)

        print(f'First 20 Followers: {first20followers}')
        print(f'Friends: {mutuals}')

    print("\n--------------------------------------------------- Tweets ---------------------------------------------------")
    ################# PART 3.1 #################
    # Write a crawler to collect the first 50 tweets that contain these two keywords: [Ohio, weather].

    tweetList = []
    searchQuery = 'Ohio AND weather -filter:links' # Keywords
    tweetIDs = crawler(searchQuery)

    for tweet in tweetIDs:
        status = getTweet(tweet)
        tweetList.append(status)

    # print(f'First 50 tweets with keywords "Ohio" and "weather": {tweetList}') 
    print('First 50 tweets with keywords "Ohio" and "weather":' )
    for t in tweetList: # printing like this for readability
        print('\t-- ' + str(t))

    ################# PART 3.2 #################
    # Write a crawler to collect the first 50 tweets that originate from Dayton region.
    geoTweetList = []
    coordinates = '39.758949,-84.191605,25mi' # latitude, longitude, radius

    geoTweetList = geoCrawler(coordinates)

    # print(f'First 50 tweets within the range of 25 miles of Dayton, OH: {geoTweetList}') 
    print('First 50 tweets within a 25 mile radius to Dayton, OH:' )
    for t in geoTweetList:
        print('\t-- ' + str(t))

    print("\n--------------------------------------------------- Finding Malicious Tweets ---------------------------------------------------")
    ################# PART 4 #################
    ## The goal here is to take a list of tweeted urls within a certain radius and determine if any of them are malicious. If they are, 
    ## then I add them to a list of suspicious users
    
    coordinates = '39.758949,-84.191605,25mi' # latitude, longitude, radius [Dayton,OH]
    urlList = []
    suspiciousTweets = []

    # create a list of [tweets, screen name]
    daytonTweets = geoCrawler2(coordinates)

    # creating list of [urls, screen name]
    print("Gathering list of tweets...")
    for t in daytonTweets:
        url = re.findall("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", t[0])
        if url:
            urlList.append([url, t[1], t[0]])
        print('\t-- ' + str(t)) # tweet, screenname


    # verify if the links are safe
    print("Gathering urls from tweets...")
    for obj in urlList:
        print('\t-- ' + str(obj)) # tweet, screenname
        for u in obj[0]: #just in case there are multiple urls in a tweet
            tempCount = 0
            r = requests.get(u)
            redirects = r.history
            endingURL = r.url

            if len(redirects) > 1:
                tempCount += 1
            if endingURL[0:5] != "HTTPS": # checks if ending url (from potential redirects) is not https
                tempCount += 1
            if tempCount >= 2: # >= to handle additional future cases (ex. domain names, etc)
                suspiciousTweets.append(obj)

    # print list of suspicious users
    print("List of potentially malicious tweets: ")

    if len(suspiciousTweets) == 0: # this will likely return empty!!!
        print("\tNo malicious tweets yet!")
    else: 
        for user in suspiciousTweets:
            print('\t-- ' + str(user)) # url, screenname
    
    return #end main

# call main()
if __name__ == '__main__':
    main()

