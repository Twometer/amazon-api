import requests
from html.parser import HTMLParser
from dataclasses import dataclass

@dataclass
class Article:
    name: str
    asin: str
    price: float


class MyHTMLParser(HTMLParser):
    article: Article

    def __init__(self):
        HTMLParser.__init__(self)
        self.article = Article("", "", 0)

    def handle_starttag(self, tag, attrs):
        if((tag == "input" and self.getAttr(attrs, "type") == "hidden") or tag == "meta") :

            key = self.getAttr(attrs, "name")
            if(key == None):
                key = self.getAttr(attrs, "id")
            
            value = self.getAttr(attrs, "content")
            if(value == None):
                value = self.getAttr(attrs, "value")

            if(key == "attach-base-product-price"):
                self.article.price = float(value)
            elif(key == "ASIN"):
                self.article.asin = value
            elif(key == "title"):
                self.article.name = value

    def handle_endtag(self, tag):
        pass

    def handle_data(self, data):
        pass

    def getAttr(self, attrs, attr):
        for name, value in attrs:
            if name == attr:
                return value


class AmazonApi:
    def getArticleInformation(self, link):
        headers = {
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        contents = requests.get(link, headers=headers)
        parser = MyHTMLParser()
        parser.feed(contents.text)
        parser.close()
        return parser.article
