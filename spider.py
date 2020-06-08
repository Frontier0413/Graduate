import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
from selenium import webdriver
import movie
# from threading import Thread, Lock

url_base = 'https://movie.douban.com/top250?start='
options = webdriver.ChromeOptions()
options.add_argument('-headless')
driver = webdriver.Chrome(options = options)

# max_thread_num = 8
# running = 1

# thread_lock = Lock()
# file_lock = Lock()
# driver_lock = Lock()

# 获取初始数据集
def get_movie_url():
    headers = { 'User-Agent' : str(UserAgent().random)}
    i = 0
    # global running
    while (i < 226):
        url_to_get = url_base + str(i) + '&filter='
        response = requests.get(url = url_to_get, headers=headers, timeout = 10)
        soup = BeautifulSoup(response.text, 'lxml')
        urls = soup.select('div.info > div.hd > a')
        for elems in urls:
            # if running < max_thread_num:
                # thread_lock.acquire()
                # if running < max_thread_num:
                    # new_thread = Thread(target = get_movie_elems_thread, args = elems['href'])
                    # running += 1
                    # new_thread.start()
                # thread_lock.release()
            get_movie_elems_thread(elems['href'])
        i += 25


# 获取对应链接的数据并输出到缓存
def get_movie_elems_thread(movie_url):
    # global running
    get_movie_elems(movie_url)

    # thread_lock.acquire()
    # running -= 1
    # thread_lock.release()

def get_movie_elems(url):
    # global running
    # driver_lock.acquire()
    # print(url)
    driver.get(url)
    # driver_lock.release()
    soup = BeautifulSoup(driver.page_source, 'lxml')
    movie_name = soup.select_one('span[property="v:itemreviewed"]')
    movie_year = soup.select_one('span[class="year"]')
    movie_infomation = soup.select_one('div[id="info"]')
    movie_score = soup.select_one('strong[property="v:average"]')

    if movie_name == '' or movie_year == '' or movie_infomation == '' or movie_score == '':
        # 此时需手动解决验证问题 解决完成之后终端输入任意字符程序 + 回车继续执行
        input()
        soup = BeautifulSoup(driver.page_source, 'lxml')
        movie_name = soup.select_one('span[property="v:itemreviewed"]')
        movie_year = soup.select_one('span[class="year"]')
        movie_infomation = soup.select_one('div[id="info"]')
        movie_score = soup.select_one('strong[property="v:average"]')
    if movie_name and movie_year and movie_infomation and movie_score:
        # file_lock.acquire()
        with open('movie.txt', 'a+', encoding = 'utf-8') as f:
            f.write(movie_name.text + '\n')
            f.write(movie_year.text)
            f.write(movie_infomation.text)
            f.write(movie_score.text)
            f.write('\n\n')
            f.close()
        # file_lock.release()
    # 如果手动解决验证出现问题，重新打开该页面并重复以上逻辑
    # 避免由于网络原因造成的程序crash，
    else:
        get_movie_elems(url)
        # 迭代调用自身必须在此处返回，否则会出现running自减两次的情况
        # return
    # driver.close()