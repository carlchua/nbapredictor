# Web Scraping Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import re
import requests
import sys
import os
import shutil

# REGULAR SEASON
def reg_szn_games(year_start, year_end):
    year_start = int(year_start)
    year_end = int(year_end) + 1
    assert(year_start>=1946 and year_end<=2021)
    months = ["october", "november", "december", "january", "february", "march"]

    # Make directory for files
    parent_dir = os.getcwd()
    reg_szn_games_path = os.path.join(parent_dir, "regular_season_games")
    os.mkdir(reg_szn_games_path)

    for year in range(year_start,year_end):

        # All games in current year
        year_path = os.path.join(reg_szn_games_path, str(year))
        os.mkdir(year_path)

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
                team1_basic = tables[0]
                team1_adv = tables[7]
                team2_basic = tables[8]
                team2_adv = tables[15]

                t1_b_header = [th.getText() for th in team1_basic.findAll('tr', limit=3)[1].findAll('th')][1:]
                r1b = team1_basic.findAll('tr')[2:]
                stats_1b = [[td.getText() for td in r1b[i].findAll('td')] for i in range(len(r1b)) if i!=5]
                df1b = pd.DataFrame(stats_1b, columns = t1_b_header)

                t1_a_header = [th.getText() for th in team1_adv.findAll('tr', limit=3)[1].findAll('th')][1:]
                r1a = team1_adv.findAll('tr')[2:]
                stats_1a = [[td.getText() for td in r1a[i].findAll('td')] for i in range(len(r1a)) if i!=5]
                df1a = pd.DataFrame(stats_1a, columns = t1_a_header)

                t2_b_header = [th.getText() for th in team2_basic.findAll('tr', limit=3)[1].findAll('th')][1:]
                r2b = team2_basic.findAll('tr')[2:]
                stats_2b = [[td.getText() for td in r2b[i].findAll('td')] for i in range(len(r2b)) if i!=5]
                df2b = pd.DataFrame(stats_2b, columns = t2_b_header)


                t2_a_header = [th.getText() for th in team2_adv.findAll('tr', limit=3)[1].findAll('th')][1:]
                r2a = team2_adv.findAll('tr')[2:]
                stats_2a = [[td.getText() for td in r2a[i].findAll('td')] for i in range(len(r2a)) if i!=5]
                df2a = pd.DataFrame(stats_2a, columns = t2_a_header)

                mydivs = soup2.findAll("div", {"class": "scores"})
                score_arr = []
                for d in mydivs:
                    score_arr.append(d.get_text())

                score1= re.sub("[^0-9]", "", score_arr[0])
                score2 = re.sub("[^0-9]", "", score_arr[1])

                winner = max([(score1, 1), (score2, 2)])[1]

                new_dir = m + str(game_no)
                local = os.path.join(year_path, new_dir)
                os.mkdir(local)
                f = open(os.path.join(local, "winner.txt"), "w+")
                buff = str(winner) + "\n" + score1 + "\n" + score2
                f.write(buff)
                f.close()

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

if __name__ == "__main__":
    main()
