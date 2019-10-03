import tweepy
from discord_webhook import DiscordEmbed, DiscordWebhook

webhook = DiscordWebhook(url='https://discordapp.com/api/webhooks/629370837052424193/iy1islXtvB-YuRCfwi1HYbQ1qGT_elSNfm2DSnDtwqOB9rUkt8_iXlM3oxDGX6U6VYvC')

class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        embed = DiscordEmbed(title='New Tweet',url='https://twitter.com/' + tweet.user.screen_name + '/status/' + str(tweet.id), description=tweet.text)
        embed.set_author(name=tweet.user.screen_name, url='https://twitter.com/' + str(tweet.user.screen_name), icon_url=str(tweet.user.profile_image_url))
        if("restock" in tweet.text):
            embed.add_embed_field(name='Restock Alert', value='@everyone')
        webhook.add_embed(embed)
        webhook.execute()

    def on_error(self, status):
        print("Error detected")



def main():

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("gV9PFuulfcJEJYYzJbLShjUg3", "QZmjT6elDX09vd14NDnq2xFngtSVN8nhmm36u17aeHM98oMitl")
    auth.set_access_token("326262955-MqsBTRFxmeSoSrvEdBtSrgXTr47rhyKPu6s9mCV8", "XyZ5jpX3xvpjv70ZP85twMpJdifdetcWlppi23QQXNlDP")



    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.get_user("IsaacBeale2")
    user_id = str(user.id)
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(follow=[user_id])



if __name__ == "__main__":
    main()
