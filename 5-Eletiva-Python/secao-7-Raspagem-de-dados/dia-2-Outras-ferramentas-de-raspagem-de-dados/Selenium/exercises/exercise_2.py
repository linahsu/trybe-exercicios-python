# Imprima todos os parágrafos da página
# https://www.wikimetal.com.br/iron-maiden-scorpions-kiss-veja-melhores-albuns-1982/.

from selenium import webdriver
from selenium.webdriver.common.by import By

firefox = webdriver.Firefox()

firefox.get("https://www.wikimetal.com.br/iron-maiden-scorpions-kiss-veja-melhores-albuns-1982/") # noqa E501

p_tags = firefox.find_elements(By.TAG_NAME, "p")

for tag in p_tags:
    print(tag.get_attribute("innerHTML"))
