#!/usr/bin/env python
# coding: utf-8

# In[1]:


#needed packages for data
from pybaseball import cache
import pybaseball
from pybaseball import batting_stats_bref
from pybaseball import get_splits
from pybaseball import batting_stats
import pandas as pd
from pybaseball import pitching_stats_bref
from pybaseball import playerid_lookup
from pybaseball import playerid_reverse_lookup
from pybaseball import get_splits
from pybaseball import pitching_stats
import requests
import pandas as pd
from bs4 import BeautifulSoup
import time

teams_list = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CWS', 'CIN', 'CLE', 'COL', 'DET', 'FLA', 'HOU', 'KAN', 'LAA', 'LAD', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SD', 'SF', 'SEA', 'STL', 'TB', 'TEX', 'TOR', 'WAS' ]

cache.enable()


# In[2]:


def get_away_lineups():
    url = 'https://www.rotowire.com/baseball/daily-lineups.php'
    data = requests.get(url)
    
    away_lineup = pd.DataFrame(columns = ['Team', 'Position', 'Player Name', 'Bats'])

    n = 9
    a = 1
    soup = BeautifulSoup(data.content, "html.parser")

    games = soup.find_all("div", {'class': ["lineup is-mlb", "lineup is-mlb has-started"]})
    lineups = soup.find_all("div", class_="lineup__box")

    #print(lineups) #no error up to here
    for lineup in lineups:
        if lineup != None:
            #point to lineup box on rotowire
            main = lineup.find("div", class_="lineup__main")
            #beginning to get team names
            team_top = lineup.find("div", class_="lineup__top")
            team_name = team_top.find("div", class_="lineup__teams")
            if team_name != None:
                visit_name = team_name.find("div", class_="lineup__team is-visit")
                team_abbr = visit_name.find("div", class_="lineup__abbr").text
                #print(team_abbr)

            #go back to main to look at visiting lineup
            away = main.find("ul", class_="lineup__list is-visit")

            if away != None:
                players = away.find_all('li', class_="lineup__player")
                for player in players:
                    #print(team_abbr)  #printing out the correct number of team abbr per lineup
                    #away_lineup.append(team_abbr)
                    get_position = player.find("div", class_="lineup__pos").text
                    #print(get_position)
                    get_name = player.find("a", href=True)['title']
                    get_hand = player.find("span", class_="lineup__bats").text
                    entry = [team_abbr, get_position, get_name, get_hand]
                    #print(entry)
                    away_lineup.loc[len(away_lineup)] = entry
    away_lineup['Game Number'] = [int(i/n) for i, x in enumerate(away_lineup.Team)]
    away_lineup['Order'] = [int(i/a) for i, x in enumerate(away_lineup.Team)]
    
    return away_lineup


# In[3]:


def get_home_lineups():
    url = 'https://www.rotowire.com/baseball/daily-lineups.php'
    data = requests.get(url)
    
    home_lineup = pd.DataFrame(columns = ['Team', 'Position', 'Player Name', 'Bats'])

    n = 9
    a = 1
    soup = BeautifulSoup(data.content, "html.parser")

    games = soup.find_all("div", {'class': ["lineup is-mlb", "lineup is-mlb has-started"]})
    lineups = soup.find_all("div", class_="lineup__box")

    #print(lineups) #no error up to here
    for lineup in lineups:
        if lineup != None:
            #point to lineup box on rotowire
            main = lineup.find("div", class_="lineup__main")
            #beginning to get team names
            team_top = lineup.find("div", class_="lineup__top")
            team_name = team_top.find("div", class_="lineup__teams")
            if team_name != None:
                visit_name = team_name.find("div", class_="lineup__team is-home")
                team_abbr = visit_name.find("div", class_="lineup__abbr").text
                #print(team_abbr)

            #go back to main to look at visiting lineup
            home = main.find("ul", class_="lineup__list is-home")

            if home != None:
                players = home.find_all('li', class_="lineup__player")
                for player in players:
                    #print(team_abbr)  #printing out the correct number of team abbr per lineup
                    #away_lineup.append(team_abbr)
                    get_position = player.find("div", class_="lineup__pos").text
                    #print(get_position)
                    get_name = player.find("a", href=True)['title']
                    get_hand = player.find("span", class_="lineup__bats").text
                    entry = [team_abbr, get_position, get_name, get_hand]
                    home_lineup.loc[len(home_lineup)] = entry

    home_lineup['Game Number'] = [int(i/n) for i, x in enumerate(home_lineup.Team)]
    home_lineup['Order'] = [int(i/a) for i, x in enumerate(home_lineup.Team)]
    
    return home_lineup


