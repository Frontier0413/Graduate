from bs4 import BeautifulSoup
import requests
import random

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

def getHTMLText(url,proxies):
    try:
        r = requests.get(url,proxies=proxies)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
    except:
        return 0
    else:
        return r.text

def get_ip_list(url):
    web_data = requests.get(url,headers)
    soup = BeautifulSoup(web_data.text, 'html')
    ips = soup.find_all('tr')
    ip_list = []
    for i in range(1, len(ips)):
        ip_info = ips[i]
        tds = ip_info.find_all('td')
        ip_list.append(tds[1].text + ':' + tds[2].text)
    # 检测ip可用性，移除不可用ip
    # 问题很大，因为在你爬取代理ip的同时，各大数据平台也会去爬取这个代理ip，
    # 不同的是，你是拿来用的，数据平台是拿来拉黑的， 因此ip池往往很快就不可用
    for ip in ip_list:
        try:
          proxy_host = "https://" + ip
          proxy_temp = {"https": proxy_host}
          res = urllib.urlopen(url, proxies=proxy_temp).read()
        except Exception as e:
          ip_list.remove(ip)
          continue
    return ip_list

def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    proxy_ip = random.choice(proxy_list)
    return proxie_ip


def random_ip():
    url = 'http://www.xicidaili.com/nn/'
    ip_list = get_ip_list(url)
    proxie = get_random_ip(ip_list)
    return proxie

