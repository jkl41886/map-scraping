import requests
import sys, string
from bs4 import BeautifulSoup
from bs4.element import Tag
from time import sleep
import bs4.element


# import mechanize
# import cookielib
# keyword1 = "Motel 6 Elizabeth - Newark Liberty International Airport"
keyword = "Destiny+Scotland+-+St+Andrew+Square+Apartments"
# keyword = "apartments near Scotland, UK"
# keyword = "apartments+near+Scotland,+UK"
# keyword = ' '.join(sys.argv[1:])
search_url = "https://www.google.com/maps/search/"
place_url = "https://www.google.com/maps/place/"
url = place_url+keyword
res = requests.get(url)

res.raise_for_status()
search_result = bs4.BeautifulSoup(res.text, "html.parser" )
# print(noStarchSoup)
print(url)
lists = search_result.find(attrs = {"class": "widget-pane-link"})
print(lists)
# for building in lists:
#     print(type(building))
f = open("bs.txt", "w")
f.write(res.text)
# s = requests.Session()
# print(s.post("address"))
# = s.post(.. etc)
