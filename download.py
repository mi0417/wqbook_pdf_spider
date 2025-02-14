import time
import random

from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import pyautogui

import logging

logging.basicConfig(format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
                    datefmt='## %Y-%m-%d %H:%M:%S')

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger()

USER = '156xxxxxxxx'
PASSWORD = 'xxxxxx'
PAGES = 300 #书的总页数
ADDRESS = 'https://wqbook.wqxuetang.com/read/pdf?bid=xxxxxxx' #书的网址
startPage = 1 #从第几页开始下载

# driver = webdriver.Chrome('.\\chromedriver.exe') #括号内写你的chromedriver.exe所在的位置
service = webdriver.ChromeService(".\chromedriver.exe")
 
# 配置选项
options = webdriver.ChromeOptions()
# 忽略证书错误
options.add_argument('--ignore-certificate-errors')
# 忽略 Bluetooth: bluetooth_adapter_winrt.cc:1075 Getting Default Adapter failed. 错误
options.add_experimental_option('excludeSwitches', ['enable-automation'])
# 忽略 DevTools listening on ws://127.0.0.1... 提示
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver=webdriver.Chrome(service=service, options=options)

def wechat_signin(driver, wait_time=60):
    '''
    wait_time: 等待用户扫描二维码的时间。

    '''
    signin = driver.find_element(by=By.XPATH, value='//*[@id="app"]/header/div[2]/span[2]')
    signin.click()
    time.sleep(1)

    wechat = driver.find_element(by=By.XPATH, value='/html/body/app-root/app-login/div/div/div[2]/div[3]/div[2]/img[1]')
    wechat.click()
    time.sleep(wait_time)

def signin(driver):
    '''
    登录。
    '''
    signin = driver.find_element(by=By.XPATH, value='//*[@id="app"]/header/div[2]/span[2]')
    signin.click()
    time.sleep(3)

    # 找到输入框，这里需要自行在F12的Elements中找输入框的位置，然后在这里写入
    user_input = driver.find_element(by=By.XPATH, value='//input[@type="text"]')
    pw_input = driver.find_element(by=By.XPATH, value='//input[@type="password"]')
    login_btn = driver.find_element(by=By.CLASS_NAME, value='ant-btn')
 
    # 输入用户名和密码，点击登录
    user_input.send_keys(USER)
    pw_input.send_keys(PASSWORD)
    time.sleep(1)
    login_btn.click()
    logger.info('等待操作滑块40秒')
    time.sleep(40)
    logger.info('等待结束')

def go_to_page_n(driver, n):
    '''
    使用鼠标滚轮跳转到对应页数。
    '''
    logger.info(f'正在跳转至第{n}页')
    ActionChains(driver)\
        .scroll_to_element(pages[n])\
        .perform()

def right_click_save_as(segment):
    '''
    segment: 我们想另存为所对应的<img>
    '''
    # logger.info('正在保存第', segment.get_attribute('data-index'), '张图片')
    ActionChains(driver)\
        .context_click(segment)\
        .perform()

    time.sleep(1)
    pyautogui.typewrite(['down', 'down', 'enter'], interval=1) #键盘输入下，下，回车，回车
    time.sleep(3)
    pyautogui.typewrite(['enter'], interval=0.5) #键盘输入下，下，回车，回车
    time.sleep(3)
    # time.sleep(5)

# 浏览器关闭下载完成后显示下载内容，会遮挡界面导致漏下载，浏览器窗口最大化有可能避开遮挡
driver.maximize_window() #将浏览器窗口最大化
driver.get(ADDRESS)
time.sleep(1)

# wechat_signin(driver)
signin(driver)

logger.info('解除鼠标右键限制')
js = 'javascript:(function() { function R(a){ona = "on"+a; if(window.addEventListener) window.addEventListener(a, function (e) { for(var n=e.originalTarget; n; n=n.parentNode) n[ona]=null; }, true); window[ona]=null; document[ona]=null; if(document.body) document.body[ona]=null; } R("contextmenu"); R("click"); R("mousedown"); R("mouseup"); R("selectstart");})() '
driver.execute_script(js)

# 获取书名
# 书名登录或未登录状态class不同 read-header-title
title = driver.find_element(by=By.CLASS_NAME, value='read-header-title').text
logger.info(title)

# 获取高清图片
pages = driver.find_elements(by=By.CLASS_NAME, value='page-img-box')
logger.info(f'page-img-box数量：{len(pages)}')

for page in range(startPage, PAGES + 1):
    go_to_page_n(driver, page)
    time.sleep(random.randint(5,20)) # 翻页后，给高清图片加载预留时间

    # 将每一个细分图片找到，统一存在pieces这个list里
    img = pages[page].find_element(by=By.CLASS_NAME, value='page-lmg')
    pieces = img.find_elements(by=By.TAG_NAME, value='img')

    # 根据“left"的css值来排序
    order = []
    row = []
    for piece in pieces:
        row.append(float(piece.value_of_css_property('left')[:-2]))

    while len(order) != len(row):
        for n in range(len(row)):
            if n not in order:
                mini = row[n]

        i = 0
        while i < len(row):
            if row[i] < mini and i not in order:
                mini = row[i]
            i += 1
        # 找到最小
        order.append(row.index(mini))
    
    for e in order:
        # time.sleep(2)
        right_click_save_as(pieces[e])

logger.info(f'等待10s后关闭浏览器')
time.sleep(10)
driver.quit()
