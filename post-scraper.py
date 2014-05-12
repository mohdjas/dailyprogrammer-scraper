import requests
import re
import os, sys, time

counter = 0

def getListing(after=""):
	"""Returns the page listing from Reddit in JSON format.	
	
	Keyword arguments:
	after -- fullname of the post after which the listing is to begin (default "")
	"""
	url =  'http://www.reddit.com/r/dailyprogrammer/.json?after=' + after
	headers = { 
		'User-Agent': 'Reddit Post Scraper 0.1' 
	}
	r = requests.get(url, headers=headers)												#Gets JSON file at url
	if r.status_code == requests.codes.ok:
		data = r.json()
		time.sleep(1)
		return data['data']
	else:
		print("Sorry, but there was an error retrieving the data!");
		return None
		
def savePostsToFile(posts):
	"""Saves each post in a file, split into folders named Easy, Medium or Hard.
	
	Keyword arguments:
	posts -- Children of the page listing
	"""
	
	global counter																								#Use the global counter variable
	
	for post in posts:
		postTitle = post['data']['title']														#Get the title of the post
		print(postTitle)
		
		try:																												#Check the title for the given expected pattern
			difficulty = re.compile('(easy|medium|intermediate|hard|difficult)', re.I).search(postTitle).group().lower()
			challenge = re.compile('#[0-9]+').search(postTitle).group()
			desc = post['data']['selftext']
			permalink = post['data']['permalink']
		except:																											#If an exception is raised, it means it is not a challenge post. So skip it.
			continue
		
		if difficulty == 'intermediate':														#Reducing the difficulty levels to three by combining synonyms
			difficulty = 'medium'
		if difficulty == 'difficult':
			difficulty = 'hard'
		
							
		if not os.path.exists(difficulty):													#Make a directory if it does not already exist
			os.makedirs(difficulty)					
		filename = difficulty + '/' + challenge + '.txt'						#Set pathname of file to be <difficulty>/<challengenumber>.txt
		if not os.path.exists(filename):
			f = open(filename, 'w')
			f.write(('http://www.reddit.com' + permalink + '\n\n').encode('utf-16'))
			f.write(desc.encode('utf-16'))
			f.close()
			counter += 1																							#Increment global counter to keep track of number of files we've written on this run
		
def main():
	listing = getListing()																				#Get the page listing from reddit using the API
	after = listing['after']																			#Get last post in listing for pagination
	while (after != None):
		savePostsToFile(listing['children'])												#Start saving the listing's children (ie, stories) to files
		listing = getListing(after)																	#Get the next listing after the post marked 'after'
		after = listing['after']
	print('Done! Wrote ' + str(counter) + ' files.')	
	
if __name__ == '__main__':
	main()
