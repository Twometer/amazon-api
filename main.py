from api import AmazonApi

AmazonApi = AmazonApi()

article = AmazonApi.getArticleInformation("https://www.amazon.de/Sony-Systemkamera-Megapixel-Display-schwarz/dp/B01BMAIEFE")
print(article.price)
