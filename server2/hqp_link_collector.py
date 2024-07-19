FILTERWORD = "pics.com"
import json
from datetime import datetime
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from datatypes import Source
from requests_html import HTMLSession
from tqdm import tqdm


def get_bookmarks():
    # Change this path to the location of your Brave bookmarks file
    bookmark_file = "/home/martin/.config/BraveSoftware/Brave-Browser/Default/Bookmarks"

    # Open the bookmarks file and load the JSON data
    with open(bookmark_file, "r") as f:
        data = json.load(f)

    # Traverse the JSON data to get the bookmarks
    bookmarks = []

    def traverse_bookmarks(node):
        if isinstance(node, dict):
            if "children" in node:
                for child in node["children"]:
                    traverse_bookmarks(child)
            elif "url" in node:
                bookmarks.append(node["url"])

    traverse_bookmarks(data["roots"]["bookmark_bar"])
    traverse_bookmarks(data["roots"]["other"])

    # Filter bookmarks that contain a specific keyword
    bookmarks = [x for x in bookmarks if FILTERWORD in x]
    return bookmarks


# def load_pre_existing_sources():
# 	sources = []

# 	# Load pre-existing sources from a JSON file
# 	if os.path.exists("sources.json"):
# 		with open("sources.json", "r") as f:
# 			collection = json.load(f)

# 		# Convert JSON data to a list of Source objects
# 		for source in collection:
# 			galleries = [Gallery(*gallery.values()) for gallery in source["galleries"]]
# 			src = Source(source["name"], galleries, source["weight"])
# 			sources.append(src)
# 	return sources


def flatten(l):
    # Flatten a list of lists into a single list
    return [item for sublist in l for item in sublist]


def get_new_id(sources):
    if len(sources) > 0:
        return max(x.id for x in sources) + 1
    return 0


def update_bookmark(sources, bookmark):
    session = HTMLSession()
    r = session.get(bookmark.url)
    # r.html.render(scrolldown=60, sleep=1)
    r.html.render()
    gallery_links = [link for link in r.html.links if "galleries" in link]
    known_gallery_names = {x.name for x in sources if x.type == "hq_pics_gallery"}
    # Look for available sources

    for gallery in tqdm(gallery_links):
        gallery_name = gallery.split("/")[-2]
        if gallery_name in known_gallery_names:
            continue

        try:
            r = requests.get(gallery)
            soup2 = BeautifulSoup(r.text)
            gallery_source = Source(
                f"{bookmark.name}:{gallery_name}",
                gallery,
                datetime.now(),
                get_new_id(sources),
                1,
                [],
                "hq_pics_gallery",
            )
            sources.append(gallery_source)
            gallery_source.attach_to_parent(bookmark)
            img_cnt = 0

            for a in soup2.find_all("a", href=True):
                link = a["href"]
                if "cdni" in link:
                    img_cnt += 1
                    # im_links.append(link)
                    img_src = Source(
                        gallery_source.name + ":" + str(img_cnt),
                        link,
                        datetime.now(),
                        get_new_id(sources),
                        1,
                        child_sources=[],
                        type="img_url",
                    )
                    sources.append(img_src)
                    img_src.attach_to_parent(gallery_source)

        except Exception as e:
            print(e)
    bookmark.last_update = datetime.now()


def update_data(sources: List[Source]):
    bookmark_urls = get_bookmarks()
    known_source_names = {x.name: x for x in sources if x.type == "hq_pics_bookmark"}
    # Add Unknown bookmarks
    for bookmark_url in tqdm(bookmark_urls):
        source_name = bookmark_url.split("/")[-2].replace("?q=", "")
        if source_name not in known_source_names:
            source = Source(
                name=source_name,
                url=bookmark_url,
                last_update=datetime(2000, 1, 1),
                id=get_new_id(sources),
                weight=1,
                child_sources=[],  # No parent
                type="hq_pics_bookmark",
            )
            sources.append(source)

    for bookmark in [source for source in sources if source.type == "hq_pics_bookmark"]:
        print(f"now updating {bookmark.name}")
        update_bookmark(sources, bookmark)

    return sources


if __name__ == "__main__":
    import datatypes

    sources = datatypes.readSources()
    sources = update_data(sources)
    datatypes.write(sources)
