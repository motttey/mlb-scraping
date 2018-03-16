import json
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd

url = "https://www.baseball-reference.com/"

def main():
	r = urllib.request.urlopen(url).read()
	soup = BeautifulSoup(r, 'lxml')
	print(soup.prettify()[0:1000])

if __name__ == '__main__':
    main()