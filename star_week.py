import os
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from datetime import date, timedelta
import time
import re

class scrapying_week:
    def __init__(self):
        self.driver = uc.Chrome()
        path = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(path,"week","star_week_text.txt")
        monday = date.today() - timedelta(days=date.today().weekday())
        self.month1 = monday.month
        self.month2 = (monday-timedelta(days=1)).month
        self.day1 = monday.day
        self.day2 = (monday-timedelta(days=1)).day
        self.pattern1 = rf"(?<![-～]){self.month1}[\u4e00-\u9fa5/.]{{1}}0?{self.day1}(?!\d)"
        self.pattern2 = rf"(?<![-～]){self.month2}[\u4e00-\u9fa5/.]{{1}}0?{self.day2}(?!\d)"

    def delete_file(self):
        if os.path.exists(self.filename):  # 檢查檔案是否存在
            os.remove(self.filename)  # 刪除檔案

    def write(self,article):
        article = article.replace("白羊","牡羊").replace("魔羯","摩羯").replace("天平","天秤")
        with open(self.filename, "a", encoding = "UTF-8") as outputfile:
            return outputfile.write(article)

    def threads_blaire_week(self):
        driver = self.driver
        driver.get("https://www.threads.net/@blaire___0")
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(5)
        articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z")
        driver.execute_script("window.scrollTo(400, 1000);")
        time.sleep(5)
        articles_list += driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z")

        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@blaire___0/post/"]').get_attribute("href") 
                       for i in articles_list
                       if re.search(f"{self.pattern1}|{self.pattern2}",i.text) 
                       and "星座運勢" in i.text and "唐綺陽" not in i.text]
        article_url = list(set(article_url))

        if article_url:
            for url in article_url:
                driver.get(url)
                time.sleep(3)
                article = driver.find_element(By.CLASS_NAME,"x1a6qonq").text+"：D"
                self.write(article)

    def threads_singingbb_week(self):
        driver = self.driver
        driver.get("https://www.threads.net/@singingbb___")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(5)

        articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z")
        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@singingbb___/post/"]').get_attribute("href") 
                       for i in articles_list if re.search(self.pattern1,i.text)]
        if article_url:
            article_list = []
            for url in article_url:
                driver.get(url)
                time.sleep(3)

                article = driver.find_elements(By.CLASS_NAME,"x1a6qonq")[0:3]
                article_list.append("\n".join(i.text for i in article).strip("\n"))
            if article_list:
                article = "\n".join(article_list)+"：D"
                self.write(article)

    def threads_v_week(self):
        driver = self.driver
        driver.get("https://www.threads.net/@tarot_from_heart")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(5)

        articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z")
        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@tarot_from_heart/post/"]').get_attribute("href") 
                       for i in articles_list if re.search(self.pattern1,i.text)]
        if article_url:
            for url in article_url:
                driver.get(url)
                time.sleep(3)
                article = driver.find_elements(By.CLASS_NAME,"x1a6qonq")[0:3]
                article = "\n".join(i.text for i in article)+"：D"
                self.write(article)

    def threads_yusitaluo_week(self):
        driver = self.driver
        driver.get("https://www.threads.net/@yusitaluo")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(5)

        articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR,"div.x9f619.x1n2onr6.x1ja2u2z")
        article_url = [i.find_element(By.CSS_SELECTOR,'a[href*="/@yusitaluo/post/"]').get_attribute("href") 
                       for i in articles_list if re.search(self.pattern2,i.text)]
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

    def vogue_week(self):
        if self.day1 < 10:
            website = ["星座運勢",f"v星座-唐綺陽-星座周運-{self.month1}0{self.day1}"]
        else:
            website = ["星座運勢",f"v星座-唐綺陽-星座周運-{self.month1}{self.day1}"]
        driver = self.driver
        for i in website:
            url = f"https://www.vogue.com.tw/article/{i}"
            driver.get(url)
            time.sleep(5)

            article = driver.find_elements(By.CLASS_NAME,"body__inner-container")
            article = "\n".join(i.text for i in article).split("繼續閱讀")[0].split("相關文章")[0]+"：D"
            article = re.sub(r"WATCH.+Vogue Taiwan","",article,flags=re.DOTALL)
            self.write(article)

    def ptt_week(self):
        url = "https://www.ptt.cc/bbs/Zastrology/index.html"
        headers = {"user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        titles = soup.find_all("div","title")
        links = []
        for title in titles:
            if re.search(f"{self.pattern1}|{self.pattern2}",title.text):
                links.append("https://www.ptt.cc"+title.find("a").get("href"))
        if links:
            for link in links:
                resp = requests.get(link, headers = headers)
                soup = BeautifulSoup(resp.text, "html.parser")
                article = soup.find(id="main-content").text
                article = article.split(re.findall(r"--[^-]+--\n※ 發信站|--\n※ 發信站",article,flags=re.DOTALL)[0])[0]
                article = re.sub(r"\n+","\n",article)+"：D"
                self.write(article)

    def stargogo_week(self):
        url = "https://www.stargogo.com/search/label/本週運勢?max-results=80"
        headers = {"user-agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36"
        }
        resp = requests.get(url, headers = headers)
        soup = BeautifulSoup(resp.text, "html.parser")
        titles = soup.find_all("h2","post-title entry-title")
        links = []
        for title in titles[0:15]:
            if re.search(f"{self.pattern1}|{self.pattern2}",title.text):
                links.append(title.find("a").get("href"))
        if links:
            for link in links:
                resp = requests.get(link, headers = headers)
                soup = BeautifulSoup(resp.text, "html.parser")
                article = soup.find("div","post-body entry-content").text.split("【本週運勢目錄一覽】")[0]
                article = re.sub(r"\n+", "\n", article)+"：D"
                self.write(article)
                time.sleep(2)

#主程式只要call這個function
def call_week():
    call = scrapying_week()
    call.delete_file()
    call.threads_blaire_week()
    call.threads_singingbb_week()
    call.threads_v_week()
    call.threads_yusitaluo_week()
    call.vogue_week()
    call.driver.close()
    call.ptt_week()
    call.stargogo_week()
    print("week完成爬蟲")

if __name__ == "__main__":
    call_week()
