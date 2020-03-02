import requests
import aiohttp
import asyncio
import lxml.html
from datetime import datetime
from utils import get_proxy, get_proxy_list
import webbrowser
from dhooks import Webhook, Embed
import json
import random
import time


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


class Monitor:

    def __init__(self, cookie_pairs, usernames):
        self.global_id = 0
        self.cookie_header_pairs = json.load(open(cookie_pairs, "r"))
        self.usernames = usernames
        self.userIDs = [self.fetch_profile_id(
            username) for username in self.usernames]
        self.webhookURL = "https://discordapp.com/api/webhooks/644694815094734848/Y9Ixa2Wh7xpF7uQzbzX8uua-cERYWbtyoD3Xg8-7NJmUl47UTN_IF-QD5W_W-3oymtdy"

    async def fetch(self, session, headers, params, cookies):
        start_fetch = datetime.now().strftime("%I:%M:%S.%f %p")
        async with session.get("https://api.twitter.com/1.1/statuses/user_timeline.json", headers=headers, params=params, cookies=cookies) as response:
            end_fetch = datetime.now().strftime("%I:%M:%S.%f %p")
            return await response.json()

    async def get_recent(self, id, username, proxy, i):
        cookies = self.cookie_header_pairs[i]['cookie']

        headers = self.cookie_header_pairs[i]['header']

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
            session.proxies = proxy
            json_data = await self.fetch(session, headers, params, cookies)
            # f = open('timelinejson.txt', 'w')
            # json.dump(json_data, f, indent=4)

        try:
            new_tweet = Tweet()
            new_tweet.id = json_data[0]["id_str"]
            new_tweet.text = json_data[0]["full_text"]
            new_tweet.created_by = UserProfile(
                username=json_data[0]["user"]["name"], screen_name=json_data[0]["user"]["screen_name"], userid=json_data[0]["user"]["id_str"])
            new_tweet.created_by.profile_image_url = json_data[0]["user"]["profile_image_url"]
            new_tweet.created_by.description = json_data[0]["user"]["description"]
            new_tweet.created_by.location = json_data[0]["user"]["location"]
            for mentioned_user in json_data[0]["entities"]["user_mentions"]:
                new_tweet.mentioned_users.append(User(
                    username=mentioned_user["name"], userid=mentioned_user["id_str"], screen_name=mentioned_user["screen_name"]))
            urls = json_data[0]["entities"]["urls"]
            for url in urls:
                url_class = URL()
                url_class.tco = url["url"]
                url_class.url = url["expanded_url"]
                new_tweet.links_in_tweet.append(url_class)
            await self.print_new(new_tweet)
        except IndexError as e:
            print("Error Parsing")
            raise e

    def fetch_profile_id(self, username):
        headers = {
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "max-age=0",
            "referer": "https://twitter.com/login",
            "upgrade-insecure-requests": "1",
            'user-agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
        }
        request = requests.get("https://www.twitter.com/" +
                               str(username), headers=headers)
        html = lxml.html.fromstring(request.content)
        id_number = html.xpath(
            '//*[@id="page-container"]/div[1]/div/div[2]/div/div/div[2]/div/div/@data-user-id')[0]
        return id_number

    async def print_new(self, new_tweet: Tweet):
        if(int(new_tweet.id) > self.global_id):
            self.global_id = int(new_tweet.id)
            print(new_tweet.text)
            print(datetime.now().strftime("%I:%M:%S.%f %p"))
            await self.post_to_webhook(new_tweet)
            if(new_tweet.links_in_tweet):
                for link in new_tweet.links_in_tweet:
                    webbrowser.open_new_tab(link.url)

    async def post_to_webhook(self, new_tweet: Tweet):
        start_time = time.time()
        text = new_tweet.text
        webhook = Webhook.Async(self.webhookURL)
        embed = Embed(title=f"Link to tweet",
                      url=f"https://twitter.com/{new_tweet.created_by.screen_name}/status/{new_tweet.id}")
        embed.set_author(name=f"New tweet from {new_tweet.created_by.screen_name}",
                         url=f'https://twitter.com/{new_tweet.created_by.screen_name}', icon_url=new_tweet.created_by.profile_image_url)
        for mentioned_user in new_tweet.mentioned_users:
            text = text.replace(f"@{mentioned_user.screen_name}",
                                f"[@{mentioned_user.screen_name}](https://twitter.com/{mentioned_user.screen_name})")
        embed.add_field(name="Content: ", value=text, inline=True)
        for url in new_tweet.links_in_tweet:
            embed.add_field(name="Link Found: ", value=f"{url.url}")
        embed.set_footer(text=f'Monitor by ike_on')
        await webhook.send(embed=embed)
        print(f"Took {time.time() - start_time} seconds to send to webhook")
        for url in new_tweet.links_in_tweet:
            if("discord" in url.url):
                await webhook.send(f"Possible discord invite found: {url.url}")
        await webhook.close()

    def run(self):
        n = 2
        max_i = len(self.cookie_header_pairs)
        i = random.randint(0, (max_i - 1))
        print(f"Using cookies {i}")
        loop = asyncio.get_event_loop()
        proxy_list = get_proxy_list()
        max_j = len(proxy_list)
        j = random.randint(0, (max_j - 1))
        while(True):
            start_time = time.time()
            proxy = proxy_list[j]
            all_groups = asyncio.gather(
                *[self.get_recent(self.userIDs[j], self.usernames[j], proxy, i) for j in range(len(self.usernames))])
            try:
                loop.run_until_complete(all_groups)
            except Exception as e:
                print(e)
                print(f"Cookie {i} not working. Switching cookies and proxy")
                j = random.randint(0, (max_j - 1))
                if(i >= max_i):
                    i = 0
                else:
                    i += 1
                print(f"Using cookies {i} and proxy {proxy_list[j]}")


usernames = ["destroyerbots", "stronomic"]
monitor = Monitor("cookie_pairs.json", usernames)
monitor.run()
