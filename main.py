import urllib.request
import urllib.parse
import re
import tweepy


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


def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)

if __name__ == '__main__':

	consumer_key = ''
	consumer_secret = ''
	access_token = ''
	access_secret = ''

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)

	api = tweepy.API(auth)

	mentions = api.mentions_timeline(count=1)
	
	for mention in mentions:
		print(mention.user.name + " -> " + mention.text.replace("@YouTwubeBot", "").lower())
		reply(api, mention)
