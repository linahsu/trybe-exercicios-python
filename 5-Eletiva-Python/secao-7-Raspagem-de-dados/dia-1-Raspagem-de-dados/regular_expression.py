from parsel import Selector
import requests


response = requests.get("http://books.toscrape.com/")
selector = Selector(text=response.text)
# Extrai todos os preços da primeira página
prices = selector.css(".product_price .price_color::text").re(r"£\d+\.\d{2}")
print(prices)

response2 = requests.get(
    "http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
selector2 = Selector(text=response2.text)

# Extrai a descrição
description = selector2.css("#product_description ~ p::text").get()
print(description)

# "Fatiamos" a descrição removendo o sufixo
suffix = "...more"
if description.endswith(suffix):
    description = description[:-len(suffix)]
print(description)
