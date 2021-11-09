
from fake_useragent import UserAgent
import aiohttp
import asyncio

import urllib.request
import urllib.error
import re
import os
import datetime
import easygui
import time
from selenium import webdriver
import sys
import shutil

ua = UserAgent()
header = ua.random
headers = {'User-Agent': header}
# 获取网页中所有图片对应的pin
def get_pins(url_):
    agent = "User-Agent={}".format(header)
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument(agent)
    driver = webdriver.Chrome(chrome_options=options)
    driver.get(url_)

    js1 = "window.scrollTo(0,document.body.scrollHeight);"
    js2 = "h=document.documentElement.scrollTop; return h"
    pattern = re.compile(r'data-id=?"(\d*)"')
    origin_top = driver.execute_script(js2)
    pins_ = set()
    # 可以使用大括号 { } 或者 set() 函数创建集合，但是注意如果创建一个空集合必须用 set() 而不是 { }，因为{}是用来表示空字典类型的。
    while True:
        html_ = driver.page_source
        pins_1 = re.findall(pattern, html_)
        pins_2 = set(pins_1)
        pins_.update(pins_2)
        driver.execute_script(js1)
        new_top = driver.execute_script(js2)
        time.sleep(1)
        if new_top == origin_top:
            break
        else:
            origin_top = new_top
    driver.close()
    return pins_

# 获取页面html
def get_html_1(url_):
    try:
        page = urllib.request.urlopen(url_)
    except urllib.error.URLError:
        return 'fail'
    html_ = page.read().decode('utf-8')
    return html_

async def fetch(url):
    # with语句保证在处理session的时候，总是能正确的关闭它
     async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers, verify_ssl=False) as resp:
        # 1.如果想要得到结果，则必须使用await关键字等待请求结束，如果没有await关键字，得到的是一个生成器
        # 2.text()返回的是字符串的文本，read()返回的是二进制的文本
            data = await resp.text()
            # print('data', data)
            return data

# 下载图片
def get_image(path_, pin_list):
    loop = asyncio.get_event_loop()
    tasks = []
    x = 1
    for pinId in pin_list:
        # 获取跳转网页网址
        url_str = r'http://huaban.com/pins/%s/' % pinId
        
    #     task = asyncio.ensure_future(fetch(url_str))
    #     tasks.append(task)
    # results = loop.run_until_complete(asyncio.wait(tasks))

    # for item in results[0]:
        # 获取点击图片时弹出网页的源码
        pinId_source = get_html_1(url_str)
        # pinId_source = item.result()
        # print("---pinId_source:", pinId_source)
        # print("---pinId_source type:", type(pinId_source))
        if pinId_source == 'fail':
            continue

        # 解析源码，获取原图片的网址
        '''
        <div class="main-image"><div class="image-holder" id="baidu_image_holder">
        <img src="//hbimg.huabanimg.com/64369267b9c8dc7a43da81457658c05b1a752f9329ec0-dSfdfl_fw658/format/webp"
        '''
        img_url_re = re.compile('main-image.*?src="(.*?)"', re.S)
        img_url_list = re.findall(img_url_re, pinId_source)
        img_url = 'http:' + img_url_list[0]

        try:
            urllib.request.urlretrieve(img_url, path_ + '\%s.jpg' % x)  # urlretrieve()方法直接将远程数据下载到本地
        except urllib.error.URLError:
            print("获取失败！%s" % img_url)
            continue
        print("获取成功！%s" % img_url)
        x += 1
    print("保存图片成功！")


# 创建文件夹路径
def createPath(boaed_id):
    path_ = easygui.diropenbox(title='选择你要保存的路径')
    while True:
        filePath = path_ + "\\" + boaed_id
        isExists = os.path.exists(filePath)
        if not isExists:
            # 创建目录
            os.makedirs(filePath)
            # print('%s创建成功！' % filePath)
            break
        else:
            # print('%s已存在重新输入！' % filePath)
            state = easygui.ccbox(msg='是否重新下载', title=' ', choices=('继续', '取消'), image=None)
            if state:
                shutil.rmtree(filePath)
            else:
                sys.exit(0)

    return filePath

def main():
    url = easygui.enterbox('请输入面板地址：', title='获取花瓣用户任意面板中的图片')
    board_id = re.findall("\d+", url)[0]
    if not board_id:
        easygui.msgbox(msg='地址输入错误', title=' ', ok_button='OK', image=None, root=None)
        sys.exit(0)
    path = createPath(board_id)
    pins = get_pins(url)
    # print(pins)
    get_image(path, pins)
    easygui.msgbox(msg='下载完成', title=' ', ok_button='OK', image=None, root=None)

def test(path_='D:\Glory\HuaBan\\34130626', pin_list=["1143629013"]):
    loop = asyncio.get_event_loop()
    tasks = []
    x = 1
    for pinId in pin_list:
        # 获取跳转网页网址
        url_str = r'https://huaban.com/pins/%s/' % pinId
        task = asyncio.ensure_future(fetch(url_str))
        tasks.append(task)
    results = loop.run_until_complete(asyncio.wait(tasks))

    # print("---results:", results)
    for item in results[0]:
        # 获取点击图片时弹出网页的源码
        # pinId_source = get_html_1(url_str)
        pinId_source = item.result()
        print("---pinId_source:", pinId_source)
        if pinId_source == 'fail':
            continue
        img_url_re = re.compile('main-image.*?src="(.*?)"', re.S)
        img_url_list = re.findall(img_url_re, pinId_source)
        print('--img_url_list:', img_url_list)
        img_url = 'http:' + img_url_list[0]
        try:
            urllib.request.urlretrieve(img_url, path_ + '\%s.jpg' % x)  # urlretrieve()方法直接将远程数据下载到本地
        except urllib.error.URLError:
            print("获取失败！%s" % img_url)
            continue
        print("获取成功！%s" % img_url)
        x += 1

if __name__ == '__main__':
    main()
    # test()