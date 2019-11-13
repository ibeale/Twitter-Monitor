import requests
import aiohttp
import asyncio
import lxml.html
from datetime import datetime
from utils import get_proxy
import webbrowser
from discord_webhook import DiscordEmbed, DiscordWebhook

global_id = 0
counter = 0
cookie_header_pairs = [
    {'cookie': {
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
        },
    'header': {
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
    },
    {'cookie': {
    '_ga': 'GA1.2.91199772.1573596064',
    '_gid': 'GA1.2.1475200831.1573596064',
    'gt': '1194374598470463488',
    'ct0': '177214c82a4c0b49c0c187220867803d',
    'kdt': 's1bLFJ3hNMatGwvRIDKo3nG2u6CKsfxi0HScGuxr',
    'remember_checked_on': '1',
    'lang': 'en',
    'dnt': '1',
    'personalization_id': 'v1_1yYxx2TANsPAinAw4DdlQQ==',
    'guest_id': 'v1%3A157359875564328763',
    '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCNSIy2FuAToMY3NyZl9p%250AZCIlZDFjODE2NjM5NWI3ZmJhZGU1MjdjMzNkZDMzMTViMjY6B2lkIiViM2Q1%250AYjFlNTIwNmYzZDRiMDUwODI5NjJkMjQxNDE2OToJdXNlcmwrCQBQVB5zOIIO--9cae7de50dd7e7eb54838170f239576879201ac3',
    'external_referer': 'padhuUp37zhJObO73CqsXZ0%2BLgQ%2Btq8mzPyoRg8vB3o%3D|0|8e8t2xd8A2w%3D',
    'ads_prefs': 'HBISAAA=',
    'twid': 'u=1045460130584612864',
    'u': '847f15ba60eefc338542be3df8e9f61a',
    'auth_token': '67eaf791c7b834eea8995d112cff5b04d59e4a1c',
    },
    'header': {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAF7aAAAAAAAASCiRjWvh7R5wxaKkFp7MM%2BhYBqM%3DbQ0JPmjU9F6ZoMhDfI4uTNAaQuTDm2uO9x3WFVr2xBZ2nhjdP0',
    'X-Twitter-Auth-Type': 'OAuth2Session',
    'X-Csrf-Token': '177214c82a4c0b49c0c187220867803d',
    'X-Twitter-Client-Version': 'Twitter-TweetDeck-blackbird-chrome/4.0.191015095829 web/',
    'Origin': 'https://tweetdeck.twitter.com',
    'Connection': 'keep-alive',
    'Referer': 'https://tweetdeck.twitter.com/',
    'TE': 'Trailers',
    },
    },
    {'cookie': {
    'personalization_id': 'v1_6+oJYDzT0lGxwvWSKrgCUA==',
    'guest_id': 'v1%3A157359918873531434',
    '_ga': 'GA1.2.1262219233.1573599186',
    '_gid': 'GA1.2.160722294.1573599186',
    '_gat': '1',
    'gt': '1194387693083353088',
    'ct0': 'a8c4636abb4a62d3d300c29193c17b43',
    '_twitter_sess': 'BAh7CiIKZmxhc2hJQzonQWN0aW9uQ29udHJvbGxlcjo6Rmxhc2g6OkZsYXNo%250ASGFzaHsABjoKQHVzZWR7ADoPY3JlYXRlZF9hdGwrCD0n0mFuAToMY3NyZl9p%250AZCIlYzBkMjYyMzhjMzQyM2Y3OGY2MGRiZjEzMzM0NjBkZmI6B2lkIiU1NTcz%250AMTBlNDY2YzU5YmIxZjAzNTQ3MTlmZDIzZmI3MToJdXNlcmwrCQDwVEpy9ooO--7daad1b6aefc70cef055b7a468f423c80e0eec5b',
    'external_referer': 'padhuUp37zhJObO73CqsXZ0%2BLgQ%2Btq8mzPyoRg8vB3o%3D|0|8e8t2xd8A2w%3D',
    'dnt': '1',
    'ads_prefs': 'HBISAAA=',
    'kdt': '4hU6W39Yyj6fN5vgW854pcoNb3OU0kVE4ylY2OXu',
    'remember_checked_on': '1',
    'twid': 'u=1047920834050846720',
    'u': '642e8b995a0aa941588f3443bc0f0b33',
    'auth_token': '709fbecd8b1999bf73714ae386b57fa326533d4c',
    'lang': 'en',
    },
    'header': {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
    'Accept': 'text/plain, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    'Authorization': 'Bearer AAAAAAAAAAAAAAAAAAAAAF7aAAAAAAAASCiRjWvh7R5wxaKkFp7MM%2BhYBqM%3DbQ0JPmjU9F6ZoMhDfI4uTNAaQuTDm2uO9x3WFVr2xBZ2nhjdP0',
    'X-Twitter-Auth-Type': 'OAuth2Session',
    'X-Csrf-Token': 'a8c4636abb4a62d3d300c29193c17b43',
    'X-Twitter-Client-Version': 'Twitter-TweetDeck-blackbird-chrome/4.0.191015095829 web/',
    'Origin': 'https://tweetdeck.twitter.com',
    'Connection': 'keep-alive',
    'Referer': 'https://tweetdeck.twitter.com/',
    'TE': 'Trailers',
    },
    },
]

class URL:
    def __init__(self):
        self.tco = None
        self.url = None

class Tweet:
    id: int
    text: str
    link_to_tweet: str
    link_to_pic: str
    username: str
    userid: str
    screen_name: str
    profile_image_url: str



    def __init__(self):
        self.links_in_tweet = []


async def fetch(session, headers, params, cookies):
    try:
        async with session.get("https://api.twitter.com/1.1/statuses/user_timeline.json", headers=headers, params=params, cookies=cookies) as response:
            return await response.json()
    except requests.exceptions as e:
        print(e)


# takes a url, and takes number of tweets to
async def get_recent(id, username, proxy, i):
    cookies = cookie_header_pairs[i]['cookie']

    headers = cookie_header_pairs[i]['header']

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
        session.proxies=proxy
        json_data = await fetch(session, headers, params, cookies)
        #global counter
        #counter += 1
        #print(f"Scrape number {counter}")

    try:
        new_tweet = Tweet()
        new_tweet.id = json_data[0]["id_str"]
        new_tweet.text = json_data[0]["full_text"]
        new_tweet.username = json_data[0]["user"]["name"]
        new_tweet.screen_name = json_data[0]["user"]["screen_name"]
        new_tweet.profile_image_url = json_data[0]["user"]["profile_image_url"]
        new_tweet.userid = json_data[0]["user"]["id_str"]
        urls = json_data[0]["entities"]["urls"]
        for url in urls:
            url_class = URL()
            url_class.tco = url["url"]
            url_class.url = url["expanded_url"]
            new_tweet.links_in_tweet.append(url_class)
        await print_new(new_tweet, username)
    except Exception as ke:
        print(ke)
        raise


async def print_new(new_tweet: Tweet, username):
    global global_id
    if(int(new_tweet.id) > global_id):
        if(new_tweet.links_in_tweet):
            for link in new_tweet.links_in_tweet:
                webbrowser.open_new_tab(link.url)
        global_id = int(new_tweet.id)
        post_to_webhook(new_tweet, username)
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
        url = "https://discordapp.com/api/webhooks/643995295541362688/dZCTze4i31lOp2sVHAyXRM-KfatO4oPVy7eurZlryPyjtzd4MXucQBYXHMOr1_1jvI5f"
        webhook = DiscordWebhook(url)
        embed = DiscordEmbed(title=f"Link to tweet", url=f"https://twitter.com/{new_tweet.screen_name}/status/{new_tweet.id}")
        embed.set_author(name=f"New tweet from {new_tweet.screen_name}", url=f'https://twitter.com/{new_tweet.screen_name}', icon_url=new_tweet.profile_image_url)
        embed.add_embed_field(name="Content: ", value=new_tweet.text, inline=True)
        embed.set_footer(text=f'Monitor by ike_on')
        webhook.add_embed(embed)
        webhook.execute()


def main():

    username = "stronomic"
    id = fetch_profile_id(username)
    n = 3
    i = 0
    j = 0
    max_i = len(cookie_header_pairs)
    while(True):
        proxy = get_proxy()
        loop = asyncio.get_event_loop()
        all_groups = asyncio.gather(*[get_recent(id, username, proxy, i) for _ in range(n)])
        try:
            loop.run_until_complete(all_groups)
        except Exception:
            print("Switching cookies")
            if(i >= max_i):
                i = 0
            else:
                i += 1


if __name__ == '__main__':
    main()
