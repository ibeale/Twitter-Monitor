import tweepy


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, api):
        self.api = api
        self.me = api.me()

    def on_status(self, tweet):
        print(f"{tweet.user.name}:{tweet.text}")

    def on_error(self, status):
        print("Error detected")


def main():

    # Authenticate to Twitter
    auth = tweepy.OAuthHandler("gV9PFuulfcJEJYYzJbLShjUg3", "QZmjT6elDX09vd14NDnq2xFngtSVN8nhmm36u17aeHM98oMitl")
    auth.set_access_token("326262955-MqsBTRFxmeSoSrvEdBtSrgXTr47rhyKPu6s9mCV8", "XyZ5jpX3xvpjv70ZP85twMpJdifdetcWlppi23QQXNlDP")


    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
    user = api.get_user("stronomic")
    user_id = str(user.id)
    tweets_listener = MyStreamListener(api)
    stream = tweepy.Stream(api.auth, tweets_listener)
    stream.filter(follow=[user_id])
    print("hi")


if __name__ == "__main__":
    main()
