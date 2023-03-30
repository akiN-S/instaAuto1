from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datetime
import time

import bs4
import random
import json
import subprocess

import insta_common

# 過去にいいねをしたか確認
def is_not_liked():
    html = driver.page_source.encode('utf-8')
    soup = bs4.BeautifulSoup(html, "lxml")
    ret = soup.select('span._aamw')
    if  not '取り消す' in str(ret[0]): # '取り消す'が格納されていなければ、未いいね
        return True
    else: # '取り消す'が格納されていれば、いいね済
        return False


def liking(driver, num):

    # 投稿の表示
    try: 
        if num == 1:
            driver.find_elements(By.CLASS_NAME, '_aagw')[9].click() # 検索結果の最新の投稿をクリック
            print(insta_common.now_time() + str(num) + 'ループ目の処理：最新の投稿をクリックしました')

        else: 
            driver.find_element(By.CLASS_NAME, '_aaqg').click() # 該当の投稿へ移動
            print(insta_common.now_time() + str(num) + 'ループ目の処理：次の投稿へ移動しました')

        time.sleep(random.randint(3, 5))
        
    except WebDriverException as e:
        print(insta_common.now_time() + str(num) + 'ループ目の処理：投稿の表示でエラーが発生しました')
        print(e)
        time.sleep(random.randint(3, 5))
        return

    # いいね処理
    try:
        if is_not_liked() == True:
            driver.find_elements(By.CLASS_NAME, '_aamw')[0].click() # 該当の投稿の'いいね'をクリック
            print(insta_common.now_time() + str(num) + 'ループ目の処理：投稿をいいね')
        else:
            print(insta_common.now_time() + str(num) + 'ループ目の処理：いいね済みです')

    except WebDriverException as e:
        print(insta_common.now_time() + str(num) + 'ループ目の処理：いいね処理でエラーが発生しました')
        print(e)
        time.sleep(random.randint(3, 5))
        return
        
    time.sleep(random.randint(3, 5))

if __name__ == '__main__':
    # 設定情報
    settingFilePath = 'insta_settings.json'
    with open(settingFilePath, 'r', encoding='utf-8') as f:
        settings = json.load(f)

    # ログイン情報
    username = settings['username']
    password = settings['password']

    # 検索対象
    tagName = settings['likingTargetTag']
    print(insta_common.now_time() + '特定キーワード: ' + tagName)

    # いいねの設定
    maxLiking = settings['maxLiking']


    # ログイン処理
    driver = insta_common.insta_login(username, password)

    # 検索処理
    insta_common.search_tags(driver, tagName)

    # 直近の投稿をいいね
    liking(driver, 1) # 1つ目の投稿をフォロー
    

    # 2つ目以降の投稿をいいねしていく
    for i in range(maxLiking-1):
        liking(driver, i+2)

    print(insta_common.now_time() + 'いいね終了')
    driver.close()
    driver.quit()

    subprocess.call('PAUSE', shell=True)