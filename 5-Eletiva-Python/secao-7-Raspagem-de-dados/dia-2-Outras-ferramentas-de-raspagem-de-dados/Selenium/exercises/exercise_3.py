# Utilizando a ferramenta Selenium, no site https://diolinux.com.br/, faça a
# extração dos campos título e link para cada post da página inicial.

from selenium import webdriver
from selenium.webdriver.common.by import By

firefox = webdriver.Firefox()


def scrape_url(url):
    firefox.get(url)

    posts = firefox.find_elements(By.CLASS_NAME, "inhype-post-details")

    posts_list = []

    for post in posts:
        post_info = {}

        post_info["title"] = (
            post.find_element(By.TAG_NAME, 'h3')
            .find_element(By.TAG_NAME, "a")
            .get_attribute("innerHTML")
        )
        post_info["link"] = (
            post.find_element(By.TAG_NAME, 'h3')
            .find_element(By.TAG_NAME, "a")
            .get_attribute("href")
        )

        posts_list.append(post_info)

    return posts_list


print(scrape_url("https://diolinux.com.br/"))
