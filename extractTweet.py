import tweepy 
import csv
import re
# consumer_key = "28JS************************q6GDavr"
# consumer_secret = "kos**********************************kaVR6KyC9dfejVRqSQqYLipRMN6nZaoYwCKw4EG"
# access_key = "44149913-Y**13c67tT8ID*********************OB3MDCU6"
# access_secret = "yzKFo3uHim1fzR0eW4udIuYiTD2yH****************************8BN"
consumer_key = "28JSn80k7NYA3iOz6sq6GDavr"
consumer_secret = "kos8IMmTPa2kaVR6KyC9dfejVRqSQqYLipRMN6nZaoYwCKw4EG"
access_key = "44149913-YQ29wDZ13c67tT8IDrWSUkVBDTkaqyMuoOB3MDCU6"
access_secret = "yzKFo3uHim1fzBlAIaMrVa0E5WnR0eW4udIuYiTD2yHBN"

def get_all_tweets(screen_name):
	#initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []		
	#make initial request for most recent tweets (2000 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=100)
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	print(len(new_tweets))
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	count = 0
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0 and count > 0 :
		# print ("getting tweets before %s" % (oldest))
		count = count - 1 
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=100,max_id=oldest)
		#save most recent tweets
		alltweets.extend(new_tweets)
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		print ("...%s so far" % (len(alltweets)))
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets=[]
	for tweet in alltweets:
		tweet_text=tweet.text.encode('unicode_escape')
		tweet_text=tweet_text.decode('unicode_escape')
		tweet_text=re.sub('[;]+',' ',tweet_text)
		outtweets.append( [tweet.id_str, tweet.created_at,tweet_text , tweet.retweet_count ,tweet.retweeted,tweet.user.favourites_count,tweet.user.friends_count]) 
	# write the csv	
	
	with open('%s_test.csv'%screen_name, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text", "retweet_count", "tweet.retweeted" , "favourites_count" , "friends_count"])
		writer.writerows(outtweets)
	pass
	#tweets1 for testing data
	count = 4
	alltweets1=[]
	new_tweets1 = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
	alltweets1.extend(new_tweets1)
	oldest = alltweets1[-1].id - 1
	# if alltweets_dict[-1].id:
	# 	oldest_dict = alltweets_dict[-1].id - 1

	while len(new_tweets1) > 0 and count >0 :
		# print ("getting tweets before %s" % (oldest))
		count = count - 1 
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets1 = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		#save most recent tweets
		alltweets1.extend(new_tweets1)
		#update the id of the oldest tweet less one
		oldest = alltweets1[-1].id - 1
		print ("...%s downloaded so far for testing" % (len(alltweets1)))
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets1=[]
	for tweet in alltweets1:
		tweet_text=tweet.text.encode('unicode_escape')
		tweet_text=tweet_text.decode('unicode_escape')		
		tweet_text=re.sub('[;]+',' ',tweet_text)
		outtweets1.append( [tweet.id_str, tweet.created_at,tweet_text , tweet.retweet_count ,tweet.retweeted,tweet.user.favourites_count,tweet.user.friends_count]) 

	with open('%s_train.csv'%screen_name, 'a') as f:
		writer = csv.writer(f)
		writer.writerow(["id","created_at","text", "retweet_count", "tweet.retweeted" , "favourites_count" , "friends_count"])
		writer.writerows(outtweets1)
	pass



if __name__ == '__main__':
	with open('users1.csv', 'r') as f:
		reader = csv.reader(f)
		users = []
		for row in reader:
			users.append(row[0])
		for user in users:
			get_all_tweets(user)


	
