import requests
import aiohttp
import asyncio
import lxml.html
from datetime import datetime
from utils import get_proxy
import webbrowser
from discord_webhook import DiscordEmbed, DiscordWebhook
import json

global_id = 0
counter = 0
json_cookie_pairs = open("cookie_pairs.json", "r")
cookie_header_pairs = json.load(json_cookie_pairs)

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
