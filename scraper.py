import json
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests

url = "https://www.baseball-reference.com/"
team_url = "https://www.baseball-reference.com/teams/ATL/2019.shtml"

def main():
	headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }
	candidate_urls = []

	req = requests.get(url=team_url, headers=headers)
	soup = BeautifulSoup(req.content, features="html.parser")

	table_body = soup.find_all('table', {'id' :'team_batting'})[0].find('tbody')
	tr_list = table_body.find_all('tr')
	for tr in tr_list:
		td_list = tr.find_all('td')
		if len(td_list) > 1:
			player_name = td_list[1]["data-append-csv"]
			b_stats_url = "https://www.baseball-reference.com/players/gl.fcgi?id=" + player_name + "&t=b&year=2018"
			print(b_stats_url)

			candidate_urls.append(b_stats_url)
	
	print(len(candidate_urls))

if __name__ == '__main__':
	main()