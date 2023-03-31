from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datetime
import time
import csv

LOAD_FILE = "CSV" # 設定ファイルの種別を指定

class InstaSetting:
    username = None
    password = None
    maxLiking = None
    likingTargetTag = None
    maxFollowing = None
    followingTargetTag = None
    maxUnfollowing = None
    postPic = None
    postText = None
   

# 画面に文字を出力する際に時刻を表示する
def now_time():
   dt_now = datetime.datetime.now()
   return dt_now.strftime('%m/%d %H:%M')+' '

# 設定情報を読み込み、変数に格納する
def load_settings():
   
   # 設定情報を格納するクラス
   instaSetting = InstaSetting()

   # JSONファイルを読み込む場合
   if LOAD_FILE == "JSON":
      # 設定情報を読み込み
      settingFilePath = 'insta_settings.json'

      with open(settingFilePath, 'r', encoding='utf-8') as f:
         settings = json.load(f)
      
      # 設定情報を変数に展開
      instaSetting.username = settings['username']
      instaSetting.password = settings['password']
      instaSetting.maxLiking = settings['maxLiking']
      instaSetting.likingTargetTag = settings['likingTargetTag']
      instaSetting.maxFollowing = settings['maxFollowing']
      instaSetting.followingTargetTag = settings['followingTargetTag']
      instaSetting.maxUnfollowing = settings['maxUnfollowing']
      instaSetting.postPic = settings['postPic']
      instaSetting.postText = settings['postText']

   # CSVファイルを読み込む場合
   elif LOAD_FILE == "CSV":
      settingFilePath = 'insta_settings.csv'

      with open(settingFilePath, 'r', encoding='shift_jis') as f:
         reader = csv.reader(f)
         countLine = 0
         try:
            for line in reader:
               countLine = countLine + 1
               key = line[0] # 0列目がkey
               data = line[1] # 1列目がdata
               
               # 0列目のkeyのデータがクラスのメンバと一致したものを格納
               if key == "username":
                  instaSetting.username = data
               elif key == "password":
                  instaSetting.password = data
               elif key == "maxLiking":
                  instaSetting.maxLiking = data
               elif key == "likingTargetTag":
                  instaSetting.likingTargetTag = data
               elif key == "maxFollowing":
                  instaSetting.maxFollowing = data
               elif key == "followingTargetTag":
                  instaSetting.followingTargetTag = data
               elif key == "maxUnfollowing":
                  instaSetting.maxUnfollowing = data
               elif key == "postPic":
                  instaSetting.postPic = data
               elif key == "postText":
                  instaSetting.postText = data

         except IndexError as e:
            print("警告: " + str(countLine) + "行目のCSVデータの読み出しに失敗しました")

   # 設定情報を格納したクラス変数を返却
   return instaSetting


# ログイン処理を行う
def insta_login(username, password):
    # driver = webdriver.Chrome (ChromeDriverManager().install())
    driver = webdriver.Chrome('./chromedriver')

    driver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
    print(now_time()+'instagramにアクセスしました')
    time.sleep(1)

    driver.find_element(By.NAME, 'username').send_keys(username)
    time.sleep(1)
    driver.find_element(By.NAME, 'password').send_keys(password)
    time.sleep(1)

    driver.find_element(By.XPATH, '//*[@id="loginForm"]/div/div[3]').click()
    time.sleep(3)
    # ログイン情報の保存「後で」をクリック
    driver.find_element(By.CLASS_NAME, 'x1i10hfl').click()
    time.sleep(3)

    # お知らせをオンにする「後で」をクリック
    driver.find_element(By.CLASS_NAME, '_a9_1').click()
    print(now_time()+'instagramにログインしました')
    time.sleep(3)

    return driver

def search_tags(driver, tagName):
    #タグを検索
    instaurl = 'https://www.instagram.com/explore/tags/'
    driver.get(instaurl + tagName)
    time.sleep(3)
    print(now_time()+"tagで検索を行いました")
    time.sleep(5)

    #直近で投稿ページに移動
    target = driver.find_elements(By.CLASS_NAME, '_aagw')[10]
    actions = ActionChains(driver)
    actions.move_to_element(target)
    actions.perform()
    print(now_time()+'最新の投稿まで画面を移動しました')
    time.sleep(3)
