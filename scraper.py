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
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> d1359045475f6e3a4849feaac3f21d6ba57fce48

    # makes a file to see the exact html we're working with, but formatted
    # nicely. Uncomment the next two lines to do so.

    # with open('html.html', 'w', encoding='utf-8') as f_out:
        # f_out.write(html.prettify())

<<<<<<< HEAD
=======
=======
    with open('html.html', 'w', encoding='utf-8') as f_out:
        f_out.write(html.prettify())
>>>>>>> db3913dd1acdf3610ce4ba33f1fcf9a0f51c07e4
>>>>>>> d1359045475f6e3a4849feaac3f21d6ba57fce48
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
<<<<<<< HEAD
        # at the end, we can just use (.*)
=======
<<<<<<< HEAD
        # at the end, we can just use (.*)
=======
        # at the end, we can just use .*
>>>>>>> db3913dd1acdf3610ce4ba33f1fcf9a0f51c07e4
>>>>>>> d1359045475f6e3a4849feaac3f21d6ba57fce48
        found = re.findall('pic.twitter.com/(.*)', tweet_text)

        # output to a list of dictionaries
        if(found):
            pic_link = 'pic.twitter.com/{}'.format(found[0])
            all_tweets.append({"id": tweet_id, "text": tweet_text, "link_to_tweet": tweet_link, "links": in_tweet_links, "link_to_pic": pic_link})
        else:
            all_tweets.append({"id": tweet_id, "text": tweet_text, "link_to_tweet": tweet_link, "links": in_tweet_links})
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======

>>>>>>> db3913dd1acdf3610ce4ba33f1fcf9a0f51c07e4
>>>>>>> d1359045475f6e3a4849feaac3f21d6ba57fce48

    print(all_tweets)


if __name__ == '__main__':
    url = 'https://twitter.com/IsaacBeale2'
    get_timeline(url)
<<<<<<< HEAD
=======
<<<<<<< HEAD
>>>>>>> d1359045475f6e3a4849feaac3f21d6ba57fce48


# TO DO:
#   Decide whether to monitor RTs or not. (Currently pulls RTS)
#   store tweets from TL in a database and query it to see if its new
#   change so that it scrapes the newest tweet rather than the whole TL
#   asynchronously make multiple requests to a page
<<<<<<< HEAD
=======
=======
>>>>>>> db3913dd1acdf3610ce4ba33f1fcf9a0f51c07e4
>>>>>>> d1359045475f6e3a4849feaac3f21d6ba57fce48
