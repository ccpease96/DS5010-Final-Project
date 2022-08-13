from lineups_v7 import *
import pandas as pd

#test to make sure away_lineups are pulling in correctly, expecting Team, Position, Name, Bats, Game Number identifier, and batting_order identifier
def test_away():
    away = get_away_lineups()
    print(away)

    return away

test_away()

#test to make sure home_lineups are pulling in correctly, expecting Team, Position, Name, Bats, Game Number identifier, and batting_order identifier
def test_home():
    home = get_home_lineups()
    print(home)

test_home()

def test_away_pitchers():
    away_pitchers = get_away_pitchers()
    print(away_pitchers)

test_away_pitchers()

def test_home_pitchers():
    home_pitchers = get_home_pitchers()
    print(home_pitchers)

    return home_pitchers

test_home_pitchers()

def test_merge():
    merging = merge(test_away(), test_home_pitchers())
    print(merging)

    return merging

test_merge()

def test_hitting_data():
    hitting = hitting_data(test_merge())

    print(hitting)

    return hitting

test_hitting_data()

def test_send_groups_to_excel():
    send_groups_to_excel(test_hitting_data())
    read_excel = pd.read_excel('SD08-13-2022.xlsx')
    print(read_excel)

test_send_groups_to_excel()

def test_replace():
    replacement = replace('BOS')

test_replace()




