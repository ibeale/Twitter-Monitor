import requests
import aiohttp
import asyncio
import lxml.html
from datetime import datetime
from utils import get_proxy
import webbrowser
from discord_webhook import DiscordEmbed, DiscordWebhook
import json
import time

global_id = 0
counter = 0
json_cookie_pairs = open("cookie_pairs.json", "r")
cookie_header_pairs = json.load(json_cookie_pairs)

class URL:
    def __init__(self):
        self.tco = None
        self.url = None

class User:
    username: str
    userid: str
    screen_name: str

    def __init__(self, username=None, userid=None, screen_name=None):
        self.username = username
        self.userid = userid
        self.screen_name = screen_name


class UserProfile(User):
    description: str
    location: str
    profile_image_url: str

    def __init__(self, username=None, userid=None, screen_name=None):
        self.urls = []
        super().__init__(username, userid, screen_name)

class Tweet:
    id: int
    text: str
    link_to_tweet: str
    link_to_pic: str
    created_by: UserProfile



    def __init__(self):
        self.links_in_tweet = []
        self.mentioned_users = []


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
        new_tweet.created_by = UserProfile(username=json_data[0]["user"]["name"], screen_name=json_data[0]["user"]["screen_name"], userid=json_data[0]["user"]["id_str"])
        new_tweet.created_by.profile_image_url = json_data[0]["user"]["profile_image_url"]
        new_tweet.created_by.description = json_data[0]["user"]["description"]
        new_tweet.created_by.location = json_data[0]["user"]["location"]
        for mentioned_user in json_data[0]["entities"]["user_mentions"]:
            new_tweet.mentioned_users.append(User(username=mentioned_user["name"], userid=mentioned_user["id_str"], screen_name=mentioned_user["screen_name"]))
        urls = json_data[0]["entities"]["urls"]
        for url in urls:
            url_class = URL()
            url_class.tco = url["url"]
            url_class.url = url["expanded_url"]
            new_tweet.links_in_tweet.append(url_class)
        print_new(new_tweet)
    except Exception as ke:
        print(ke)
        raise


def print_new(new_tweet: Tweet):
    global global_id
    if(int(new_tweet.id) > global_id):
        post_start = time.time()
        print(new_tweet.text)
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        print(current_time)
        global_id = int(new_tweet.id)
        if(new_tweet.links_in_tweet):
            for link in new_tweet.links_in_tweet:
                webbrowser.open_new_tab(link.url)
        post_to_webhook(new_tweet)
        print(f"Took {time.time() - post_start} to post")


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


def post_to_webhook(new_tweet:Tweet):
        url = "https://discordapp.com/api/webhooks/629370837052424193/iy1islXtvB-YuRCfwi1HYbQ1qGT_elSNfm2DSnDtwqOB9rUkt8_iXlM3oxDGX6U6VYvC"
        text = new_tweet.text
        webhook = DiscordWebhook(url)
        embed = DiscordEmbed(title=f"Link to tweet", url=f"https://twitter.com/{new_tweet.created_by.screen_name}/status/{new_tweet.id}")
        embed.set_author(name=f"New tweet from {new_tweet.created_by.screen_name}", url=f'https://twitter.com/{new_tweet.created_by.screen_name}', icon_url=new_tweet.created_by.profile_image_url)
        for mentioned_user in new_tweet.mentioned_users:
            text = text.replace(f"@{mentioned_user.screen_name}", f"[@{mentioned_user.screen_name}](https://twitter.com/{mentioned_user.screen_name})")
        embed.add_embed_field(name="Content: ", value=new_tweet.text, inline=True)
        for url in new_tweet.links_in_tweet:
            embed.add_embed_field(name="Link Found: ", value=f"{url.url} - [tco]({url.tco})")
        embed.set_footer(text=f'Monitor by ike_on')
        webhook.add_embed(embed)
        webhook.execute()


def main():

    username = "juicynotify"
    id = fetch_profile_id(username)
    n = 3
    i = 0
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
