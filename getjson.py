import requests
import json

cookies =  {
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
('user_id', '1139036457048379397'),
('cards_platform', 'Web-13'),
('include_entities', '1'),
('include_user_entities', '1'),
('include_cards', '1'),
('send_error_codes', '1'),
('tweet_mode', 'extended'),
('include_ext_alt_text', 'true'),
('include_reply_count', 'true'),
)

response = requests.get("https://api.twitter.com/1.1/statuses/user_timeline.json", headers=headers, params=params, cookies=cookies)
json_data = response.json()

f = open('timelinejson.txt', 'w')
json.dump(json_data, f)
