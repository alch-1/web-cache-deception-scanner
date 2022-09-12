import requests
from time import sleep
from pprint import pprint

url_ = input("Enter url ")
suffix = "/"
attack_string = "teamchae.css"

attack_url = url_ + suffix + attack_string

ar1 = requests.get(attack_url)
sleep(0.3)
ar2 = requests.get(attack_url)

pprint(ar1.headers.items())
pprint(ar2.headers.items())