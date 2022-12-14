import requests 
# from urllib.request import urlopen
# from pwrite_ import pwrite_
from time import sleep
# import sublist3r 
from seleniumwire import webdriver
from seleniumwire.utils import decode
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
from datetime import datetime
import random, string


### DEFINITIONS ###

LOGS = "logs.txt"
URLS = "urls.txt"
TODAY = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
FOUND = "vulnerable.txt"

## Write to vulnerable
with open(FOUND, "a+") as f:
  f.write("********** Run on: " + str(TODAY) +" **********")

def randomword(length):
  letters = string.ascii_lowercase
  return ''.join(random.choice(letters) for i in range(length))


def decode_req(request):
  body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
  return body

def https_getter(url):
  return url.replace("http", "https")

def write_(s):
  f = open(LOGS, "a+")
  print(s)
  f.write(s + "\n")
  f.close()

def writefound(s):
  f = open(FOUND, "a+")
  print(s)
  f.write(s + "\n")
  f.close()

### CODE START ###

lst = []

with open (URLS, "r+") as f:
  lst = f.readlines()


lst = [l.strip() for l in lst]

attack_lst = [
  r"/"
  # r"%0A",
  # r"%3Fname=",
  # r"%3B",
  # r"%23",
  # r"%2F",
  # r"%25%30%41",
  # r"%25%30%30",
  # r"%25%33%46",
  # r"%25%33%42",
  # r"%25%32%33", 
  # r"%25%32%46",
  # r"%40",
  # r"%25%34%30",
  # r"%5C",
  # r"%25%35%43",
  # r"%3A",
  # r"%25%33%41",
  # r"@"
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
  "cf-cache-status":["MISS", "EXPIRED"],
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


# attack_string = "teamchae.css"

## start header

write_("********** Run on: " + str(TODAY) +" **********")

## Get stuff
for url_ in lst:
  ## url we will use. based on research, css files have the most success. 
  ## we use a unique name so that it is a unique file
  attack_string = randomword(5) + ".css"


  ## Add http://, may not be necessary.
  # sublister_domain = url_
  url_ = "http://" + url_

  # ## Get subdomains (not needed for now)
  # write_("[!] getting subdomains for", url_)
  # subdomains = sublist3r.main(
  #   sublister_domain, 5, sublister_domain + "_subdomains.txt", 
  #   ports=None, silent=False, verbose= False, enable_bruteforce= False, engines=None
  # )

  # exit()

  write_(" ====== [i] testing for " +  str(url_) + " ======")
  r1 = requests.get(url_)
  r2 = requests.get(url_)

  if r1.content == r2.content:
    write_("[!] static page detected, abort test!")
  else:
    ## step 2
    ## add attack url
    write_("[!] step 1 passed (dynamic page), moving on to step 2...")
    for suffix in attack_lst:
      write_("---------------------------------")
      sleep(0.3) # prevent unintended spam
      # make attack url
      attack_url = url_ + suffix + attack_string
      
      failed = False

      ## Use requests
      ##  Get the URL
      chrome_options = webdriver.ChromeOptions()
      chrome_options.add_argument("--disable-extensions")
      chrome_options.add_argument("--disable-gpu")
      chrome_options.add_argument("--headless")

      ## make driver
      driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

      # get url
      try:
        driver.get(attack_url)
      except Exception as e:
        write_("[!] error:" + str(e))
        break

      # time.sleep(10)
      # driver2.get(url_)

      # check url
      with open(LOGS, "a+") as f:
        for request in driver.requests:
          # write_((str(request)), len(str(request)))
          url = str(request.url).strip()

          ## find domain
          # remove www
          parsed_url = urlparse(url).netloc.replace("www.", "")
          # write_("Domain:", parsed_url)

          ## domain to compare with
          parsed_compare = urlparse(url_).netloc.replace("www.", "")
          # write_("Compare:", parsed_compare)

          ## compare domain, we only want the domains that match our url_
          if parsed_url == parsed_compare:
            ## NOTE main
            # write_ url
            write_("------ " + url + " ------")
            for status in cache_status:
              try:
                cache_response = request.response.headers[status]
                # None, HIT, MISS, etc.
                write_("[i] " + str(status) + ": " + str(cache_response))

                ## check for cache response
                if cache_response == None:
                  write_("[!] hit or miss status not present for " + str(status))
                else:
                  selenium_url = request.url
                  miss_list = miss.get(status) # get list of codes that match miss
                  if cache_response in miss_list: # first req is a miss, move to stage 2
                    write_("[i] first request for " + str(selenium_url) + " is a MISS, now checking for HIT...")

                    # check for second cache HIT
                    # make second driver
                    driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)


                    try:
                      driver2.get(attack_url)
                    except Exception as e:
                      write_("[!] error: " + str(e))
                      break

                    for request2 in driver2.requests:
                      # write_((str(request)), len(str(request)))
                      url2 = str(request2.url).strip()

                      ## find domain
                      # remove www
                      parsed_url2 = urlparse(url2).netloc.replace("www.", "")
                      # print("Domain:", parsed_url2)

                      ## domain to compare with
                      parsed_compare2 = urlparse(url_).netloc.replace("www.", "")
                      # print("Compare:", parsed_compare2)

                      if parsed_url2 == parsed_compare2:
                        write_("--- checking for HIT for " + str(url2) + " ---")
                        for status2 in cache_status:
                          try:
                            cache_response2 = request2.response.headers[status2]
                            # write_("line 224 [i] " + str(status2) + ": " + str(cache_response2))

                            if cache_response2 == None:
                              write_("[!] HIT or MISS status not present for " + str(status2))
                            else:
                              selenium_url = request.url
                              hit_list = hit.get(status2) # get list of codes that match hit
                              if cache_response2 in hit_list: # req is a miss, website is vulnerable 
                                writefound("[i] second request is a HIT, " + str(url2) + " is vulnerable to WCD!")
                                break
                          except Exception as e:
                            write_("[!] Error: " + str(e))
                      else:
                        write_("[i] no HIT found, website is not vulnerable. ")
                        break
                  else:
                    write_("[!] first request is not a MISS")
                    break
              except Exception as e:
                write_("[!] error " + str(e))
                pass