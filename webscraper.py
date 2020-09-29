# Web Scraping Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
from selenium import webdriver
import requests
import sys
import os
import shutil
from selenium import webdriver

team_dict = {
    "Atlanta Hawks": "ATL", "Boston Celtics": "BOS", "Brooklyn Nets": "BRK",
    "Chicago Bulls": "CHI", "Charlotte Hornets": "CHO", "Charlotte Bobcats": "CHA",
    "Cleveland Cavaliers": "CLE", "Dallas Mavericks": "DAL", "Denver Nuggets": "DEN",
    "Detroit Pistons": "DET", "Golden State Warriors": "GSW", "Houston Rockets": "HOU",
    "Indiana Pacers": "IND", "Los Angeles Clippers": "LAC", "Los Angeles Lakers": "LAL",
    "Vancouver Grizzlies": "VAN", "Memphis Grizzlies": "MEM", "Miami Heat": "MIA",
    "Milwaukee Bucks": "MIL", "Minnesota Timberwolves": "MIN", "New Orleans Pelicans": "NOH",
    "New Orleans/Oklahoma City Hornets": "NOK", "New Orleans Hornets": "NOH", "New York Knicks": "NYK",
    "Seattle SuperSonics": "SEA", "Oklahoma City Thunder": "OKC", "Orlando Magic": "ORL",
    "Philadelphia 76ers": "PHI", "Phoenix Suns": "PHO", "Portland Trail Blazers": "POR",
    "Sacramento Kings": "SAC", "San Antonio Spurs": "SAS", "Toronto Raptors": "TOR",
    "Utah Jazz": "UTA", "Washington Wizards": "WAS", "Washington Bullets": "WSB"
            }


def train(year_start, year_end):
        year_start = int(year_start)
        year_end = int(year_end) + 1
        assert(year_start>=2000 and year_end<=2020)
        months = {"october": 1, "november": 2, "december": 3, "january": 4, "february": 5, "march": 6}
        parent_dir = os.getcwd()
        new_path = os.path.join(parent_dir, "training_data")
        os.chdir(new_path)

        for year in range(year_start,year_end):
            for m in months:
                game_no = 0
                year_str = str(year-1) + '-' + str(year)[2:]
                # CHROMEDRIVER PATH HERE IF NEEDED
                d = webdriver.Chrome(executable_path=parent_dir+'\chromedriver.exe')
                url = 'https://stats.nba.com/teams/advanced/?sort=W&dir=-1&Season={}&SeasonType=Regular%20Season&Month={}'.format(year_str, months[m])
                d.get(url)
                s = BeautifulSoup(d.page_source, 'html.parser').find('table')
                headers, [_, *data] = [i.getText().strip() for i in s.find_all('th')], [[i.getText().strip() for i in b.find_all('td')] for b in s.find_all('tr')]
                final_data = [i for i in data if len(i) > 1]
                df1 = pd.DataFrame(final_data, columns = headers[:20])
                del df1['']
                df1.loc[(df1['TEAM']=='LA Clippers'), 'TEAM']= 'Los Angeles Clippers'       #After 2016, The Los Angeles Clippers were rebranded the 'LA Clippers', but this doesn't show on basketball reference

                url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(year,m)
                html = urlopen(url)
                soup = BeautifulSoup(html, features="lxml")
                table = soup.find('table')
                header = [th.getText() for th in table.findAll('tr', limit=2)[0].findAll('th')]
                header[2:6] = ['team1', 'team1pts', 'team2', 'team2pts']
                basic_data = table.findAll('tr')[2:]
                g_data = [[td.getText() for td in basic_data[i].findAll(['td','th'])] for i in range(len(basic_data))]
                games = pd.DataFrame(g_data, columns = header)
                games = games.drop(['Date', '\xa0', '\xa0', 'Attend.', 'Notes', 'Start (ET)'], axis=1)

                games["team1pts"] = games["team1pts"].astype(str).astype(int)
                games["team2pts"] = games["team2pts"].astype(str).astype(int)

                games = games.merge(df1.add_prefix('1'), how='left', right_on = ['1TEAM'], left_on = ['team1']).drop(['1TEAM'], axis=1)
                games = games.merge(df1.add_prefix('2'), how='left', right_on = ['2TEAM'], left_on = ['team2']).drop(['2TEAM'], axis=1)

                games['net'] = games['team1pts'] - games['team2pts']

                filename = '{}{}.csv'.format(year, months[m])
                games.to_csv(filename)


