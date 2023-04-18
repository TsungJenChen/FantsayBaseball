import webbrowser

import requests
from datetime import datetime
import pandas as pd
import WebCrawling.Auth as auth
import time

LEAGUEID = auth.LEAGUEID
URL = auth.URL
KEY = auth.KEY
SECRET = auth.SECRET
CODE = auth.CODE


def get_authorization_url():
    ###
    # According to the Documentation (https://developer.yahoo.com/oauth2/guide/flows_authcode/):
    #   1. 'redirect_uri':
    #       If the user should not be redirected to your server, you should specify the callback as oob (out of band).
    #   2. 'response_type' should be set as "code"
    #   3. References: https://github.com/edwarddistel/yahoo-fantasy-baseball-reader,
    #                  https://qiita.com/prs-watch/items/bb2f05c7983ec8fa0cb3
    ###

    params = {
              'client_id': KEY,
              'redirect_uri': 'oob',
              'response_type': 'code'
              }
    response = requests.get("https://api.login.yahoo.com/oauth2/request_auth", params=params, allow_redirects=False)

    if response.status_code == 302:
        print('successful')
        webbrowser.open(response.url, new=1)

def get_access_token():

    CODE = input("Please enter the authorization key:")
    auth.CODE = CODE

    params = {
        'client_id': KEY,
        'client_secret': SECRET,
        'redirect_uri': 'oob',
        'grant_type':'authorization_code',
        'code': CODE
    }

    tokens = requests.post('https://api.login.yahoo.com/oauth2/get_token', data=params)

    if tokens.status_code != 200:
        CODE = input("There might be a typo in the key you just entered. Please enter the correct authorization key:")
        auth.CODE = CODE
        tokens = requests.post('https://api.login.yahoo.com/oauth2/get_token', data=params)
    return tokens.json()  # Return the result as a dict object


def get_league_info(soup):
    pass


def Draft_Results_Scraping(draft_soup):

    ###
    # To get the Draft Result
    # param: Draft_soup: url link
    # output: pd.DataFrame. The draft result.
    ###

    output_dataset = pd.DataFrame(columns=["Pick", "Round", "Team_Key", "Player_Key"])
    for d in draft_soup.find_all("draft_result"):
        new_row = {}
        for i in range(len(d.find_all())):
            if i == 3:
                new_row[output_dataset.columns[i]] = d.find_all()[i].text[6:]
            else:
                new_row[output_dataset.columns[i]] = d.find_all()[i].text
        output_dataset = output_dataset.append(new_row, ignore_index=True)
    return output_dataset


