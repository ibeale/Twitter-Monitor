import sys
import time
import socket
import random
import colored
import linecache
from colored import stylize
from datetime import datetime

class Logger:

    def __init__(self, title, id_num=None):
        if id_num == None:
            self.identifier = "[{}]".format(title)
        else:
            self.identifier = "[{} {}]".format(title, id_num)

    def info(self, msg, tag="INFO"):
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        text = "[{}] {} [{}] → {}".format(current_time, self.identifier, tag, msg)
        print(stylize(text, colored.fg("cyan")))

    def error(self, msg, tag="ERROR"):
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")

        exc_type, exc_obj, tb = sys.exc_info()
        f = tb.tb_frame
        lineno = tb.tb_lineno
        filename = f.f_code.co_filename
        linecache.checkcache(filename)
        line = linecache.getline(filename, lineno, f.f_globals)

        msg = msg + f"\n{lineno} → {line}"

        text = "[{}] {} [{}] → {}".format(current_time, self.identifier, tag, msg)
        print(stylize(text, colored.fg("red")))

        hook = Webhook("https://discordapp.com/api/webhooks/633365674592305173/oZZVdJNQOxByuJTT93_CzbFiZ-Wi-j9Zre26zrHpmkDXjHsXEyAoFOU_it-4DVW3pQAC")
        embed = Embed(
            color = "10027008",
            description = msg
        )
        embed.set_author(str(socket.gethostname()))
        embed.set_title(f":warning:Error from **{self.identifier}**:warning:")
        hook.send(embed=embed)

    def success(self, msg ,tag="SUCCESS"):
        current_time = datetime.now().strftime("%I:%M:%S.%f %p")
        text = "[{}] {} [{}] → {}".format(current_time, self.identifier, tag, msg)
        print(stylize(text, colored.fg("green")))

def get_proxy():
    proxies = open("proxies.txt").read().splitlines()
    proxy = random.choice(proxies)
    split = proxy.split(":")
    ip = split[0]
    port = split[1]
    try:
        user = split[2]
        password = split[3]
        dict = {
        "http": f"http://{user}:{password}@{ip}:{port}",
        "https": f"https://{user}:{password}@{ip}:{port}",
        }
    except:
        dict = {
        "http": f"http://{ip}:{port}",
        "https": f"https://{ip}:{port}",
        }
    return dict

def get_proxy_list():
    list = []
    proxies = open("proxies.txt").read().splitlines()
    for proxy in proxies:
        split = proxy.split(":")
        ip = split[0]
        port = split[1]
        try:
            user = split[2]
            password = split[3]
            dict = {
            "http": f"http://{user}:{password}@{ip}:{port}",
            "https": f"https://{user}:{password}@{ip}:{port}",
            }
        except:
            dict = {
            "http": f"http://{ip}:{port}",
            "https": f"https://{ip}:{port}",
            }
        list.append(dict)
    return list

if __name__ == "__main__":
    logger = Logger("TASK", "1")
    logger.info("info")
    # logger.error("error")
    logger.success("success")
    print(get_proxy())
