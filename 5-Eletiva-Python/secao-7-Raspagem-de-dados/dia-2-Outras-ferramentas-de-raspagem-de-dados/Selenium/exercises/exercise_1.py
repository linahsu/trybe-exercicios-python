# Com o Selenium, faça uma requisição para o endpoint
# https://quotes.toscrape.com/ e imprima a primeira citação
# que aparece na página.

from selenium import webdriver
from selenium.webdriver.common.by import By

firefox = webdriver.Firefox()

response = firefox.get("https://quotes.toscrape.com/")

first_quote = firefox.find_element(
    By.CLASS_NAME, "text").get_attribute("innerHTML")

print(first_quote)
