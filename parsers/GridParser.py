
import requests
from html.parser import HTMLParser

class GridParser(HTMLParser):

    def __init__(self, url, test):
        super().__init__()
        self.reset()
        self.openTags = []
        self.magGrid = []
        self.hrefOpen = False
        self.yearOpen = False
        self.year = 0
        self.url = url
        self.dict =  {'Issue':[],
        'URL':[]
        }
        self.test = test

    
    def handle_starttag(self, tag, attrs):
        if tag not in ['meta','link','img','input','li','br']:
            self.openTags.append(tag)
        if (tag == 'th' and ('class', 'year') in attrs):
            self.yearOpen = True
        if ((tag == 'a')):
            self.hrefOpen = True
            if 'table' in self.openTags:
                for attr in attrs:
                    if (attr[0] == "href"):
                        self.dict["URL"].append(attr[1])

    def handle_endtag(self, tag):
        if self.yearOpen:
            self.yearOpen = False
        if self.hrefOpen:
            self.hrefOpen = False

        self.openTags.remove(tag)

    def handle_data(self, data):
        if self.yearOpen:
            self.year = data
        if self.hrefOpen and 'table' in self.openTags:
            self.dict['Issue'].append(data + " " + self.year)

    def run(self):
        #Use this block for testing
        #-----------------------------------------------
        if self.test:
            r = open("ISFDB_test_html/issuegridsample.html")
            self.feed(r.read())
        #-----------------------------------------------

        #Use this block for production
        #-----------------------------------------------
        else:
            r = requests.get(self.url)
            self.feed(r.text)
        #-----------------------------------------------
        
        return self.dict



