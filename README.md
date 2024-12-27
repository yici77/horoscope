# **星座運勢爬蟲**

此程式是星座運勢分析專案底下的爬蟲module，目的是定時蒐集星座運勢文章，以便將星座運勢進行後續的統計分析

* 每月運勢：star_month.py
* 每周運勢：star_week.py
* 每日運勢：star_day.py



### 每個程式的架構及功能如下

* import套件(requests+bs4用於靜態網頁，selenium用於動態網頁)
```python
import os
import requests
from bs4 import BeautifulSoup
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from datetime import date
import time
import re
```

* 以class創建driver物件提供後續的function操作
```python
class scrapying_month:
    def __init__(self):
        self.driver = uc.Chrome()
```

* 使用datetime以及re確定文章是當月、當週或當日運勢(以每日為例)
```python
    month = datetime.today().month
    day = datetime.today().day
    self.pattern = rf"(?<!-){month}[\u4e00-\u9fa5/.]{{1}}0?{day}(?!\d)(?!-)"
```

* define刪除檔案的函式(每次run程式時自動刪除前次爬蟲的資料)
```python
def delete_file(self):
    if os.path.exists(self.filename): 
        os.remove(self.filename) 
```

* define寫檔的函式以及統一用詞
```python
def write(self,article):
    article = article.replace("白羊","牡羊").replace("魔羯","摩羯").replace("天平","天秤")
    with open(self.filename, "a", encoding = "UTF-8") as outputfile:
        return outputfile.write(article)
```

* 每個function抓不同網站的資料並清洗出需要的資訊(以threads範例)
```python
def threads_day(self):
    userid_list = ["riman.xs.zaia","macaumdd","astro_crystal2020"]
    driver = self.driver
    for userid in userid_list:
        driver.get(f"https://www.threads.net/@{userid}")
        driver.execute_script("window.scrollTo(0, 300);")
        time.sleep(5)

        # 定位頁面中包含所有文章的標籤
        articles_list = driver.find_element(By.CSS_SELECTOR,"div.x1c1b4dv.x13dflua.x11xpdln").find_elements(By.CSS_SELECTOR, "div.x9f619.x1n2onr6.x1ja2u2z")
        # 找出包含"星座"以及日期相符的文章，並定位此文章的包含url的標籤
        article_url = [i.find_element(By.CSS_SELECTOR,f'a[href*="/@{userid}/post/"]')
                       for i in articles_list if (re.search(self.pattern,i.text) and "星座" in i.text)]
        # 進入文章頁面
        if article_url:
            driver.get(f"{article_url[0].get_attribute("href")}")
            time.sleep(3)

            # 定位包含文章的標籤並爬取文字
            article_list = driver.find_elements(By.CLASS_NAME,"x1a6qonq")[0:3]
            article = [i.text for i in article_list]
            # 清洗不需要的內容
            if "留言" in article[0]:
                article = "\n".join(article)+"：D"
            else:
                article = article[0]+"：D"
            # 寫檔
            self.write(article)
```
*p.s. "：D"此符號的目的是後續讀取檔案時用以切割文章*

* 一次叫出所有函式提供此專案的主程式call function
```python
def call_day():
    def call_day():
    call = scrapying_day()
    call.delete_file()
    call.threads_day()
    call.linetoday_culture_day()
    call.linetoday_meng_day()
    call.linetoday_sofia_day()
    call.niunews_day()       
    call.driver.close()
    call.techpurple_day()
    call.stargogo_day()        
    print("day完成爬蟲")

if __name__ == "__main__":
    call_month()
```

* 所有爬蟲得到的文章會寫進txt檔，以便後續進行分析