# In[4]:


def get_away_pitchers():
    url = 'https://www.rotowire.com/baseball/daily-lineups.php'
    data = requests.get(url)
    
    away_pitcher = pd.DataFrame(columns = ['Team', 'Player Name', 'Throws'])

    soup = BeautifulSoup(data.content, "html.parser")
    n=1

    games = soup.find_all("div", {'class': ["lineup is-mlb", "lineup is-mlb has-started"]})
    lineups = soup.find_all("div", class_="lineup__box")
    #print(lineups)

    for lineup in lineups:
        if lineup != None:
            main = lineup.find("div", class_="lineup__main")

            away = main.find("ul", class_="lineup__list is-visit")
            #beginning to get team names
            team_top = lineup.find("div", class_="lineup__top")
            team_name = team_top.find("div", class_="lineup__teams")
            if team_name != None:
                visit_name = team_name.find("div", class_="lineup__team is-visit")
                team_abbr = visit_name.find("div", class_="lineup__abbr").text
                #print(team_abbr) loop is good up to this point

            if away != None:
                players = away.find_all('li', class_="lineup__player-highlight mb-0")

                for player in players:
                    player_name = player.find('div', class_="lineup__player-highlight-name")

                    get_name = player_name.find("a", href=True).text
                    #print(get_name)
                    get_hand = player_name.find("span", class_="lineup__throws").text
                    #print(get_hand)
                    entry = [team_abbr, get_name, get_hand]
                    #print(entry)
                    away_pitcher.loc[len(away_pitcher)] = entry

    away_pitcher['Game Number'] = [int(i/n) for i, x in enumerate(away_pitcher.Team)]
    return away_pitcher


# In[5]:


def get_home_pitchers():
    url = 'https://www.rotowire.com/baseball/daily-lineups.php'
    data = requests.get(url)
    
    home_pitcher = pd.DataFrame(columns = ['Team', 'Player Name', 'Throws'])

    soup = BeautifulSoup(data.content, "html.parser")
    n=1

    games = soup.find_all("div", {'class': ["lineup is-mlb", "lineup is-mlb has-started"]})
    lineups = soup.find_all("div", class_="lineup__box")
    #print(lineups)

    for lineup in lineups:
        if lineup != None:
            main = lineup.find("div", class_="lineup__main")

            home = main.find("ul", class_="lineup__list is-home")
            #beginning to get team names
            team_top = lineup.find("div", class_="lineup__top")
            team_name = team_top.find("div", class_="lineup__teams")
            if team_name != None:
                visit_name = team_name.find("div", class_="lineup__team is-home")
                team_abbr = visit_name.find("div", class_="lineup__abbr").text
                #print(team_abbr) #loop is good up to this point

            if home != None:
                players = home.find_all('li', class_="lineup__player-highlight mb-0")

                for player in players:
                    player_name = player.find('div', class_="lineup__player-highlight-name")

                    get_name = player_name.find("a", href=True).text
                    #print(get_name)
                    get_hand = player_name.find("span", class_="lineup__throws").text
                    #print(get_hand)
                    entry = [team_abbr, get_name, get_hand]
                    #print(entry)
                    home_pitcher.loc[len(home_pitcher)] = entry


    home_pitcher['Game Number'] = [int(i/n) for i, x in enumerate(home_pitcher.Team)]
    return home_pitcher


# In[6]:


def merge(lineup, pitcher):
    try:
        lineup_vs_pitcher = pd.merge(lineup, pitcher, on= 'Game Number')
        return lineup_vs_pitcher
    except:
        print("Merge was done on files that cannot be merged for this program")


# In[7]:


