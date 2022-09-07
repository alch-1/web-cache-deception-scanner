#-*- coding:utf-8 -*-
from time import sleep
from optparse import Option
from random import uniform
import bs4
import argparse
import requests
from utils import createFolder,writeFile
from json2html import json2html
from urllib.parse import urlparse
# from pwn import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

id='pentesting1234'
pw='hackenterbobs12#@'

# Must set driver for your path
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
# options.add_argument('headless')
options.add_argument('window-size=1920x1080')
# options.add_argument("disable-gpu")
s = Service('/mnt/c/Users/aldri/Desktop/chromedriver_linux64/chromedriver')
driver = webdriver.Chrome(service=s,options=options)


class Node:
    def __init__(self):
        self.pNode = None
        self.data = list()
        self.count = 0
    
    def previous_node(self):
        return self.pNode
    def insert(self, url, content_len, status_code):
        self.data.append({'url' : url, 'content_len' : content_len, 'status_code' : status_code, 'link' : None})
        self.count += 1
    def getData(self, index):
        return self.data[index]
    def getLength(self):
        return self.count
    def modifyData(self, index, key, value):
        self.data[index][key] = value


      
def command_parser():
    parser = argparse.ArgumentParser(description = "URL crawler")
    
    parser.add_argument("--url", required=True, help="Input url or --url [Parent url] [Sub url (option)], --url http://test.com/")
    parser.add_argument("--excloud", required=False, default=None, nargs='+', help="Input exclouded url, --excloud http://test.com/logout http://test.com/login")
    
    arg = parser.parse_args()
    

    return arg


    
def request(url, header):
    if 'logout' in url:
        return driver
    if len(header) == 0:
        driver.get(url)
    else:
        driver.get(url,headers=header)
    
    return driver

def url_parser(bs, arg, url_table):
    tag_list = {"a" : "href", "img" : "src", "iframe" : "src", "form" : "action", "script" : "src", "link" : "href"}
    result_list = list()
    
    for key in tag_list.keys():
        link_list = bs.find_all(key)        
        
        for l in link_list:
            link = l.get(tag_list[key])
            
            if link is None or len(link) == 1 or link == "" or link[0] == '#':
                # Useless data
                # ex) #, #content, /, None ...
                continue
            
            if link[0] == '/' or link[0] == '?':
                result_list.append(arg.url + link)
            else:
                result_list.append(link)
    
    # Delete duplicate url 
    result_list = set(result_list)
    result_list = list(result_list - set(url_table))
    url_table += result_list
    
    return insertData(result_list), url_table
    
# Insert in Node 
def insertData(data):
    node = Node()
    for d in data:
        node.insert(d, None, None)
    
     
    return node

# This fucntion must modified with user
def init_login(url):
    if url =="https://vk.com/":
        login_url='https://vk.com/login?u=2&to=L2ZlZWQ/'
        login_x_path='//*[@id="login_button"]/span/span'
        id='01086291952'
        pw='hackenterbobs12#@'
        driver.get(login_url)
        driver.find_element_by_name('email').send_keys(id)
        driver.find_element_by_name('pass').send_keys(pw)
        driver.find_element_by_xpath(login_x_path).send_keys(Keys.ENTER)
    elif url == 'https://www.evernote.com/':
        login_url='https://www.evernote.com/Login.action?referralSpecifier=mktgrepack_en_oo_web_nav_V00/'
        login_x_path='//*[@id="loginButton"]'
        id='smlijun@naver.com'
        pw='hackenterbobs12#@'
        driver.get(login_url)
        driver.find_element(By.NAME,'email').send_keys(id)
        driver.find_element(By.XPATH,login_x_path).send_keys(Keys.ENTER)
        sleep(uniform(3,4))
        driver.find_element(By.NAME,'password').send_keys(pw)
        sleep(uniform(3,4))
        driver.find_element(By.XPATH,login_x_path).send_keys(Keys.ENTER)
        return 'https://www.evernote.com/client/web?_sourcePage#?hm=true&'
    elif url == 'https://www.grammarly.com/':
        login_url = 'https://www.grammarly.com/signin'
        login_x_path='//*[@id="page"]/div/div/div[2]/div/form/button'
        id='smlijun@naver.com'
        pw='hackenterbobs12#@'
        driver.get(login_url)
        driver.find_element(By.NAME,'emali').send_keys(id)
        driver.find_element(By.NAME,'password').send_keys(pw)
        sleep(uniform(3,4))
        driver.find_element(By.XPATH,login_x_path).send_keys(Keys.ENTER)
    elif url =='https://www.tiktok.com/':
        login_url = 'https://www.tiktok.com/login/phone-or-email/email/'
        login_x_path='//*[@id="root"]/div/div[1]/form/button'
        id='smlijun@naver.com'
        pw='hackenterbobs12#@'
        driver.get(login_url)
        sleep(uniform(1,3))
        driver.find_element(By.NAME,'email').send_keys(id)
        driver.find_element(By.NAME,'password').send_keys(pw)
        driver.find_element(By.XPATH,login_x_path).send_keys(Keys.ENTER)

       
        

def nodeToList(node):
    result = dict()
    for index in range(node.getLength()):
        result[node.getData(index)["url"]] = list()
    for index in range(node.getLength()):
        n = node.getData(index)
        
        if n["link"] is not None:
            result[n["url"]].append(nodeToList(n["link"]))
    
    return result

def get_status_code(url):
    try:
        r=requests.get(url)
        return r.status_code
    
    except requests.exceptions.RequestException as erra:
        print("error occuerd! passing This url")
        return 200


def nodeTravel(node, bs, arg, url_table, count, max_depth):
    if count < max_depth:
        for index in range(node.getLength()):
            d = node.getData(index)
            parsed_uri_1 = urlparse(d["url"]).netloc
            parsed_uri_2 = urlparse(arg.url).netloc
            
            # Ohter domain do not crawl.
            if parsed_uri_1 != parsed_uri_2:
                continue
            
            r = request(d["url"], header)
            
            # Check recived response
            if r is None:
                continue
            
            status_code = get_status_code(d["url"])
            bs = bs4.BeautifulSoup(r.page_source, "html.parser")
            node_link, url_table = url_parser(bs, arg, url_table)
            node.modifyData(index, "link", node_link)
            node.modifyData(index, "status_code", status_code)
            
        
        for index in range(node.getLength()):
            link = node.getData(index)["link"]
            
            if link is not None:
                count += 1 
                nodeTravel(link, bs, arg, url_table, count, max_depth)

if __name__ == "__main__":
    url_table = list()
    arg = command_parser()
    
    header = ''


    print("URL crawling with selenium")
    print("Target URL : %s"%arg.url)
    print("Login stage is running....")
    init_login(arg.url)
    
    r = request(arg.url, header)
    
    # Check recived response
    if r is None:
        exit()
    bs = bs4.BeautifulSoup(r.page_source, "html.parser")
    root, url_table = url_parser(bs, arg, url_table)
    
    
    nodeTravel(root, bs, arg, url_table, 0, 20)
    
    result = nodeToList(root)
    
    # second filter to delete not in scope
    key1=arg.url.index('.')
    key2=arg.url[::-1].index('.',2)
    keyword=arg.url[key1:len(arg.url)-key2]

    for url in result:
        if keyword not in url:
            del url
    
    result = json2html.json2html(result, 1)
    

    createFolder('data')
    writeFile(f"./data/{arg.url[8:-1]}.html",result)
    print("Finishing Url Crawling")