def reg_szn_games(year_start, year_end):
    year_start = int(year_start)
    year_end = int(year_end) + 1
    assert(year_start>=1946 and year_end<=2021)
    months = ["october", "november", "december", "january", "february", "march"]

    # Make directory for files
    parent_dir = os.getcwd()
    reg_szn_games_path = os.path.join(parent_dir, "regular_season_games")
    os.chdir(reg_szn_games_path)

    for year in range(year_start,year_end):

        # All games in current year
        year_path = os.path.join(reg_szn_games_path, str(year))
        if not os.path.exists(year_path):
            os.mkdir(year_path)
        else:
            continue

        for m in months:
            game_no = 0
            # Get links to game stats
            url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(year,m)
            html = urlopen(url)
            soup = BeautifulSoup(html, features="lxml")
            table = soup.find('table')
            t_rows = table.find_all('tr')
            ls = []
            count = 0
            for tr in t_rows:
                for a in tr.find_all('a', href = True):
                    ls.append(a['href']);
            ls = ls[3:]
            ls = ls[::4]

            for addr in ls:
                # Get data for individual games
                game_url = 'https://www.basketball-reference.com' + addr
                html2 = urlopen(game_url)
                header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:32.0) Gecko/20100101 Firefox/32.0',}
                r = requests.get(game_url, headers = header, verify = False)
                soup2 = BeautifulSoup(r.text, features="lxml")
                tables = soup2.find_all("table")
                if len(tables)==16:
                    team1_basic = tables[0]
                    team1_adv = tables[7]
                    team2_basic = tables[8]
                    team2_adv = tables[15]
                else:
                    overtimes = int((len(tables)-16)/2)
                    team1_basic = tables[0]
                    team1_adv = tables[7+overtimes]
                    team2_basic = tables[8+overtimes]
                    team2_adv = tables[15+(overtimes*2)]


                basic_header= [th.getText() for th in team1_basic.findAll('tr', limit=3)[1].findAll('th')]
                basic_header[0] = 'Players'
                adv_header = [th.getText() for th in team1_adv.findAll('tr', limit=3)[1].findAll('th')]
                adv_header[0] = 'Players'

                r1b = team1_basic.findAll('tr')[2:]
                stats_1b = [[td.getText() for td in r1b[i].findAll(['td', 'th'])] for i in range(len(r1b)) if i!=5]
                df1b = pd.DataFrame(stats_1b, columns = basic_header)

                r1a = team1_adv.findAll('tr')[2:]
                stats_1a = [[td.getText() for td in r1a[i].findAll(['td', 'th'])] for i in range(len(r1a)) if i!=5]
                df1a = pd.DataFrame(stats_1a, columns = adv_header)

                r2b = team2_basic.findAll('tr')[2:]
                stats_2b = [[td.getText() for td in r2b[i].findAll(['td', 'th'])] for i in range(len(r2b)) if i!=5]
                df2b = pd.DataFrame(stats_2b, columns = basic_header)

                r2a = team2_adv.findAll('tr')[2:]
                stats_2a = [[td.getText() for td in r2a[i].findAll(['td', 'th'])] for i in range(len(r2a)) if i!=5]
                df2a = pd.DataFrame(stats_2a, columns = adv_header)

                mydivs = soup2.findAll("div", {"class": "scores"})
                score_arr = []
                for d in mydivs:
                    score_arr.append(int(d.get_text()))

                teamnames = soup2.find_all("a", {"itemprop": "name"})
                headers = [n.getText() for n in teamnames]
                outcome = pd.DataFrame([score_arr], columns = headers)

                new_dir = m + str(game_no)
                local = os.path.join(year_path, new_dir)
                os.mkdir(local)

                outcome.to_csv("outcome.csv")
                shutil.move("outcome.csv", local)

                df1b.to_csv("team1basic.csv")
                shutil.move("team1basic.csv", local)

                df1a.to_csv("team1adv.csv")
                shutil.move("team1adv.csv", local)

                df2b.to_csv("team2basic.csv")
                shutil.move("team2basic.csv", local)

                df2a.to_csv("team2adv.csv")
                shutil.move("team2adv.csv", local)

                game_no += 1


def season_stats(year):
    year = int(year)
    assert(year>=1946 and year<=2020)
    parent_dir = os.getcwd()
    season_stats = os.path.join(parent_dir, "season_stats_{}".format(year))
    os.mkdir(season_stats)
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)
    html = urlopen(url)
    soup = BeautifulSoup(html, features = "lxml")
    soup.find_all('tr', limit = 2)
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')][1:]
    r = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in r[i].findAll('td')] for i in range(len(r))]
    df = pd.DataFrame(player_stats, columns = headers)
    df.to_csv("stats.csv")
    shutil.move("stats.csv", season_stats)


def main():
    if sys.argv[1] == "rsg":
        year_start = sys.argv[2]
        year_end = sys.argv[3]
        reg_szn_games(year_start, year_end)

    if sys.argv[1] == "szn":
        year = sys.argv[2]
        season_stats(year)

    if sys.argv[1] == "train":
        year_start = sys.argv[2]
        year_end = sys.argv[3]
        train(year_start, year_end)

if __name__ == "__main__":
    main()
