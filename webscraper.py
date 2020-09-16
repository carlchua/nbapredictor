# Web Scraping Imports
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import filedialog

# REGULAR SEASON
month = ['october', 'november', 'december', 'january', 'february', 'march']
for year in range(2017,2020)
    for m in months:
        url = "https://www.basketball-reference.com/leagues/NBA_{}_games-{}.html".format(year,m)
        html = urlopen(url)
        soup = BeautifulSoup(html)
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
            game_url = 'https://www.basketball-reference.com' + addr
            html2 = urlopen(game_url)
            soup2 = BeautifulSoup(html2)
            tables = soup.find_all("table")
            team1_basic = tables[0]
            team1_adv = tables[7]
            team2_basic = tables[8]
            team2_adv = tables[15]

            t1_b_header = [th.getText() for th in team1_basic.findAll('tr', limit=3)[1].findAll('th')][1:]
            r1b = team1_basic.findAll('tr')[2:]
            stats_1b = [[td.getText() for td in r1b[i].findAll('td')] for i in range(len(r1b))]
            df1b = pd.DataFrame(stats_1b, columns = r1_b_header)

            t1_a_header = [th.getText() for th in team1_adv.findAll('tr', limit=3)[1].findAll('th')][1:]
            r1a = team1_basic.findAll('tr')[2:]
            stats_1a = [[td.getText() for td in r1a[i].findAll('td')] for i in range(len(r1a))]
            df1a = pd.DataFrame(stats_1a, columns = r1_a_header)

            t2_b_header = [th.getText() for th in team2_basic.findAll('tr', limit=3)[1].findAll('th')][1:]
            r2b = team1_basic.findAll('tr')[2:]
            stats_2b = [[td.getText() for td in r2b[i].findAll('td')] for i in range(len(r2b))]
            df2b = pd.DataFrame(stats_2b, columns = r2_b_header)


            t2_a_header = [th.getText() for th in team2_adv.findAll('tr', limit=3)[1].findAll('th')][1:]
            r2a = team1_basic.findAll('tr')[2:]
            stats_2a = [[td.getText() for td in r2a[i].findAll('td')] for i in range(len(r2a))]
            df2a = pd.DataFrame(stats_2a, columns = r2_a_header)





# ML Imports
import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.function as f
from torch.utils.data import dloader
