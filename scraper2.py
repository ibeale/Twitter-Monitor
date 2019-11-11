import requests
import re
import time
import aiohttp
import asyncio
import lxml.html
from datetime import datetime
from bs4 import BeautifulSoup as bs
from utils import get_proxy_list, get_proxy
import webbrowser
from discord_webhook import DiscordEmbed, DiscordWebhook

global_id = 0
counter = 0

class URL:
    def __init__(self):
        self.tco = None
        self.url = None

class Tweet:
    id: int
    text: str
    link_to_tweet: str
    link_to_pic: str

    def __init__(self):
        self.links_in_tweet = []


async def fetch(session, headers, params, cookies):
    try:
        async with session.get("https://api.twitter.com/1.1/statuses/user_timeline.json", headers=headers, params=params, cookies=cookies) as response:
            return await response.json()
    except:
        print("Connection Error")


# takes a url, and takes number of tweets to
async def get_recent(id, username, proxy):
    include_retweets = False
    cookies = {
    'personalization_id': 'v1_RoPtB41SlpatEEfyYliIvA==',
    'guest_id': 'v1%3A155666719981665034',
    '_ga': 'GA1.2.134835951.1556667201',
    '_gid': 'GA1.2.255002093.1573504394',
    '_gat': '1',
    'gt': '1193990088880836608',
    'ct0': 'c020dcf4100acf64786504c35d9bfca3',
    '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCPGpK1xuAToMY3NyZl9p%250AZCIlOGI2Mjk1ZTRmZmExNzBiNmQyNWU1NzE5YjhlMGRmM2Q6B2lkIiVlYzAw%250ANjRmYWJiYWQ0OGI3ZjY3ZGU1NGNkYjA2MTUyMDoJdXNlcmkEq2ByEw%253D%253D--e3cf2769ceba6d2cbc3efe62de1d0b5cf1c951c8',
    'external_referer': 'padhuUp37zhJObO73CqsXZ0%2BLgQ%2Btq8mzPyoRg8vB3o%3D|0|8e8t2xd8A2w%3D',
    'ads_prefs': 'HBIRAAA=',
    'kdt': 'eKJU2EhRyGVOaDv25RPIEiDxbYgvsGBZT57XwVjE',
    'remember_checked_on': '1',
    'twid': 'u=326262955',
    'u': 'af8bb7eafbf989bb65037e7f76313476',
    'auth_token': '2d3e53cd2a20c0ed9750dae52a8d5eb511f02edc',
    'lang': 'en',
    }

    headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://tweetdeck.twitter.com/',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAF7aAAAAAAAASCiRjWvh7R5wxaKkFp7MM%2BhYBqM%3DbQ0JPmjU9F6ZoMhDfI4uTNAaQuTDm2uO9x3WFVr2xBZ2nhjdP0',
    'X-Twitter-Auth-Type': 'OAuth2Session',
    'X-Csrf-Token': 'c020dcf4100acf64786504c35d9bfca3',
    'X-Twitter-Client-Version': 'Twitter-TweetDeck-blackbird-chrome/4.0.191015095829 web/',
    'Origin': 'https://tweetdeck.twitter.com',
    'Connection': 'keep-alive',
    'TE': 'Trailers',
    }

    params = (
    ('count', '40'),
    ('include_my_retweet', '1'),
    ('since_id', '1193304574762852358'),
    ('include_rts', '1'),
    ('user_id', f'{id}'),
    ('cards_platform', 'Web-13'),
    ('include_entities', '1'),
    ('include_user_entities', '1'),
    ('include_cards', '1'),
    ('send_error_codes', '1'),
    ('tweet_mode', 'extended'),
    ('include_ext_alt_text', 'true'),
    ('include_reply_count', 'true'),
)
    async with aiohttp.ClientSession() as session:
        #session.proxies=proxy
        await asyncio.sleep(0.2)
        json_data = await fetch(session, headers, params, cookies)
        global counter
        counter += 1
        #print(f"Scrape number {counter}")

    # data = requests.get(url)
    try:
        new_tweet = Tweet()
        new_tweet.id = json_data[0]["id_str"]
        new_tweet.text = json_data[0]["full_text"]
        urls = json_data[0]["entities"]["urls"]
        for url in urls:
            url_class = URL()
            url_class.tco = url["url"]
            url_class.url = url["expanded_url"]
            new_tweet.links_in_tweet.append(url_class)
        await print_new(new_tweet, username)
    except:
        print(str(proxy) + "Failed")
        pass


async def print_new(new_tweet: Tweet, username):
    global global_id
    if(int(new_tweet.id) > global_id):
        if(new_tweet.links_in_tweet):
            for link in new_tweet.links_in_tweet:
                webbrowser.open_new_tab(link.url)
        global_id = int(new_tweet.id)
        #post_to_webhook(new_tweet, username)
        print(new_tweet.text)
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        print(current_time)

def fetch_profile_id(username):
    headers = {
    "accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "accept-encoding":"gzip, deflate, br",
    "accept-language":"en-US,en;q=0.9",
    "cache-control":"max-age=0",
    "referer":"https://twitter.com/login",
    "upgrade-insecure-requests":"1",
    'user-agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    }
    request = requests.get("https://www.twitter.com/"+str(username), headers=headers)
    html = lxml.html.fromstring(request.content)
    id_number = html.xpath('//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/@data-user-id')[0]
    return id_number

def post_to_webhook(new_tweet:Tweet, username):
        url = "https://discordapp.com/api/webhooks/629370837052424193/iy1islXtvB-YuRCfwi1HYbQ1qGT_elSNfm2DSnDtwqOB9rUkt8_iXlM3oxDGX6U6VYvC"
        webhook = DiscordWebhook(url)
        embed = DiscordEmbed(title=f"{username}", url=f"https://twitter.com/{username}/status/{new_tweet.id}")
        embed.add_embed_field(name="Content: ", value=new_tweet.text, inline=True)
        webhook.add_embed(embed)
        webhook.execute()

def main():
    usernames = [
                'stronomic'
                ]
    username = 'stronomic'

    start_time = time.time()
    id = fetch_profile_id(username)

    while(True):
        proxy = get_proxy()
        loop = asyncio.get_event_loop()
        all_groups = asyncio.gather(*[get_recent(id, username, proxy) for _ in range(10)])
        results = loop.run_until_complete(all_groups)
        # print("Took %s seconds to execute" % (time.time() - start_time))



if __name__ == '__main__':
    main()


# TO DO:
#   Decide whether to monitor RTs or not. (Currently pulls RTS)
#   store tweets from TL in a database and query it to see if its new
#   change so that it scrapes the newest tweet rather than the whole TL
#   asynchronously make multiple requests to a page
