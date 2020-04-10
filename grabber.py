# -*- coding: utf-8 -*-
import sys
import re
import os
import json

import requests
import textwrap
from bs4 import BeautifulSoup


class GrabberArticle:
    """url - article address.
       filename - file name used to save. Matches the last item in the URL path.
       path - path to save article. Match with URL paths ([CUR_DIR]/host/path1/path2/...)
       content_tags - tags for article processing.
       wrap - сolumn width.
    """
    # Set default values:
    url = ""
    filename = ""
    path = ""
    content_tags = ['p']
    wrap = 80

    def __init__(self, url_address):
        self.url = url_address
        # Get path and filename for saving article by splitting URL.
        # If the URL ends with some.html, then the previous (-2) element
        # of the path is taken to form the path and the filename = some.html.txt respectively.
        path_arr = self.url.split('/')
        if path_arr[-1] != '':
            self.filename = path_arr[-1] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-1])
        else:
            self.filename = path_arr[-2] + ".txt"
            self.path = os.getcwd() + "/".join(path_arr[1:-2])
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def write_in_file(self, text):
        # Write file in path, stored in self.path: "[CUR_DIR]/host/path_item1/path_item2/..."
        # with filename, stored in self.filename
        file = open(str(self.path) + '/' + str(self.filename), mode="w")
        file.write(text)
        file.close()

    def get_text(self):
        # return clear text of article
        r = requests.get(self.url).text
        soup = BeautifulSoup(r, 'html.parser')
        content = soup.find_all(self.content_tags)
        # Getting the entire tag content, described in self.content_tags.
        wrapped_text = ""
        for p in content:
            # Skipping empty tags.
            if p.text != '':
                # Formatting links into view: [link]
                links = p.find_all('a')
                if links != '':
                    for link in links:
                        p.a.replace_with(link.text + str("[" + link['href'] + "]"))
                # Text formatting in tags according to сolumn width (self.wrap).
                wrapped_text += ''.join(textwrap.fill(p.text, self.wrap)) + "\n\n"
        self.write_in_file(wrapped_text)


if __name__ == "__main__" and (len(sys.argv) > 1):
    try:
        mr = GrabberArticle(sys.argv[1])
        mr.get_text()
        print("Successfully processed")
    except Exception:
        print("Error processing URL")
