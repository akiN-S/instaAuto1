from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By

import sys
import random
import json
import pyautogui
import time
import subprocess

import insta_common

class FollowingItem:
    element = None
    username = None
    status = None

class followingCollector:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.dic_id_following = {}
        self.window_width = 0
        self.window_height = 0
        self.driver = None

    def get_num_following(self):
        # 画面に表示されているフォロー数を取得
        following_number = self.driver.find_elements(By.CLASS_NAME, '_ac2a')[2].text
        print(insta_common.now_time() + 'following_number: ' + following_number)
        
        return following_number

    def scroll(self):
        # 画面をスクロール
        pyautogui.scroll(-5*self.window_height)

    def do_infinite_scroll(self):
        # 画面を一番下までスクロールする

        num_following = self.get_num_following() # スクロールの制御のために、フォロー数を取得

        # フォロー数が、0または多すぎないことを確認
        if int(num_following) == 0 or int(num_following) > 500000:
            print(insta_common.now_time() + 'フォローが 0 または 500000以上は非対応です')
            return 0

        # 現在表示されているフォロー一覧を取得
        followings_list01 = self.get_following_list()

        while True:
            # スクロールの準備
            self.window_width, self.window_height = pyautogui.size()
            pyautogui.moveTo(self.window_width/2, self.window_height/2, duration=0)

            # スクロールを実行
            for i in range(5):
                self.scroll()
                time.sleep(1)

            # 現在表示されているフォロー一覧を取得し、取得状況を表示
            followings_list02 = self.get_following_list()
            print(insta_common.now_time() + '-----Now getting followings({}/{})-----'.format(len(followings_list01), num_following))

            # フォロー一覧の取得が完了していれば、ループを終了
            if len(followings_list01) != len(followings_list02):
                followings_list01 = followings_list02
            else:
                break

    def get_following_list(self):

        followsElements = self.driver.find_elements(By.CLASS_NAME, 'xiojian') # フォロー一覧の要素を取得
        followingItems = [] # フォロー一覧の要素を格納する配列

        for followsElement in followsElements:
            if not 'フォローする' in followsElement.text: # 'フォローする'と表示されているユーザはおすすめであり、フォロー中ではない
                followingItem = FollowingItem() # フォロー情報を格納するClassを呼び出し
                followingItem.element = followsElement # 要素を格納
                followingItem.username = followsElement.text.split('\n')[0] # ユーザ名を格納
                followingItem.status = 'フォロー中' # ステータスを'フォロー中'を格納

                followingItems.append(followingItem) # フォロー情報を配列に格納

        return followingItems


    def display_followings(self, target_username):
        url = "https://www.instagram.com/{}/following".format(target_username) # フォロー一覧を表示するURL
        # url = "I:\\マイドライブ\\20_work\\20230323_coconala\\20230323-01_instagram\\納品物\\test.html"
        self.driver.get(url) # 該当のURLへアクセス
        time.sleep(random.randint(3, 5))
        return 

    def get_followings(self):
        print(insta_common.now_time() + 'フォロー一覧の取得を開始')

        self.do_infinite_scroll() # 画面を一番下までスクロール
        self.followings_list = self.get_following_list() # 表示されているフォロー一覧を取得
        print(insta_common.now_time() + 'フォロー一覧の取得を完了')

        return self.followings_list

    def main(self, username, maxUnfollowing):
        # ログイン処理
        self.driver = insta_common.insta_login(self.username, self.password)
        # self.driver = webdriver.Chrome('./chromedriver')
        time.sleep(1)
        self.driver.maximize_window() # 画面を最大化、スクロール機能の正しく動作させるために必要
        
        try:
            self.display_followings(target_username=username) # フォロー一覧を表示
            followings_list = self.get_followings() # フォロー一覧のユーザ名と要素を取得
        except:
            import traceback
            traceback.print_exc()

        # フォロー数が削除対数より少ない場合、削除対象数をフォロー数と同じにする
        if maxUnfollowing > len(followings_list):
            maxUnfollowing = len(followings_list)

        print(insta_common.now_time() + 'フォロー一覧の下から' + str(maxUnfollowing) + '番目までをアンフォローします')
        unfollowingList = followings_list[-maxUnfollowing:] # フォロー全リストを下から削除数分取得

        # アンフォロー対象を順番に処理
        for unfollowTarget in unfollowingList:
            print(insta_common.now_time() + unfollowTarget.username + 'をアンフォローします')

            try:
                element = unfollowTarget.element.find_element(By.CLASS_NAME, '_aad6') # アンフォローのボタンの要素
                ActionChains(self.driver).move_to_element(element).perform() # 該当の要素をクリックするために、その要素を表示するように移動
                time.sleep(1)
                element.click() # アンフォローのボタンをクリック
                time.sleep(1)
                self.driver.find_element(By.CLASS_NAME, '_a9-_').click() # 'フォローをやめる'をクリック
                time.sleep(random.randint(3, 5))

            except WebDriverException as e:
                print(insta_common.now_time() + unfollowTarget.username + 'のアンフォローでエラーが発生しました')
                print(e)
                time.sleep(random.randint(3, 5))
                return

        self.driver.quit()
        return self.dic_id_following


if __name__ == '__main__':
    # 設定情報
    settingFilePath = 'insta_settings.json'
    with open(settingFilePath, 'r', encoding='utf-8') as f:
        settings = json.load(f)

    # ログイン情報
    username = settings['username']
    password = settings['password']

    # アンフォロー数の設定
    maxUnfollowing = settings['maxUnfollowing']
    
    if maxUnfollowing == 0:
        print(insta_common.now_time() + 'アンフォロー対象が 0人 のためツールを終了します')
        sys.exit( )

    fc = followingCollector(username, password)
    fc.main(username, maxUnfollowing)

    subprocess.call('PAUSE', shell=True)
