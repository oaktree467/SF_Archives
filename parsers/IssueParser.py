import requests
from html.parser import HTMLParser

class IssueParser(HTMLParser):

    def __init__(self, test):
        super().__init__()
        self.openData = False
        self.url = ""
        self.str = ""
        self.vol = ""
        self.test = test

    def clean(self):
        self.openData = False
        self.url = ""
        self.str = ""
        self.vol = ""

    def handle_starttag(self, tag, attrs):
        for attr in attrs:
            if (('class' in attr) and ('notes' in attr)):
                self.openData = True

    def handle_endtag(self, tag):
        if self.openData and tag == "div":
            self.openData = False

    def handle_data(self, data):
        if self.openData:
            self.str = str(data)
            if ('Vol' in self.str) or ('Volume' in self.str):
                self.openData = False
            

    def parseDataStr(self):
        #print(self.str)
        self.str = self.str.split()
        ind = -1
        
        if "Vol" in self.str:
            ind = self.str.index("Vol")
        if "Volume" in self.str:
            ind = self.str.index("Volume")
        if (ind != -1):
            self.str = self.str[ind:(ind+4)]
            for x in range(0, len(self.str)):
                if ',' in self.str[x]:
                    ind2 = self.str[x].index(",")
                    self.str[x] = (self.str[x])[:(ind2)]
                if '.' in self.str[x]:
                    ind2 = self.str[x].index(".")
                    self.str[x] = (self.str[x])[:(ind2)]
            

    def run(self, url):
        self.clean()
        self.url = url

        #Use this block for testing
        #-----------------------------------------------
        if self.test:
            r = open("ISFDB_test_html/volumesample.html")
            self.feed(r.read())
        #-----------------------------------------------

        #Use this block for production
        #-----------------------------------------------
        else:
            r = requests.get(self.url)
            self.feed(r.text)
        #-----------------------------------------------
        
        self.parseDataStr()
        return self.str

#def main():
#    parser = IssueParser(True)
#    print(parser.run("ISFDB_test_html/volumesample.html"))

#if __name__ == "__main__":
#    main()




