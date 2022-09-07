import uuid
import os
import argparse
from bs4 import BeautifulSoup
from time import sleep


def get_rand_string(length):
    
    # Returns a random string of length string_length.
    random = str(uuid.uuid4())
    random = random.upper() 
    random = random.replace("-","") 
    return random[0:length] 

def command_parser():
    parser = argparse.ArgumentParser(description = "Web Cache Deception helper")
    
    parser.add_argument("--url", required=True, help="Input url or --url [Parent url] [Sub url (option)], --url http://test.com/")
    parser.add_argument("--excloud", required=False, default=None, nargs='+', help="Input exclouded url, --excloud http://test.com/logout http://test.com/login")
    
    arg = parser.parse_args()

    return arg

def writeFile(file,data):
    f=open(file,'w+',encoding='utf-8')
    f.write(data)
    f.close()

def readFile(file):
    f=open(file,'r+',encoding='utf-8')
    data=f.read()
    f.close()
    return data

def html2list(file):
    urls=list()
    file_data=readFile(file)
    soup = BeautifulSoup(file_data, 'html.parser')
    for i in soup.find_all('div',class_='list'):
        urls.append(i.text)
    return urls


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print ('Error: Creating directory. ' +  directory)
 

def pre_path_wcd(url,ext,urlset):
    if ext=='php':
        index1=url.index('php')+3
        payload=url[:index1]+'/'+'WCDtest'+'/'
        print(payload)
        urlset.add(payload)
    else:
        index1=url[::-1].index('/')
        index2=url.index('.'+ext)
        exist=url[len(url)-index1:index2]
        payload=url.replace(exist,'WCDtest')
        urlset.add(payload)