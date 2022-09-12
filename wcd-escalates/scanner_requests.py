import requests 
# from urllib.request import urlopen
# from pprint import pprint
from time import sleep
# import sublist3r 


LOGS = "logs.txt"
URLS = "urls.txt"

lst = []

with open (URLS, "r+") as f:
  lst = f.readlines()

lst = [l.strip() for l in lst]

attack_lst = [
  r"/",
  r"%0A",
  r"%3Fname=",
  r"%3B",
  r"%23",
  r"%2F",
  r"%25%30%41",
  r"%25%30%30",
  r"%25%33%46",
  r"%25%33%42",
  r"%25%32%33",
  r"%25%32%46",
  r"%40",
  r"%25%34%30",
  r"%5C",
  r"%25%35%43",
  r"%3A",
  r"%25%33%41",
  r"@"
]

hit = {
  "X-Cache": ["HIT", "TCP_HIT", "HIT from *"],
  "server-timing" : ["desc=HIT", "desc=TCP_HIT"],
  "cf-cache-status": ["HIT"], # include DYNAMIC ?
  "X-cache": ["TCP_HIT", "TCP_REMOTE_HIT"],
  "X-Proxy-Cache":["HIT"],
  "X-Rack-Cache":["hit"],
  "x-cache-info":["cached"],
  "x-cache": ["Hit from cloudfront"]
}

miss = {
  "X-Proxy-Cache" : ["MISS"],
  "X-Rack-Cache" : ["miss"],
  "x-cache-info" : ["caching"],
  "server-timing":["desc=MISS", "desc=TCP_MISS"],
  "X-Cache":["MISS","TCP_MISS","MISS from *"],
  "cf-cache-status":["MISS"],
  "X-cache":["TCP_MISS"],
  "cdn_cache_status":["miss"],
  "x-cache": ["Miss from cloudfront"]
}

cache_status = [
  "server-timing", 
  "X-Cache", 
  "X-Cache-Remote",
  "cf-cache-status",
  "cdn_cache_status",
  "x-cache",
  "X-Proxy-Cache",
  "X-Rack-Cache",
  "x-cache-info"
]


## url we will use. based on research, css files have the most success. 
## we use a unique name so that it is a unique file
attack_string = "teamchae.css"

## Get stuff
for url_ in lst:
  ## Add http://, may not be necessary.
  # sublister_domain = url_
  url_ = "http://" + url_

  # ## Get subdomains
  # print("[!] getting subdomains for", url_)
  # subdomains = sublist3r.main(
  #   sublister_domain, 5, sublister_domain + "_subdomains.txt", 
  #   ports=None, silent=False, verbose= False, enable_bruteforce= False, engines=None
  # )

  # exit()

  print(" ====== [i] testing for", url_, "======")
  r1 = requests.get(url_)
  r2 = requests.get(url_)

  if r1.content == r2.content:
    print("[!] static page detected, abort test!")
  else:
    ## step 2
    ## add attack url
    print("[!] step 1 passed (dynamic page), moving on to step 2...")
    for suffix in attack_lst:
      print("---------------------------------")
      sleep(0.3)
      # make attack url
      attack_url = url_ + suffix + attack_string
      
      failed = False

      ## Use requests
      try:
        print("[i] trying", attack_url)
        ar1 = requests.get(attack_url)
        sleep(0.3)
        ar2 = requests.get(attack_url)

        h1 = ar1.headers
        # print(type(h1))
        h2 = ar2.headers
      except Exception as e:
        print("[!] error:", e)
        failed = True

      if failed == False:
        ## get cache status
        ## make sure first is a cache hit and second is a cache miss
        for status in cache_status:
          print("====== [i] trying " + status + " ======")
          h1_status = h1.get(status)
          print("[i] 1st status: ", h1_status)
          h2_status = h2.get(status)
          print("[i] 2nd status: ", h2_status)


          # check for first cache hit 
          if h1_status == None or h2_status == None: # if any is none, there is no chance of wcd.
            print("[!] hit or miss status not present for", status)
          else: # status is present. check if the code matches
            hit_list = hit.get(status) # get list of codes that match hit
            status_list = h1_status.split(" ")
            for word in status_list:
              if word in hit_list: # first req is a hit, move to stage 2
                print("[i] first request is a HIT, now checking for MISS...")

                # check for second cache miss
                miss_list = miss.get(status)
                status2_list = h2_status.split(" ")
                for word2 in status2_list:
                  if word2 in miss_list:
                    print("[i] second request is a MISS, website is vulnerable to WCD!")
                else:
                  print("[i] no miss found, website is not vulnerable. ")
                  break
              else:
                print("[!] first request is not a hit")
                break
          

      ## Use urlopen
      # try:
      #   with urlopen(attack_url) as resp1:
      #     print("[1] attack url passed:", attack_url)
      #     pass
      #   with urlopen(attack_url) as resp2:
      #     print("[2] attack url passed:", attack_url)
      #     pass
      # except Exception as e:
      #   print("[!] error: 404!")
      #   failed = True

      # if failed == False:
      #   h1 = resp1.headers.items()
      #   h2 = resp2.headers.items()

      #   print(h1)

