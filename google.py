#!/usr/bin/env python
# -*- coding: UTF8 -*-

import threading
import re
import HTMLParser


htmlparser = HTMLParser.HTMLParser()

def get_preferences_signature(prefhtml):
    """get the sig hidden value in http://www.google.com/preferences"""

    sig = None
    for i in re.findall('<input(.*?)>', prefhtml):
        if re.findall('name="sig"', i):
            sig = re.findall('value="(.*?)"', i)[0]
            break
    if not sig:
        return
    return sig


get_preferences_link = lambda prefhtml: "http://www.google.com/setprefs?submit2=Save+Preferences&hl=en&uulo=0&muul=4_20&luul=&safeui=off&suggon=2&num=100&q=&prev=http%3A%2F%2Fwww.google.com%2F&sig=" + get_preferences_signature(prefhtml)


class Links(list):
    """Extract lionks from page"""

    def __init__(self, htmlpage):
        super(Links, self).__init__()
        l = re.findall("<h3 class=\"r\">(.*?)</h3>", htmlpage)
        l = [htmlparser.unescape(re.findall("href=\"(.*?)\"", i)[0]) for i in l]
        self.extend(l)



class LinkScraper(list):
    """scrape links from a google results page"""

    def __init__(self, arg):
        if type(arg) in (list, tuple):
            super(LinkScraper, self).__init__(arg)
        else:
            super(LinkScraper, self).__init__()
            r = Links(arg)
            self.extend(r)



