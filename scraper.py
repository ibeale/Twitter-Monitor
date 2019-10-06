import requests
import re
from bs4 import BeautifulSoup as bs


def get_timeline(url):
    # link to profile to monitor
    data = requests.get(url)
    all_tweets = []
    html = bs(data.text, 'html.parser')
    # get timeline
    timeline = html.select('#timeline li.stream-item')

    # makes a file to see the exact html we're working with, but formatted
    # nicely. Uncomment the next two lines to do so.

    # with open('html.html', 'w', encoding='utf-8') as f_out:
        # f_out.write(html.prettify())

    for tweet in timeline:
        tweet_id = tweet['data-item-id']
        tweet_link = '{}'.format(url) + '/status/' + tweet_id
        tweet_text = tweet.select('p.tweet-text')[0].get_text()

        # selects all <a> tags with class='twitter-timeline-link'
        redir_html = tweet.select('p.tweet-text a.twitter-timeline-link')
        in_tweet_links = []

        # if we find an <a> tag with the right class, iterate through
        # them to extract all href links. This gives us the t.co links
        if(redir_html):
            for link in redir_html:
                in_tweet_links.append(link['href'])

        # uses regex to find links to pic.twitter.com, since they're always
        # at the end, we can just use (.*)
        found = re.findall('pic.twitter.com/(.*)', tweet_text)

        # output to a list of dictionaries
        if(found):
            pic_link = 'pic.twitter.com/{}'.format(found[0])
            all_tweets.append({"id": tweet_id, "text": tweet_text, "link_to_tweet": tweet_link, "links": in_tweet_links, "link_to_pic": pic_link})
        else:
            all_tweets.append({"id": tweet_id, "text": tweet_text, "link_to_tweet": tweet_link, "links": in_tweet_links})

    print(all_tweets)


if __name__ == '__main__':
    url = 'https://twitter.com/IsaacBeale2'
    get_timeline(url)


# TO DO:
#   Decide whether to monitor RTs or not. (Currently pulls RTS)
#   store tweets from TL in a database and query it to see if its new
#   change so that it scrapes the newest tweet rather than the whole TL
#   asynchronously make multiple requests to a page
