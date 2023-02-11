
import pandas as pd
import numpy as np
import requests as rq
from bs4 import BeautifulSoup

# Add headings, time lag, bot, title, .etc later

def gamelog_table_scraping(BRefID, Position_Type):
    year = 2021
    br_player_page_url = f'https://www.baseball-reference.com/players/gl.fcgi?id={BRefID}&t=b&year={year}'
    br_player_page= rq.get(br_player_page_url)
    player_soup = BeautifulSoup(br_player_page.text, "html.parser")

    if Position_Type == "B":
        id = "batting_gamelogs"
        categories = ["Date", "Tm", "Opp", "PA", "AB", "R", "H", "2B", "3B", "HR", "HBP", "RBI", "BB", "SO", "SB"]


    else:
        id = "pitching_gamelogs"
        categories = ["Date", "Tm", "Opp", "Dec", "IP", "H", "R", "ER", "BB", "SO", "HR", "HBP"]

    # PlayerName BRefID
    gamelogs_table = player_soup.find("table", id=id)

    # Get column names
    gamelogs_table_column_names = gamelogs_table.find("thead").find_all("th")
    gamelogs_table_contents = gamelogs_table.find("tbody").find_all("tr", class_=lambda
        x: x != "thead")  # Skip monthly repeated column name row

    column_names = list()
    for col_index in range(0, len(gamelogs_table_column_names)):
        column_names.append(gamelogs_table_column_names[col_index].text)
    player_game_log_data = pd.DataFrame(columns=column_names[1:])

    # Main Scraping Part
    for nrow in range(0, len(gamelogs_table_contents)):
        new_row = {}
        for col_index in range(0, len(column_names) - 1):
            new_row[column_names[col_index + 1]] = gamelogs_table_contents[nrow].find_all("td")[col_index].text
        player_game_log_data = player_game_log_data.append(new_row, ignore_index=True)

    player_game_log_data_essential = player_game_log_data[categories]

    return player_game_log_data, player_game_log_data_essential