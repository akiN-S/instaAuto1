from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import datetime
import time

def now_time():
   dt_now = datetime.datetime.now()
   return dt_now.strftime('%m/%d %H:%M')+' '

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
