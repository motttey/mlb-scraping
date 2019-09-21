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

	if len(soup.find_all('div', {'id' :'info'})) == 0: return;
	name = soup.find('div', {'id' :'info'}).find('h1').text

	print(name.encode("utf-8"))

	result_object = {}
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

	if len(soup.find_all('table', {'id' :'batting_gamelogs'})) == 0: return;

	table_body = soup.find_all('table', {'id' :'batting_gamelogs'})[0].find('tbody')
	tr_list = table_body.find_all('tr')

	if len(tr_list) > 50:
		for tr in tr_list:
			td_list = tr.find_all('td')
			for td in td_list:
				if td.text != '':
					if td["data-stat"] == "PA":
						PA = PA + int(td.text)
					elif td["data-stat"] == "H":
						hits = hits + int(td.text)
					elif td["data-stat"] == "2B":
						two_base = two_base + int(td.text)
					elif td["data-stat"] == "3B":
						three_base = three_base + int(td.text)
					elif td["data-stat"] == "HR":
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

			if len(td_list) > 2 and td_list[2].find('a'):
				game = int(tr.find('th').text)
				date_str = td_list[2].find('a').text
				team = td_list[3].text

				tdatetime = datetime.strptime(date_str, '%b %d')
				tdate = datetime(2018, tdatetime.month, tdatetime.day)
				if tdate > date_list[datetime_index]:
					single_hits = hits - two_base - three_base - home_runs
					# stats_array = [game, PA, single_hits, two_base, three_base, home_runs, RBI, SB, CS, SH, SF, BB, HBP, SO, GDP]
					stats_array = [PA, RBI, single_hits, two_base, three_base, home_runs, SB, SO, BB, HBP, SF]

					batter_stat_object = {}
					batter_stat_object["name"] = name
					batter_stat_object["team"] = team

					batter_stat_object["Number of Game"] = game
					batter_stat_object["PA"] = PA
					batter_stat_object["single_hits"] = single_hits
					batter_stat_object["two_base"] = two_base
					batter_stat_object["three_base"] = three_base
					batter_stat_object["home_runs"] = home_runs
					batter_stat_object["RBI"] = RBI
					batter_stat_object["SB"] = SB
					batter_stat_object["CS"] = CS
					batter_stat_object["SH"] = SH
					batter_stat_object["SF"] = SF
					batter_stat_object["BB"] = BB
					batter_stat_object["HBP"] = HBP
					batter_stat_object["SO"] = SO
					batter_stat_object["GDP"] = GDP

					if datetime_index >= 6:
					   batter_stat_object["Btype"] = (single_hits * 2 + SB * 2 + three_base * 2 - BB * 2 - HBP - home_runs * 3) / (game * 3.1)
					else:
					   batter_stat_object["Btype"] = (single_hits * 2 + SB * 2 + three_base * 3 - BB - two_base - home_runs * 4) / (game * 3.1)

					batter_stat_object["vec"] = stats_array
					result_object[date_list[datetime_index]] = batter_stat_object

					if datetime_index < len(date_list) - 1: datetime_index = datetime_index + 1
				# if len(td_list) > 1:
	return result_object

def main():
	teams = [
	"NYY", "TBR", "BOS", "TOR", "BAL",
	"MIN", "CLE", "CHW", "KCR", "DET",
	"HOU", "OAK", "TEX", "LAA", "SEA"
	]
	# teams = ["NYY"]

	date_list = []
	first_data = datetime(2018, 4, 1)
	current_date = first_data
	while current_date < datetime(2018, 9, 15):
		current_date = current_date + timedelta(days=14)
		date_list.append(current_date)

	result_object_array = []
	for team in teams:
		candidate_urls = get_batter_candidates(team)
		for candidate_url in candidate_urls:
			result_object = get_batter_statistics(candidate_url, date_list)
			if result_object and len(result_object) == len(date_list):
				result_object_array.append(result_object)
		# print(result_object.encode("utf-8"))

	result_json_obj = {}
	result_json_obj["time_array"] = []

	for date in date_list:
		date_obj = {}
		date_str = date.strftime('%m/%d')
		date_obj[date_str] = []
		for result_object in result_object_array:
			if date in result_object:
				date_obj[date_str].append(result_object[date])

		result_json_obj["time_array"].append(date_obj)

	fw = open('out_batter.json', 'w', encoding="utf-8")
	json.dump(result_json_obj, fw, indent=4, ensure_ascii=False)
	return
if __name__ == '__main__':
	main()
