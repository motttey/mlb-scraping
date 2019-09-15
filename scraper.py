import json
from bs4 import BeautifulSoup
import urllib.request
import pandas as pd
import requests

url = "https://www.baseball-reference.com/"

def get_batter_candidates(team):
	team_url = "https://www.baseball-reference.com/teams/" + team + "/2018.shtml"
	candidate_urls = []
	print(team_url)

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
	return candidate_urls

def main():
	headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }
	teams = ["NYY", "TBR", "BOS", "TOR", "BAL"]

	for team in teams:
		get_batter_candidates(team)

if __name__ == '__main__':
	main()
