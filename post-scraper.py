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
	
	#Gets JSON file at url
	r = requests.get(url, headers=headers)												
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
	
	#Use the global counter variable
	global counter																								
	
	for post in posts:
		#Get the title of the post
		postTitle = post['data']['title']														
		print(postTitle)
		
		#Check the title for expected pattern
		try:																												
			difficulty = re.compile('(easy|medium|intermediate|hard|difficult)', re.I).search(postTitle).group().lower()
			challenge = re.compile('#[0-9]+').search(postTitle).group()
			desc = post['data']['selftext']
			permalink = post['data']['permalink']
		#If an exception is raised, it means it is not a challenge post. So skip it.
		except:																											
			continue
		
		#Reducing the difficulty levels to three by combining synonyms
		if difficulty == 'intermediate':														
			difficulty = 'medium'
		if difficulty == 'difficult':
			difficulty = 'hard'
		
		#Make a directory if it does not already exist							
		if not os.path.exists(difficulty + '/' + challenge):				
			os.makedirs(difficulty + '/' + challenge)					
		#Set pathname of file to be <difficulty>/<challengenumber>/problem.txt
		filename = difficulty + '/' + challenge + '/problem.txt'		
		if not os.path.exists(filename):
			f = open(filename, 'w')
			f.write(('http://www.reddit.com' + permalink + '\n\n').encode('utf-16'))
			f.write(desc.encode('utf-16'))
			f.close()
			#Increment global counter to keep track of number of files we've written on this run
			counter += 1																							
		
def main():
	#Get the page listing from reddit using the API
	listing = getListing()																				
	#Get last post in listing for pagination
	after = listing['after']																			
	while (after != None):
		#Start saving the listing's children (ie, stories) to files
		savePostsToFile(listing['children'])				
		#Get the next listing after the post marked 'after'								
		listing = getListing(after)																	
		after = listing['after']
	print('Done! Wrote ' + str(counter) + ' files.')	
	
if __name__ == '__main__':
	main()
