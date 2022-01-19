# CPS 470/570: Computer Networks and Security #
## Programming Assignment 2 ##

### 1. Purpose ###

This project crawls twitter social networks and conducts basic data analytics. 

### 2. Description ###
#### 2.1: Twitter Basics ####

Twitter users post tweets (i.e., “status updates”) – text messages of up to 140 characters, which can also contain images, video media, or links to other online resources – and interact with others by following or responding to their messages. The data structure of a tweet contains (in addition to the text) metadata such as a username and a user screen name, numerical identifiers, a timestamp, the language of the text, the location of the user, and/or the ways in which the status update references other messages or users on the platform.

The types of information that we can extract from twitter:

- Information about a user
- User’s Followers or Friends
- Tweets published by a user
- Search results on Twitter
- Places & Geo

It offers three Twitter APIs:

- REST APIs: Provide programmatic access to read and write Twitter data
- Streaming APIs: Once a request for information is made, the Streaming APIs provide a continuous stream of updates with no further input from the user
- Search API: The Twitter Search API searches against a sampling of recent Tweets published in the past 7 days

Tweets are delivered in the format JSON (JavaScript Object Notation between web servers and clients) that can be processed using a number of programming languages and software packages. There are many existing libraries in common programming languages to facilitate interaction with the Twitter APIs, e.g., tweepy (for python) and twitter4j (for java). While you are welcome to use twitter4j, this handout shows instructions for using tweenpy. The main steps include:

- Apply for a developer account at twitter
- Install tweepy
- Create a python project and write code for crawling!

Each will be explained in details in the following. 

#### 2.2 Apply for a developer account ####

Go to https://developer.twitter.com/en/apps. Create a twitter account and then click Create an app. 

#### 2.3. Install tweepy ####

pip install tweepy

#### 2.4. Create a python project for crawling twitter ####

Enter the skeleton code and test using github and twitter as the users.

Twitter APIs have rate limiting. See details at https://developer.twitter.com/en/docs/basics/ratelimiting.

- The REST API rate limits can be found at https://developer.twitter.com/en/docs/basics/ratelimits. For instance, the GET users/ calls are limited to 15 requests every 15 minutes.
- One can connect to the Streaming API to form a HTTP request. The Streaming API free-ups rate limits for more use, but it still has rate limiting. Check this link https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/connecting.

You should not exceed the rate limits when doing this project; otherwise, your developer account might be blocked by twitter.

Tweepy has well written documenation at https://tweepy.readthedocs.io/en/latest/index.html. The sample code above is from the website. Your task is to read documentation and address the questions for this assignment. 

#### 2.5. Report ####

##### Task 1 (15pts):  

A use profile provides a rich source of information to study twitter users. Given a list of user’s screen names, write a crawler to display this users’ profile information. You should get the following information for any existing twitter user:

- User name:
- Screen name:
- User ID:
- Location:
- User description:
- The number of followers:
- The number of friends:
- The number of tweets (i.e., statuses):
- User URL:

##### Task 2 (15pts): #####

There are two types of connection between users: follower and friend. Friendship is bidirectional while following is one direction. In the following figure, Amy and Peter are friends (meaning that they follow each other), Bob is following Amy (so Bob is Amy’s follower), and Amy follows Sophia. Given a list of user’s screen names (any existing names), write a crawler to collect the
users’ social network information (i.e., display friends and the first 20 followers). Note that friends are bidirectional (e.g., Amy and Peter are friends as they follow each other). 


##### Task 3 (30pts): #####

Twitter provides APIs to collect tweets that contain the specified keywords or originate from a given geographic region. The returned objects of the search are in JavaScript Object Notation (JSON). You will extract some fields in JSON. You will look at both Search API and streaming API.

1.  (15pts) Write a crawler to collect the first 50 tweets that contain these two keywords: [Ohio, weather].
2.  (15pts) Write a crawler to collect the first 50 tweets that originate from Dayton region, specified by point_radius: [Longitude of the center, Latitude of the center, radius], where the radius can be up to 25 miles. Any tweet containing a geo point that falls within this region will be matched. Dayton OH geographic information is: Latitude 39.758949, Longitude -84.191605. Note that Google Maps takes a slightly different format, i.e., [Latitude, Longitude].

##### Task 4 (40pts): #####
Use the twitter API for your own idea. The following are some ideas for your reference. You can go to scholar.google.com and search papers/books on “twitter” to do brainstorming.

1. Write code to deliver tweets of your interest to your email at 8:00AM every day;
2. Write code to deliver tweets on stock price changes to your email and make suggestions, e.g., buy/sell this stock;
3. Write code to detect fake news;
4. Write code to detect bot accounts (i.e., accounts controlled by attackers);
5. Write code to detect users who need help (e.g., people with mental health issues);
6. Or your own idea. 

### 3. Turn In ###
- Your report that provides answers to the tasks in Section 2.5.
- Source code: You can either submit a single script file that finishes all tasks altogether or individual .py files for each task.
- Submit a README file: The Python version you used to test your code; how to compile/run your source code.

