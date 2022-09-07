import random
from random import uniform
from time import sleep
from urllib import request
import requests
# from pwn import *
from extention import possible_extention
from utils import *
from urllib.parse import urlparse,parse_qs,unquote


class WCDAttacker:
    def PathAttacker(self,url):
        payload=url.replace('WCDtest',get_rand_string(5))
        print("Checking URL : %s",payload)
        
        try:
            wcd=requests.get(payload)
            if wcd.status_code==200:
                return True
            elif 'error' in wcd.text:
                return False
            else:
                return False
        except requests.exceptions.RequestException as erra:
            print("error occuerd! passing This url")
        
        

    def QueryAttaker(self,url):

        parsed_url=urlparse(unquote(url))
        querys=parse_qs(parsed_url.query)
        for query in querys:
            param=querys[query]
            payload=url.replace(''.join(param),get_rand_string(random.randint(1,10)))
            try:
                wcd=requests.get(payload)
                print()
                if wcd.status_code==200:
                    return True
                elif 'error' in wcd.text or 'not found' in wcd.text:
                    return False
                else:
                    return False
            except requests.exceptions.RequestException as erra:
                print("error occuerd! passing This url")


class WCDhelper:

    def url_grouping(self,list_data,group):
        Query_url=list()
        Path_url=list()
        for url in list_data:
            if '?' in url:
                Query_url.append(url)
            else:
                Path_url.append(url)

        if group==2:
            print('Detect %s path url'%len(Path_url))
            return Path_url
        elif group==1:
            print('Detect %s query url'%len(Query_url))
            return Query_url


    def pathurl_helper(self,urls):
        Attacker=WCDAttacker()
        urlset=set()
        possible_url=list()
        for url in urls:
            for ext in possible_extention:
                if '.'+ext in url:
                    pre_path_wcd(url,ext,urlset)
        for url in urlset:
            sleep(uniform(5,10))
            if Attacker.PathAttacker(url):
                possible_url.append(url)
        print("Possible URL :%s"%possible_url)
        return possible_url


    def queryurl_helper(self,urls):
        Attacker=WCDAttacker()
        possible_url=list()
        for url in urls:
            sleep(uniform(5,10))
            if Attacker.QueryAttaker(url):
                possible_url.append(url)
            
        return possible_url