def hitting_data(lineup):
    
    try:
    
        #one off names with accents that won't pull through correctly unless this is done
        lineup['Player Name_x'] = lineup['Player Name_x'].replace(['Yordan Alvarez'],'Yordan Álvarez')
        lineup['Player Name_x'] = lineup['Player Name_x'].replace(['Jose Abreu'],'José Abreu')
        lineup['Player Name_x'] = lineup['Player Name_x'].replace(['Eloy Jimenez'],'Eloy Jiménez')
        lineup['Player Name_x'] = lineup['Player Name_x'].replace(['Luis Garcia'],'Luis García')
        lineup['Player Name_x'] = lineup['Player Name_x'].replace(['Yandy Diaz'],'Yandy Díaz')

        #getting list of player names to split
        list_batters = lineup['Player Name_x']

        #setting up our lists so we can add them as columns
        id_list = []
        first_name_list = []
        last_name_list = []

        #spliting and altering names based on criteria found in batting_stats library
        for batter in list_batters:
            split_name = batter.split(' ', 1)
            first_name_list.append(split_name[0])
            last_name_list.append(split_name[1])
            if split_name[0] == 'J.D.':
                split_name[0] = 'J. D.'
            elif split_name[0] == 'C.J.':
                split_name[0] = 'C. J.'
            elif split_name[0] == 'Jose' and split_name[1] == 'Iglesias':
                split_name[0] = 'José'
            elif split_name[1] == 'Diaz' and split_name[0] == 'Aledmys':
                split_name[1] = 'Díaz'

            #using names to lookup their player_ids from data sources
            id_search = playerid_lookup(split_name[1], split_name[0])

            #if the player is new or cannot be found give them no ID
            if id_search.empty:
                player_id = 'No ID'
                id_list.append(player_id)
            else:
                player_id = id_search['key_bbref'][0]
                id_list.append(player_id)

        #add columns to dataframe
        lineup['Batter_ID_bbref'] = id_list
        lineup['First_Name'] = first_name_list
        lineup['Last_Name'] = last_name_list

        #get batting stats from fangraphs
        data_b = batting_stats(2022, qual = 0)
        player_ids = data_b['IDfg'].tolist()

        #reverse lookup using fangraphs ID so we can match to lineup dataframe
        players_transform = playerid_reverse_lookup(player_ids, key_type = 'fangraphs')
        players_transform = players_transform[[str('key_fangraphs'), 'key_bbref']]

        #adding hitting data to list of IDS
        get_hitting_data = pd.merge(data_b, players_transform, right_on='key_fangraphs', left_on='IDfg', how = 'inner')

        #matching hitting data to lineup list based on ID
        match_hitting_stats = pd.merge(lineup, get_hitting_data, left_on = 'Batter_ID_bbref', right_on = 'key_bbref', how = 'left')

        #cleanup dataframe for fields that we want
        match_hitting_stats = match_hitting_stats[['Team_x', 'Position', 'Player Name_x', 'Bats', 'Game Number', 'Order', 'Team_y', 'Player Name_y',
                          'Throws', 'Batter_ID_bbref', 'IDfg', 'G', 'AB', 'PA', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 
                          'IBB', 'SO', 'HBP', 'SF', 'SH', 'GDP', 'SB', 'CS', 'OBP', 'SLG', 'OPS', 'ISO', 'BABIP', 'First_Name', 'Last_Name', 'key_bbref']]

        #check for null values - this will be new or unfound players
        null_data = match_hitting_stats.loc[match_hitting_stats['G'].isnull()]

        null_players = null_data['Player Name_x']

        null_dataframe = pd.DataFrame(columns = ['First_Name', 'Last_Name'])    

        list_z = data_b['Name']

        first_list = []
        last_list = []

        for c in list_z:
            break_name = c.split(' ', 1)
            first_name = break_name[0]
            last_name = break_name[1]
            first_list.append(first_name)
            last_list.append(last_name)
            #blah = [first_name, last_name]


        data_b['First'] = first_list
        data_b['Last'] = last_list

        #data_b.head() #prints as expected

        null_data_merge = pd.merge(null_data, data_b, right_on = ['First', 'Last'], 
                      left_on = ['First_Name', 'Last_Name'], how = 'left')


        null_data_merge = null_data_merge[['Team_x', 'Position', 'Player Name_x', 'Bats', 'Game Number', 'Order', 'Team_y', 'Player Name_y',
                          'Throws', 'Batter_ID_bbref', 'IDfg_y', 'G_y', 'AB_y', 'PA_y', 'H_y', '1B_y', '2B_y', '3B_y', 'HR_y', 'R_y', 'RBI_y', 'BB_y', 
                          'IBB_y', 'SO_y', 'HBP_y', 'SF_y', 'SH_y', 'GDP_y', 'SB_y', 'CS_y', 'OBP_y', 'SLG_y', 'OPS_y', 'ISO_y', 'BABIP_y', 'First_Name', 'Last_Name', 'key_bbref']]

        null_data_merge = null_data_merge.rename(columns = {'IDfg_y': 'IDfg', 'G_y': 'G', 'AB_y': 'AB', 'PA_y': 'PA', 'H_y': 'H', '1B_y': '1B', '2B_y': '2B', '3B_y': '3B', 'HR_y': 'HR', 'R_y': 'R', 'RBI_y': 'RBI', 'BB_y': 'BB', 
                          'IBB_y': 'IBB', 'SO_y': 'SO', 'HBP_y': 'HBP', 'SF_y': 'SF', 'SH_y': 'SH', 'GDP_y': 'GDP', 'SB_y': 'SB', 'CS_y': 'CS', 'OBP_y': 'OBP', 'SLG_y': 'SLG', 'OPS_y': 'OPS', 'ISO_y': 'ISO', 'BABIP_y': 'BABIP'})



        match_hitting_stats_remove_null = match_hitting_stats[match_hitting_stats['key_bbref'].notna()]
        match_hitting_stats_remove_null = match_hitting_stats_remove_null.append(null_data_merge)

        final_hitting_data = match_hitting_stats_remove_null
        final_hitting_data = final_hitting_data.sort_values(by = ['Game Number', 'Order'])


        #add 25% hitter for null hitters
        final_hitting_data['G'] = final_hitting_data['G'].fillna(70)
        final_hitting_data['SB'] = final_hitting_data['SB'].fillna(0)
        final_hitting_data['CS'] = final_hitting_data['CS'].fillna(0)
        final_hitting_data['AB'] = final_hitting_data['AB'].fillna(139.5)
        final_hitting_data['PA'] = final_hitting_data['PA'].fillna(150.5)
        final_hitting_data['H'] = final_hitting_data['H'].fillna(32)
        final_hitting_data['1B'] = final_hitting_data['1B'].fillna(20.5)
        final_hitting_data['2B'] = final_hitting_data['2B'].fillna(6)
        final_hitting_data['3B'] = final_hitting_data['3B'].fillna(0)
        final_hitting_data['HR'] = final_hitting_data['HR'].fillna(2)
        final_hitting_data['R'] = final_hitting_data['R'].fillna(17.5)
        final_hitting_data['RBI'] = final_hitting_data['RBI'].fillna(15)
        final_hitting_data['BB'] = final_hitting_data['BB'].fillna(8)
        final_hitting_data['IBB'] = final_hitting_data['IBB'].fillna(0)
        final_hitting_data['SO'] = final_hitting_data['SO'].fillna(36)
        final_hitting_data['HBP'] = final_hitting_data['HBP'].fillna(1)
        final_hitting_data['SF'] = final_hitting_data['SF'].fillna(0.5)
        final_hitting_data['SH'] = final_hitting_data['SH'].fillna(0)
        final_hitting_data['GDP'] = final_hitting_data['GDP'].fillna(2)
        final_hitting_data['OBP'] = final_hitting_data['OBP'].fillna(0.284)
        final_hitting_data['SLG'] = final_hitting_data['SLG'].fillna(0.627)
        final_hitting_data['ISO'] = final_hitting_data['ISO'].fillna(0.108)
        final_hitting_data['BABIP'] = final_hitting_data['BABIP'].fillna(0.271)

        final_hitting_data['RC P/S'] = (final_hitting_data['H']+final_hitting_data['BB']+final_hitting_data['IBB'] + final_hitting_data['HBP'])*(final_hitting_data['1B']+2*final_hitting_data['2B']+3*final_hitting_data['3B']+4*final_hitting_data['HR'])/(final_hitting_data['AB']+final_hitting_data['BB']+final_hitting_data['IBB'] + final_hitting_data['HBP'])/((0.982*final_hitting_data['AB']-final_hitting_data['H']+final_hitting_data['GDP']+final_hitting_data['SF']+final_hitting_data['SH']+final_hitting_data['CS'])/26.83)/9*162

        rS = final_hitting_data['RC P/S']
        rS.replace(to_replace = 0, value = 51.9, inplace = True)

        return final_hitting_data
    
    except:
        print("An exception occured")


