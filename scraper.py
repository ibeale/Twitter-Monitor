import requests
import re
from bs4 import BeautifulSoup as bs


def main():
    # link to profile to monitor
    url = 'https://twitter.com/IsaacBeale2'
    data = requests.get(url)
    all_tweets = []
    html = bs(data.text, 'html.parser')
    # get timeline
    timeline = html.select('#timeline li.stream-item')
    for tweet in timeline:
        tweet_id = tweet['data-item-id']
        tweet_link = '{}'.format(url) + '/status/' + tweet_id
        tweet_text = tweet.select('p.tweet-text')[0].get_text()
        found = re.findall('pic.twitter.com/(.*)', tweet_text)
        if(found):
            pic_link = 'pic.twitter.com/{}'.format(found[0])
            all_tweets.append({"id": tweet_id, "text": tweet_text, "link_to_tweet": tweet_link, "link_to_pic": pic_link})
        else:
            all_tweets.append({"id": tweet_id, "text": tweet_text, "link_to_tweet": tweet_link})


    print(all_tweets)


if __name__ == '__main__':
    main()
