import csv
import matplotlib.pyplot as plt
import re
sum = 0
count =0

with open("users1.csv", "r") as infile1:
	reader1 = csv.reader(infile1)
	for row1 in reader1:						#for each user
		name = row1[0] + '_train.csv'
		with open(name, "r") as infile:
			reader = csv.reader(infile)
			for row in reader:
				if row[3].isdigit():
					sum = sum + int(row[3].split()[0])
					count = count + 1

			average = sum/count
			dictionary = {} 
			dictionary1 = {} 
			count_dict = {}
			print (average)
		with open(name, "r") as infile:
			reader = csv.reader(infile)
			for row in reader:
				tweet_score=0
				if row[3].isdigit():
					tweet_score = (float(row[3])/average ) 
				
				for word in row[2].split():
					word1=re.sub('[^A-Za-z0-9]+', '', word)
					word2=re.sub('[^0-9]+', '', word1)
					if(word1!=word2):
						if word1 in dictionary:
							dictionary[word1] = dictionary[word1] + tweet_score
							count_dict[word1] = count_dict[word1] + 1
						else:  
							dictionary[word1] = tweet_score
							count_dict[word1] = 1



			#this loop calculates the average score for each word using the count of the word stored in count_dict
			with open(row1[0]+'_dict.csv','w') as outfile_dict:
				writer=csv.writer(outfile_dict)
				for k,v in dictionary.items():
					v1=dictionary[k]
					dictionary[k] = v1/ count_dict[k]
					writer.writerow([k,dictionary[k]])
				
		
			name2 = row1[0] + '_test.csv'
			with open(name2, "r") as infile2:
				reader = csv.reader(infile2)
				x = []
				y = []

				counter = 1

				for row in reader:
					sum = 0.0
					counter_word = 0
					for word in row[2].split():
						word1=re.sub('[^A-Za-z0-9]+', '', word)
						word2=re.sub('[^0-9]+', '', word1)
						if(word1!=word2):
							if word1 in dictionary.keys():
								sum = sum + dictionary[word1]
								counter_word = counter_word + 1

					tweet_score = 0
					if counter_word != 0:
						tweet_score = sum/counter_word
			
					
					expected_retweet_count = (tweet_score*average)
					#print (expected_retweet_count)

					if row[3].isdigit():
						if(expected_retweet_count==0):
							continue 
						tweet_interesting = int(row[3])/expected_retweet_count
						if(tweet_interesting>1):	
							print(row[2])
						test_result =   row1[0]+'_result.csv' 
						with open(test_result, "a") as outfile:
							writer = csv.writer(outfile)
							writer.writerow([row[2], row[3],tweet_score, expected_retweet_count, tweet_interesting])
							if(tweet_interesting!=0):
								y.append(float(tweet_interesting))
								x.append(counter)
								counter = counter + 1


		plt.plot(x,y)
		plt.show()						



							


