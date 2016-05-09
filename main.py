import urllib.request
import urllib.parse
import re
import tweepy
from time import sleep

def search(text):

	query_string = urllib.parse.urlencode({"search_query": text})
	html_content = urllib.request.urlopen("http://www.youtube.com/results?" + query_string)
	search_results = re.findall(r'href=\"\/watch\?v=(.{11})', html_content.read().decode())
	video = "http://www.youtube.com/watch?v=" + search_results[0]

	return video


def reply(api, mention):

	video = search(mention.text.replace("@YouTwubeBot", "").lower())
	id = mention.id
	user = mention.user.screen_name
	api.update_status("Voilà la vidéo, @" + user + "-> " + video, id)

if __name__ == '__main__':

	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_secret = ''

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	while True:
		try:
			mentions = api.mentions_timeline(count=1)
			for mention in mentions:
				print(mention.user.name + " -> " + mention.text.replace("@YouTwubeBot", "").lower())
				reply(api, mention)
			sleep(60)
		except:
			rate = api.rate_limit_status()
			print (rate['resources']['statuses']['/statuses/mentions_timeline'])
			sleep(15 * 60)