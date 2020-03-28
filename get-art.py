import os
import requests
import json
import random

from collections import OrderedDict
from flask import Flask, render_template, send_from_directory
from dotenv import load_dotenv


app = Flask(__name__)

load_dotenv()


def authenticate():

    client_id = os.getenv("client_id", None)
    client_secret = os.getenv("client_secret", None)
    print(client_id, client_secret)
    return client_id, client_secret


def get_xapp_token(client_id, client_secret):

    token_url = "https://api.artsy.net/api/tokens/xapp_token"
    payload = {"client_id": client_id, "client_secret": client_secret}
    get_token = requests.post(token_url, params=payload)
    xapp_token = json.loads(get_token.text)["token"]
    return xapp_token


def randomize():

    # Artsy number of artworks taken from: https://developers.artsy.net/
    artwork_number = 27577

    index = random.randrange(artwork_number)
    return index


def get_artist(xapp_token, artwork_id):

    url = "https://api.artsy.net/api/artists"
    payload = {"xapp_token": xapp_token, "artwork_id": artwork_id}
    response = requests.get(url, params=payload)
    data = json.loads(response.text, object_pairs_hook=OrderedDict)
    
    if data["_embedded"]["artists"]:
        artist = data["_embedded"]["artists"][0]["name"]
    else:
        artist = "Unknown"
    
    return artist


def get_art_of_the_moment(xapp_token, index):

    url = "https://api.artsy.net/api/artworks"
    payload = {"xapp_token": xapp_token, "offset": index, "size": "1"}
    response = requests.get(url, params=payload)
    data = json.loads(response.text, object_pairs_hook=OrderedDict)

    artwork = data["_embedded"]["artworks"][0]

    title = "Unknown" if artwork["title"] == "" else artwork["title"]
    date = "Unknown" if artwork["date"] == "" else artwork["date"]
    artist = "Unknown" if get_artist(xapp_token, artwork["id"]) == "" else get_artist(xapp_token, artwork["id"])
    image_link_large = "https://www.artsy.net/images/icon-152.png" if artwork["_links"]["image"]["href"] == "" else artwork["_links"]["image"]["href"].replace("{image_version}","large")
    image_link_normalized = "https://www.artsy.net/images/icon-152.png" if artwork["_links"]["image"]["href"] == "" else artwork["_links"]["image"]["href"].replace("{image_version}","normalized")
    artsy_link = "https://www.artsy.net" if artwork["_links"]["permalink"]["href"] == "" else artwork["_links"]["permalink"]["href"]

    return {
        "title": title, 
        "date": date, 
        "artist": artist, 
        "image_link_large": image_link_large, 
        "image_link_normalized": image_link_normalized, 
        "artsy_link": artsy_link
    }


@app.route("/")
def render():
    client_id, client_secret = authenticate()
    xapp_token = get_xapp_token(client_id, client_secret)
    data = get_art_of_the_moment(xapp_token, randomize())
    return render_template("index.html", **data)

@app.route("/css/<path>")
def send_css(path):
    return send_from_directory("css", path)

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template("500.html"), 500
