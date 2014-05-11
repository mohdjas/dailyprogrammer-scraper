import requests
import re
import os, sys, time

counter = 0

def getListing(after=""):
	"""
		Returns the posts in a JSON format.	
	"""
	url =  'http://www.reddit.com/r/dailyprogrammer/.json?after=' + after
	headers = { 
		'User-Agent': 'Reddit Post Scraper 0.1' 
	}
	r = requests.get(url, headers=headers)
	if r.status_code == requests.codes.ok:
		data = r.json()
		time.sleep(1)
		return data['data']
	else:
		print("Sorry, but there was an error retrieving the data!");
		return None
		
def savePostsToFile(posts):
	"""
		Saves each post in a separate file after parsing it, split into folders named Easy, Medium or Hard. File is named after the challenge number.
	"""
	
	global counter
	
	for post in posts:
		postTitle = post['data']['title']
		print(postTitle)
		
		if post['data']['title'] == True:
			continue
		
		try:
			difficulty = re.compile('(easy|medium|intermediate|hard|difficult)', re.I).search(postTitle).group().lower()
			challenge = re.compile('#[0-9]+').search(postTitle).group()
			desc = post['data']['selftext']
			permalink = post['data']['permalink']
		except:
			continue
		
		if difficulty == 'intermediate':
			difficulty = 'medium'
		if difficulty == 'difficult':
			difficulty = 'hard'
		
							
		if not os.path.exists(difficulty):
			os.makedirs(difficulty)
		filename = difficulty + '/' + challenge + '.txt'
		if not os.path.exists(filename):
			f = open(filename, 'w')
			f.write(('http://www.reddit.com' + permalink + '\n\n').encode('utf-16'))
			f.write(desc.encode('utf-16'))
			f.close()
			counter += 1
		
def main():
	listing = getListing()
	after = listing['after']
	while (after != None):
		savePostsToFile(listing['children'])
		listing = getListing(after)
		after = listing['after']
	print('Done! Wrote ' + str(counter) + ' files.')	
	
if __name__ == '__main__':
	main()
