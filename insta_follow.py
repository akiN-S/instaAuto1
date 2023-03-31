from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datetime
import time

import sys
import bs4
import random
import json
import subprocess

import insta_common

# 過去にフォローをしたか確認
def is_not_followed():
    html = driver.page_source.encode('utf-8')
    soup = bs4.BeautifulSoup(html, "lxml")
    ret = soup.select('div._aacl._aaco._aacw._aad6._aade')
    if ret: # 配列に何か('フォローする')が格納されていたら、未フォロー
        return True
    else: # 配列に何も入っていなければ、フォロー済
        return False

def following(driver, num):

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

    # フォロー処理
    try:
        if is_not_followed() == True:
            driver.find_elements(By.CLASS_NAME, '_aacw')[0].click() # 該当の投稿者の'フォローする'をクリック
            print(insta_common.now_time() + str(num) + 'ループ目の処理：投稿者をフォロー')
        else:
            print(insta_common.now_time() + str(num) + 'ループ目の処理：フォロー済みです')

    except WebDriverException as e:
        print(insta_common.now_time() + str(num) + 'ループ目の処理：フォロー処理でエラーが発生しました')
        print(e)
        time.sleep(random.randint(3, 5))
        return
        
    time.sleep(random.randint(3, 5))


if __name__ == '__main__':

    # 設定情報読み込み
    instaSetting = insta_common.load_settings()

    if instaSetting.username == "" or instaSetting.password == "" \
    or instaSetting.followingTargetTag == "" or instaSetting.maxFollowing == "":
        print('必要な設定情報の読み込みに失敗しました')
        sys.exit()


    print(insta_common.now_time() + 'フォロー特定キーワード: ' + instaSetting.followingTargetTag)
    print(insta_common.now_time() + 'フォロー試行対象投稿者数: ' + instaSetting.maxFollowing)

    # ログイン処理
    driver = insta_common.insta_login(instaSetting.username, instaSetting.password)

    # 検索処理
    insta_common.search_tags(driver, instaSetting.followingTargetTag)


    # 直近の投稿者をフォロー
    following(driver, 1) # 1人目の投稿者をフォロー

    # 2目以降の投稿者をフォローしていく
    for i in range(int(instaSetting.maxFollowing)-1):
        following(driver, i+2)

    print(insta_common.now_time() + 'フォロー終了')
    driver.close()
    driver.quit()

    subprocess.call('PAUSE', shell=True)