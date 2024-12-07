import os
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from datetime import date
import time
import re

class scrapying_month:
    def __init__(self):
        self.driver = uc.Chrome()
        self.filename = "month/star_month_text.txt"

    def delete_file(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def write(self,article):
        article = article.replace("白羊","牡羊").replace("魔羯","摩羯").replace("天平","天秤")
        with open(self.filename, "a", encoding = "UTF-8") as outputfile:
            return outputfile.write(article)

    def threads_soulcats_month(self):
        driver = self.driver
        driver.get("https://www.threads.net/@soul.cats_tarot2017")
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(5)

        articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z")
        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@soul.cats_tarot2017/post/"]').get_attribute("href") for i in articles_list if f"「{date.today().month}月份」" in i.text]
        if article_url:
            article_list = []
            for url in article_url:
                driver.get(url)
                time.sleep(3)
                article = driver.find_element(By.CLASS_NAME,"x1a6qonq").text
                article_list.append(article.strip("\n"))
            if article_list:
                article = "\n".join(article_list)+"：D"
                self.write(article)

    def threads_astromatt_month(self):
        driver = self.driver
        driver.get("https://www.threads.net/@astromatt888")
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(5)

        articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z")
        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@astromatt888/post/"]').get_attribute("href") for i in articles_list if f"{date.today().month}月運勢" in i.text]
        if article_url:
            article_list = []
            for url in article_url:
                driver.get(url)
                time.sleep(3)
                article = driver.find_element(By.CLASS_NAME,"x1a6qonq").text
                article_list.append(article.strip("\n"))
            if article_list:
                article = "\n".join(article_list)+"：D"
                self.write(article)

    def niunews_month(self):
        driver = self.driver
        driver.get("https://www.niusnews.com/search/new/%E6%98%9F%E5%BA%A7%E9%81%8B%E5%8B%A2")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(5)
        title_list = driver.find_elements(By.CSS_SELECTOR,"div.card.post-list-item")
        for i in title_list:
            title = i.find_element(By.CLASS_NAME,"subject").text
            if "星座整體運勢" in title:
                link = title.get_attribute("href")
                driver.get(link)
                article = driver.find_element(By.CLASS_NAME,"post-content.main-content").find_elements(By.TAG_NAME,"p")
                article = [i.text for i in article]
                article = "\n".join(article).split("關於星座專家")[0].strip("\n")+"：D"
                self.write(article)
                break

    def elle_month(self):
        url = "https://www.elle.com/tw/lovelife/horoscopes/"
        headers = {"user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.text, "html.parser")

        links = soup.find_all("a","ee4ms352")
        links = [i.get("href") for i in links if date.today().strftime("%B").lower() in i.get("href")]
        article_list = []
        for link in links:
            link = "https://www.elle.com"+link
            resp = requests.get(link, headers = headers)
            soup = BeautifulSoup(resp.text, "html.parser")
            article = soup.find("div","listicle-container").text.split("art-skvortsova//Getty Images")
            article = "\n".join(article).split("【延伸閱讀】")[0].split("廣告 - 內文未完請往下捲動")
            if re.search(r"fire|water|wind|earth", link):
                article_list.append("\n".join(article))
                if len(article_list) == 4:
                    article = "\n".join(article_list).strip("\n")+"：D"
                    self.write(article)
            if "sophiasastrology" in link:
                article = "\n".join(article).strip("\n")+"：D"
                self.write(article)

    def tang_month(self):
        url = f"https://www.tatlerasia.com/lifestyle/wellbeing/jesse-tang-horoscope-{date.today().strftime("%B").lower()}-2024-zh-hant"
        headers = {"user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        article = soup.find_all("p")
        article = [i.text for i in article]
        article = "\n".join(article).split("繼續閱讀")[0].split("1 / 1")[1:0]
        article = "\n".join(article).strip("\n")
        article = re.sub(r"\n+", "\n", article)+"：D"
        self.write(article)

    def stargogo_month(self):
        url = "https://www.stargogo.com/search/label/本月運勢?max-results=80"
        headers = {"user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        titles = soup.find_all("h2","post-title entry-title")
        links = []
        for title in titles:
            if str(date.today().month)+"月星座運勢" in title.text and "-" not in title.text:
                links.append(title.find("a").get("href"))

        if links:
            for link in links:
                resp = requests.get(link, headers = headers)
                soup = BeautifulSoup(resp.text, "html.parser")
                article = soup.find("div","post-body entry-content").text.split("MBTI")[0].split("【小鐵】")[0].strip("\n")
                article = re.sub(r"\n+", "\n", article)+"：D"
                self.write(article)
                time.sleep(2)

def call_month():
    call = scrapying_month()
    call.delete_file()
    call.threads_soulcats_month()
    call.threads_astromatt_month()
    call.niunews_month()
    call.driver.close()
    call.elle_month()
    call.tang_month()
    call.stargogo_month()


if __name__ == "__main__":
    call_month()
