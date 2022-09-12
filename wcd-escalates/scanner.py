##  Import webdriver from Selenium Wire instead of Selenium
import selenium
from seleniumwire import webdriver
from seleniumwire.utils import decode
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urlparse
import time

LOGS = "logs.txt"

def decode_req(request):
  body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
  return body

def https_getter(url):
  return url.replace("http", "https")

##  Get the URL
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

# driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

lst = [
  "http://sgcarmart.com"
]

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

## Get stuff
for url_ in lst:
  ## make driver
  driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

  # get url
  driver.get(url_)
  # time.sleep(10)
  # driver2.get(url_)

  # check url
  with open(LOGS, "a+") as f:
    for request in driver.requests:
      # print((str(request)), len(str(request)))
      url = str(request.url).strip()

      ## find domain
      # remove www
      parsed_url = urlparse(url).netloc.replace("www.", "")
      # print("Domain:", parsed_url)

      ## domain to compare with
      parsed_compare = urlparse(url_).netloc.replace("www.", "")
      # print("Compare:", parsed_compare)

      ## compare domain, we only want the domains that match our url_
      if parsed_url == parsed_compare:
        # # if True:
        # f.write("=========================================\n")
        # f.write(str(request.url) + "\n") # <--------------- Request url
        # # f.write(str(request.headers)) # <----------- Request headers
        
        # ## Body handled by requests (should be)
        # # f.write("Body:")
        # # body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
        # # f.write(str(body))

        # f.write(str(request.response.headers)) # <-- Response headers
        # f.write("=========================================")
        # # print("Pass!")

        ## NOTE main
        # print url
        print("=======" + url + "=======")
        for status in cache_status:
          try:
            print(status, ":", request.response.headers[status])
          except Exception as e:
            print("[!] error", e)
            pass

  # driver2.get(url_)

# d1 = sorted([r for r in driver.requests if r in lst])
# d2 = sorted([r for r in driver.requests if r in lst])

##  Print request headers
# for i in range(len(d1)):
#   request = d1[i]
#   request2 = d2[i]

#   body = decode_req(request)
#   body2 = decode_req(request)

#   ## step 1
#   if body == body2:
#     print("[!] static page detected, abort test!")
#   else:
#     ## step 2
#     ## add attack url
#     print("[!] step 1 passed, moving on to step 2...")


  