# In[8]:


def final_data(lineup):
    try:
        list_pitchers = lineup['Player Name_y']
        handness_hitters = lineup['Bats']
        pitching_hand = lineup['Throws']

        pitcher_id_list = []
        pitcher_first = []
        pitcher_last = []

        for pitcher in list_pitchers:
            split_name = pitcher.split(' ', 1)
            pitcher_first.append(split_name[0])
            pitcher_last.append(split_name[1])
            id_search = playerid_lookup(split_name[1], split_name[0])
            if id_search.shape[0] > 1:
                id_search = id_search.loc[id_search['mlb_played_last'] == 2022, 'key_bbref'].iloc[0]
                pitcher_id_list.append(id_search)
                #print(id_search)
            elif id_search.empty:
                pitcher_id = 'No ID'
                pitcher_id_list.append(pitcher_id)
            else:
                pitcher_id = id_search['key_bbref'][0]
                #print(pitcher_id)
                pitcher_id_list.append(pitcher_id)

        lineup['Pitcher ID'] = pitcher_id_list
        lineup['Pitcher_FirstName'] = pitcher_first
        lineup['Pitcher_LastName'] = pitcher_last

        pitching_splits = pd.DataFrame()

        for p, h, t in zip(pitcher_id_list, handness_hitters, pitching_hand):
            if h == 'R' and p != 'No ID':
                df = get_splits(p, pitching_splits = True, year = 2022)
                pitching_splits = pitching_splits.append(df[0].loc['Platoon Splits', :].iloc[0:1], p)

            elif h == 'L' and p != 'No ID':
                df = get_splits(p, pitching_splits = True, year = 2022)
                pitching_splits = pitching_splits.append(df[0].loc['Platoon Splits', :].iloc[1:2], p)

            elif h == 'S' and p!= 'No ID' and t == 'L':
                df = get_splits(p, pitching_splits = True, year = 2022)
                pitching_splits = pitching_splits.append(df[0].loc['Platoon Splits', :].iloc[0:1], p)

            elif h == 'S' and p!= 'No ID' and t == 'R':
                df = get_splits(p, pitching_splits = True, year = 2022)
                pitching_splits = pitching_splits.append(df[0].loc['Platoon Splits', :].iloc[1:2], p)

            else:
                pitching_splits = pitching_splits.append(pd.Series(), ignore_index = True)

        pitching_splits['Pitcher_ID'] = pitcher_id_list
        pitching_splits['Pitcher_FirstName'] = pitcher_first
        pitching_splits['Pitcher_LastName'] = pitcher_last

        pitching_splits['ERA'] = (pitching_splits['R']*9)/((pitching_splits['PA'] - pitching_splits['H'] - pitching_splits['CS'] - pitching_splits['GDP'])/3)
        pitching_splits['ERA'] = pitching_stats['ERA'].fillna(4.55)


        pitching_splits['Adjusted ERA'] = pitching_splits['ERA']/4.00 
        pitching_splits = pitching_splits[['Pitcher_ID', 'Adjusted ERA', 'Pitcher_FirstName', 'Pitcher_LastName']]

        lineup['Adjusted ERA'] = pitching_splits['Adjusted ERA']
        lineup['RC Adjusted'] = lineup['RC P/S'] * lineup['Adjusted ERA']


        return lineup
    
    except:
        print('lineup used as argument did not satisfy conditions on function')


