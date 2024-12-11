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
        path = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(path,"month","star_month_text.txt")

    def delete_file(self):
        if os.path.exists(self.filename):  # 檢查檔案是否存在
            os.remove(self.filename)  # 刪除檔案

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
        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@soul.cats_tarot2017/post/"]').get_attribute("href")
                       for i in articles_list if f"{date.today().month}月份" in i.text and "全部上傳" not in i.text]
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
        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@astromatt888/post/"]').get_attribute("href") 
                       for i in articles_list if f"{date.today().month}月運勢" in i.text]
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
            title = i.find_element(By.CLASS_NAME,"subject")
            if "星座整體運勢" in title.text:
                link = title.get_attribute("href")
                driver.get(link)
                article = driver.find_element(By.CLASS_NAME,"post-content.main-content").find_elements(By.TAG_NAME,"p")
                article = "\n".join(i.text for i in article).split("✿ 個人網站 ✿")[0].strip("\n")+"：D"
                self.write(article)
                break

    def tang_month(self):
        url = f"https://www.tatlerasia.com/lifestyle/wellbeing/jesse-tang-horoscope-{date.today().strftime("%B").lower()}-2024-zh-hant"
        headers = {"user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        article = soup.find("div","article-container").text.split("繼續閱讀")[0].split("稿重點整理。")[1]
        article = re.sub(r"\s|1 / 1|[a-zA-Z ]+", "\n", article)+"：D"
        article = re.sub("\n+", "\n", article)
        self.write(article)

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
            article = "\n".join(article).split("【延伸閱讀】")[0]
            article = re.sub(r"[a-zA-Z@ ]+|\n+|//|廣告 - 內文未完請往下捲動", "\n", article)
            if re.search(r"fire|water|wind|earth", link):
                article_list.append(article)
                if len(article_list) == 4:
                    article = "\n".join(article_list)+"：D"
                    self.write(article)
            else:
                article = article.split("此內容來源為")[0]+"：D"
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

#主程式只要call這個function
def call_month():
    call = scrapying_month()
    call.delete_file()
    call.threads_soulcats_month()
    call.threads_astromatt_month()
    call.niunews_month()
    call.driver.close()
    call.tang_month()    
    call.elle_month()
    call.stargogo_month()
    print("month完成爬蟲")

if __name__ == "__main__":
    call_month()
