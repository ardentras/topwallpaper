from bs4 import BeautifulSoup
from bs4 import SoupStrainer
import requests
from datetime import date, timedelta

today = str(date.today())
yesterday = str(date.today() - timedelta(1))

user_agent = {'User-Agent': 'osx:com.shaunrasmusen.topwallpaper:v0.1 (by /u/YouAreNotHere)'}
reddit_soup = str(BeautifulSoup(requests.get("http://www.reddit.com/r/wallpapers/top/?sort=top&t=day", headers=user_agent).text,
                                "html.parser", parse_only=SoupStrainer("a")).prettify("ascii"))
link_start = reddit_soup.find("imgur.com/")
reddit_soup = reddit_soup[link_start:].split("\"")
imgur_pic = str(reddit_soup[0])

if imgur_pic[10:12] == "a/" or imgur_pic[10:18] == "gallery/":
    imgur_soup = str(BeautifulSoup(requests.get("http://" + imgur_pic).text,
                                   "html.parser", parse_only=SoupStrainer("img")).prettify("ascii"))
    link_start = imgur_soup.find("i.imgur.com/")
    imgur_soup = imgur_soup[link_start:].split("\"")
    if (str(imgur_soup[0])[-5] == "s"):
        imgur_pic = "http://" + str(imgur_soup[0])[:-5] + ".jpg"
    else:
        imgur_pic = "http://" + str(imgur_soup[0])[:-4] + ".jpg"
elif imgur_pic[-4] == ".":
    imgur_pic = "http://" + imgur_pic
else:
	imgur_pic = "http://" + imgur_pic + ".jpg"

print(imgur_pic)
import shutil
import os
user_path = str(os.getcwd())

picture_req = requests.get(imgur_pic, stream=True, headers=user_agent)
if picture_req.status_code == 200:
    with open('redditWallpaper-' + today + '.jpg', 'wb') as f:
        print("Downloading image from", imgur_pic + " to " + user_path + "/redditWallpaper-" + today + ".jpg")
        picture_req.raw.decode_content = True
        shutil.copyfileobj(picture_req.raw, f)

print("Changing background")

from subprocess import call
try:
    status = call("osascript -e \'tell application \"Finder\" to set desktop picture to POSIX file \"" + user_path + "/redditWallpaper-" + today + ".jpg\"\'", shell=True)
    if os.path.isfile("redditWallpaper-" + yesterday + ".jpg"):
        print("Deleting yesterday's wallpaper...")
        os.remove(user_path + "/redditWallpaper-" + yesterday + ".jpg")
except OSError as e:
    print(e)