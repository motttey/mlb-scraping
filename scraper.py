import json
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from time import strptime

import urllib.request
import pandas as pd
import requests

url = "https://www.baseball-reference.com/"

def get_batter_candidates(team):
	headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }
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

def get_batter_statistics(url, date_list):
	headers = { "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0", }
	req = requests.get(url=url, headers=headers)
	soup = BeautifulSoup(req.content, features="html.parser")

	datetime_index = 0
	name = soup.find('div', {'id' :'info'}).find('h1').text
	print(name.encode("utf-8"))

	# "試合数", "打席", "単打", "二塁打", "三塁打", "本塁打", "打点", "盗塁", "盗塁刺", "犠打", "犠飛", "四球", "死球", "三振", "併殺打"

	game = 0
	PA = 0
	hits = 0
	two_base = 0
	three_base = 0
	home_runs = 0
	RBI = 0
	SB = 0
	CS = 0
	SH = 0
	SF = 0
	BB = 0
	HBP = 0
	SO = 0
	GDP = 0

	table_body = soup.find_all('table', {'id' :'batting_gamelogs'})[0].find('tbody')
	tr_list = table_body.find_all('tr')

	if len(tr_list) > 50:
		for tr in tr_list:
			td_list = tr.find_all('td')
			for td in td_list:
				if td["data-stat"] == "PA":
					PA = PA + int(td.text)
				elif td["data-stat"] == "H":
					hits = hits + int(td.text)
				elif td["data-stat"] == "2B":
					two_base = two_base + int(td.text)
				elif td["data-stat"] == "3B":
					three_base = three_base + int(td.text)
				elif td["data-stat"] == "3B":
					home_runs = home_runs + int(td.text)
				elif td["data-stat"] == "RBI":
					RBI = RBI + int(td.text)
				elif td["data-stat"] == "SB":
					SB = SB + int(td.text)
				elif td["data-stat"] == "CS":
					CS = CS + int(td.text)
				elif td["data-stat"] == "SH":
					SH = SH + int(td.text)
				elif td["data-stat"] == "SF":
					SF = SF + int(td.text)
				elif td["data-stat"] == "BB":
					BB = BB + int(td.text)
				elif td["data-stat"] == "HBP":
					HBP = HBP + int(td.text)
				elif td["data-stat"] == "SO":
					SO = SO + int(td.text)
				elif td["data-stat"] == "GIDP":
					GDP = GDP + int(td.text)

			if len(td_list) > 2:
				date_str = td_list[2].find('a').text
				tdatetime = datetime.strptime(date_str, '%b %d')
				tdate = datetime(2018, tdatetime.month, tdatetime.day)
				if tdate > date_list[datetime_index]:
					print(tdate)
					datetime_index = datetime_index + 1
					single_hits = hits - two_base - three_base - home_runs
					stats_array = [game, PA, single_hits, two_base, three_base, home_runs, RBI, SB, CS, SH, SF, BB, HBP, SO, GDP]
					print(stats_array)
				# if len(td_list) > 1:

def main():
	# teams = ["NYY", "TBR", "BOS", "TOR", "BAL"]
	teams = ["NYY"]

	date_list = []
	first_data = datetime(2018, 4, 1)
	current_date = first_data
	while current_date.month < 10:
		current_date = current_date + timedelta(days=14)
		date_list.append(current_date)

	for team in teams:
		candidate_urls = get_batter_candidates(team)
		get_batter_statistics(candidate_urls[0], date_list)

if __name__ == '__main__':
	main()