# In[9]:


def send_groups_to_excel(lineup):
    list_of_teams = lineup['Team_x'].unique()
    path = "/Users/connor/Desktop/Mathletics/Baseball/Python Work/Daily Lineups/"

    TodaysDate = time.strftime("%m-%d-%Y")

    for team in list_of_teams:
        filtered_data = lineup[lineup['Team_x'] == team]
        filtered_data.to_excel(path + team + TodaysDate + ".xlsx")


# In[10]:


def calculate_wins():
    answer = input("Do you want to calculate the expected wins of a lineup? ")
    TodaysDate = time.strftime("%m-%d-%Y")
    path = "/Users/connor/Desktop/Mathletics/Baseball/Python Work/Daily Lineups/"
    
    if answer.lower() == 'yes':
        team = input("What team would you like to look at? (Use team abbreviation) ")
        dataframe = pd.read_excel(path + team + TodaysDate + ".xlsx" )
        
        df = dataframe['RC P/S'].sum()
        print(team + " can create " + "%.2f" % df + " runs with their lineup tonight.")
        win = ((df**2)/(700**2 + df**2))*100
        
        print("With average pitching, the " + team + " should win " + "%.2f" %  win + "% of their games")
        
    else:
        pass


# In[11]:


def send_lineups_to_excel(lineup):
    list_of_teams= lineup['Team'].unique()
    path = "/Users/connor/Desktop/Mathletics/Baseball/Python Work/Daily Lineups/"
    
    for team in list_of_teams:
        lineups = lineup[lineup['Team'] == team]
        lineups.to_excel(path + team + ".xlsx")


