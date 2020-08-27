from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import datetime
import random
import sys
import logging


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class InstagramBot:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def closeBrowser(self):
        self.driver.close()

    def login(self):
        driver = self.driver
        driver.get("https://www.instagram.com/")
        time.sleep(2)
        login_button = driver.find_element_by_xpath("//a[@href='/accounts/login/?source=auth_switcher']")
        login_button.click()
        time.sleep(2)

        user_name_elem = driver.find_element_by_xpath("//input[@name='username']")
        user_name_elem.clear()
        user_name_elem.send_keys(self.username)
        passworword_elem = driver.find_element_by_xpath("//input[@name='password']")
        passworword_elem.clear()
        passworword_elem.send_keys(self.password)
        passworword_elem.send_keys(Keys.RETURN)
        time.sleep(40)


    def like_photo(self, hashtag):
        driver = self.driver
        driver.get("https://www.instagram.com/explore/tags/" + hashtag + "/")
        time.sleep(2)

        # gathering photos
        pic_hrefs = []
        for i in range(1, 7):
            try:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                # get tags
                hrefs_in_view = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                # print("Check: pic href length " + str(len(pic_hrefs)))
            except Exception:
                continue

        # Liking photos
        unique_photos = len(pic_hrefs)
        for pic_href in pic_hrefs:
            driver.get(pic_href)
            time.sleep(2)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            try:
                time.sleep(random.randint(6, 10))
                like_button = lambda: driver.find_element_by_xpath('//span[@aria-label="Like"]').click()
                like_button().click()
                for second in reversed(range(0, random.randint(18, 28))):
                    print_same_line("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    print("#" + hashtag + ': unique photos left: ' + str(unique_photos)
                                    + " | Sleeping " + str(second))
                    time.sleep(1)
            except Exception as e:
                time.sleep(2)
            unique_photos -= 1

if __name__ == "__main__":

    username = "xxxxx"
    password = "yyyyy"

    ig = InstagramBot(username, password)
    ig.login()
    hashtags = [
                # cat
                '貓','可愛','小貓','猫','黒猫同盟','黑貓','サバトラ','猫の日',
                '猫好きな人と繋がりたい','ねこ部','ねこぐらむ','ねこ写真',
                '終生飼養','領養代替購買不棄養',
                'catsofinstagram','cats_of_instagram','catsoftheworld','weeklyfluff',
                'yourcatphoto','catlover','catfeatures','gato','blackcats','moodygrams'
                'neko','cutepetclub','meow','purr','catslife',
                # Taiwan
                '金門','台湾','台灣','台湾留学','台湾旅行','今日もx日和',
                '台湾大好き','台湾好きな人と繋がりたい','我愛台灣','台湾一人旅',
                'yo_taiwan'
                # travel
                '旅大好き',
                # other
                '写真好きな人と繋がりたい','親子',
                # girl
                '清新','人像','人像攝影','少女','女の子','日系','美少女','被写体',
                '小清新','ポートレート','good_portraits_world','ポートレート撮影',
                'ポトレ撮影隊',
                # camera, trip
                'カメラ練習','カメラある生活','カメラのある生活','photravelers',
                
                '蘆洲','關渡','淡水','淡水河','基隆河','降落','着陸','內湖','中央大學'
                ]

    while True:
        try:
            # Choose a random tag from the list of tags
            tag = random.choice(hashtags)
            ig.like_photo(tag)
        except Exception:
            ig.closeBrowser()
            time.sleep(60)
            ig = InstagramBot(username, password)
            ig.login()