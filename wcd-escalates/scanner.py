##  Import webdriver from Selenium Wire instead of Selenium
import selenium
from seleniumwire import webdriver
from seleniumwire.utils import decode
from webdriver_manager.chrome import ChromeDriverManager
import time

LOGS = "logs.txt"

def decode_req(request):
  body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
  return body

##  Get the URL
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

lst = [
  "https://www.google.com/"
]

## Get stuff
for url_ in lst:
  driver.get(url_)

  time.sleep(10)
  
  driver2.get(url_)

d1 = sorted([r for r in driver.requests if r in lst])
d2 = sorted([r for r in driver.requests if r in lst])

##  Print request headers
for i in range(len(d1)):
  request = d1[i]
  request2 = d2[i]

  body = decode_req(request)
  body2 = decode_req(request)

  ## step 1
  if body == body2:
    print("[!] static page detected, abort test!")
  else:
    ## step 2
    ## add attack url
    print("[!] step 1 passed, moving on to step 2...")


  # print(type(str(request)), len(str(request)))
  # if str(request.url).strip() == "https://www.google.com/":
    # print("=========================================")
    # print(request.url) # <--------------- Request url
    # print(request.headers) # <----------- Request headers
    
    # print("Body:")
    # body = decode(request.response.body, request.response.headers.get('Content-Encoding', 'identity'))
    # print(body)

    # print(request.response.headers) # <-- Response headers
    # print("=========================================")
    # # print("Pass!")
    # pass