# In[12]:


def replace(team):
    path = "/Users/connor/Desktop/Mathletics/Baseball/Python Work/Daily Lineups/"
    
    if team in teams_list:
        dataframe = pd.read_excel(path + team + ".xlsx")
    
        from pybaseball.lahman import people
        people = pd.DataFrame(people())

        people = people[['playerID', 'nameFirst', 'nameLast', 'bats', 'nameGiven']]
        #people_list = people['nameGiven']

        print(dataframe[['Team', 'Position', 'Player Name', 'Bats']])

        replace_player = input("Who do you want to replace in the above lineup? ")
        new_player = input("Who do you want to replace the player with? ")

        new_player_split = new_player.split(' ')
        new_player_last = new_player_split[1]
        new_player_first = new_player_split[0]

        replacing = people[(people['nameFirst'] == new_player_first) & (people['nameLast'] == new_player_last)]
        replacing = replacing[['nameFirst', 'nameLast', 'bats']]
        replacing['Player Name'] = replacing["nameFirst"].str.cat(replacing["nameLast"], sep=" ")
        bats = replacing['bats'].item()

        dataframe.loc[dataframe["Player Name"] == replace_player, ["Player Name", 'Bats']] = (new_player, bats)

        print(dataframe[['Team', 'Position', 'Player Name', 'Bats']])


        return dataframe
    
    else:
        print("Team abbreviation is not in list")
    
    


# In[13]:


def main():
    away_lineups = get_away_lineups()
    away_list = list(away_lineups['Team'].unique())

    
    home_lineups = get_home_lineups()
    home_list = list(home_lineups['Team'].unique())
    
    answer = input("Do you want to replace a player in a lineup?")
    
    if answer.lower() == 'yes':
        
        pick_team = input("What team do you want to replace a player on? ")
        
        if pick_team in away_list:
            away_lineups = replace(pick_team)
            send_lineups_to_excel(away_lineups)
            send_lineups_to_excel(home_lineups)
        elif pick_team in home_list:
            home_lineups = replace(pick_team)
            send_lineups_to_excel(away_lineups)
            send_lineups_to_excel(home_lineups)         
    else:
        send_lineups_to_excel(away_lineups)
        send_lineups_to_excel(home_lineups)

    away_pitcher = get_away_pitchers()
    home_pitcher = get_home_pitchers()

    away_merge = merge(away_lineups, home_pitcher)
    home_merge = merge(home_lineups, away_pitcher)

    away_hitting = hitting_data(away_merge)
    home_hitting = hitting_data(home_merge)

    away_excel = send_groups_to_excel(away_hitting)
    home_excel = send_groups_to_excel(home_hitting)

    calculate_wins()
        
main()
    

