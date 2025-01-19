import requests 
import json
import gspread
import time
import datetime
import pytz
import os 
 
start_time = time.time()

creds_json = os.environ['CREDS']
CREDS = json.loads(creds_json)

client = gspread.service_account_from_dict(CREDS)

# Open the spreadsheet
spreadsheet = client.open("Discord ESPN Stats Bot")

# Get the Players sheet
players_sheet = spreadsheet.worksheet("Master")

base_url = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/teams/"

current_players = []

for i in range(30):
    
    i += 1
    url = f"{base_url}{i}/roster"
    api_call = requests.get(url)
    api_json = api_call.json()
    
    team = api_json['team']['displayName']
    # print(f"Team: {team}")
    players = api_json['athletes']
    
    for position in players:
        #print(f"Curent Position: {position['position']}")
        for player in position['items']:
            player_name = player['displayName']
            player_position = player['position']['abbreviation']
            player_id = player['id']

            # print(player_name)
            # print(player_id)
            # print(player_position)
            
            current_players.append({
                'Player_Name': player_name,
                'Player_ID': player_id,
                'Player_Team': team,
                'Player_Position': player_position,
                'Batting Average': "",
                'Home Runs': "",
                'BA w RISP': "",
                'HR v LEFT': "",
                'HR v RIGHT': "",
                'BA v LEFT': "",
                'BA v RIGHT': "",
                'OPS': "",
                'RBIS': "",
                'L15 BA': "",
                'L15 HR': "",
                'L15 OPS': "",
                'L15 RBI': "",
                
                'IP': "",
                'Hits Allowed': "",
                'Ks': "",
                'OPP BA w RISP': "",
                'ERA': "",
                'Walks': "",
                'H/9': "",
                'BB/9': "",
                'K/9': "",
                'L15 IP': "",
                'L15 Hits Alowed': "",
                'L15 Ks': "",
                'L15 ERA': "",
                'L15 Walks': ""
            })

print('Finished looping through all teams')

# Hitter: Aaron Judge
# Pitcher: Chris Sale            
# Test Hitter Stats: https://site.web.api.espn.com/apis/common/v3/sports/baseball/mlb/athletes/33192/stats?region=us&lang=en&contentorigin=espn&category=batting
# Test Pitcher Stats: https://site.web.api.espn.com/apis/common/v3/sports/baseball/mlb/athletes/30948/stats?region=us&lang=en&contentorigin=espn&category=pitching
# Test Pitcher Splits: https://site.web.api.espn.com/apis/common/v3/sports/baseball/mlb/athletes/30948/splits?region=us&lang=en&contentorigin=espn&season=2024&category=pitching
# Test Hitter Splits: https://site.web.api.espn.com/apis/common/v3/sports/baseball/mlb/athletes/33192/splits?region=us&lang=en&contentorigin=espn&season=2024&category=batting


stats_url = 'https://site.web.api.espn.com/apis/common/v3/sports/baseball/mlb/athletes/'
# pitcher_stats_url_suffix = '/stats?region=us&lang=en&contentorigin=espn&category=pitching'
# hitter_stats_url_suffix = '/stats?region=us&lang=en&contentorigin=espn&category=batting'

current_year = time.strftime("%Y")
pitcher_splits_url_suffix = f'/splits?region=us&lang=en&contentorigin=espn&season={current_year}&category=pitching'
hitter_splits_url_suffix = f'/splits?region=us&lang=en&contentorigin=espn&season={current_year}&category=batting'

print("Getting Stats")
    
for player in current_players:
    try:
        if player['Player_Position'] in ["CP", "SP", "RP"]:
            full_splits_url = f"{stats_url}{player['Player_ID']}{pitcher_splits_url_suffix}"
            try:
                splits_api = requests.get(full_splits_url)
                api_json = splits_api.json()
                if 'splits' in api_json['splitCategories'][0]:
                    try:
                        player['IP'] = api_json['splitCategories'][0]['splits'][0]['stats'][8]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting IP")
                    try:
                        player['Hits Allowed'] = api_json['splitCategories'][0]['splits'][0]['stats'][9]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting Hits Allowed")
                    try:
                        player['Ks'] = api_json['splitCategories'][0]['splits'][0]['stats'][14]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting Ks")
                    try:
                        player['OPP BA w RISP'] = api_json['splitCategories'][10]['splits'][2]['stats'][12]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting OPP BA w RISP")
                    try:
                        player['ERA'] = api_json['splitCategories'][0]['splits'][0]['stats'][0]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting ERA")
                    try:
                        player['Walks'] = api_json['splitCategories'][0]['splits'][0]['stats'][13]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting Walks")
                    try:
                        player['L15 IP'] = api_json['splitCategories'][4]['splits'][-2]['stats'][8]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 IP")
                    try:
                        player['L15 Hits Alowed'] = api_json['splitCategories'][4]['splits'][-2]['stats'][9]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 Hits Alowed")
                    try:
                        player['L15 Ks'] = api_json['splitCategories'][4]['splits'][-2]['stats'][14]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 Ks")
                    try:
                        player['L15 ERA'] = api_json['splitCategories'][4]['splits'][-2]['stats'][0]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 ERA")
                    try:
                        player['L15 Walks'] = api_json['splitCategories'][4]['splits'][-2]['stats'][13]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 Walks")
            except requests.RequestException as e:
                print("Error Getting Splits")
                print(f"RequestException: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting splits")
            
            if player['IP'] != "" or player['IP'] != "0":
                player['H/9'] = round(float(player['Hits Allowed']) / float(player['IP']) * 9, 2)
                player['BB/9'] = round(float(player['Walks']) / float(player['IP']) * 9, 2)
                player['K/9'] = round(float(player['Ks']) / float(player['IP']) * 9, 2)
        else:
            full_splits_url = f"{stats_url}{player['Player_ID']}{hitter_splits_url_suffix}"
            try:
                splits_api = requests.get(full_splits_url)
                api_json = splits_api.json()
                if 'splits' in api_json['splitCategories'][0]:
                    try:
                        player['L15 BA'] = api_json['splitCategories'][2]['splits'][-2]['stats'][12]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 Batting Average")
                    try:
                        player['L15 HR'] = api_json['splitCategories'][2]['splits'][-2]['stats'][5]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 Homeruns")
                    try:
                        player['L15 OPS'] = api_json['splitCategories'][2]['splits'][-2]['stats'][15]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 OPS")
                    try:
                        player['L15 RBI'] = api_json['splitCategories'][2]['splits'][-2]['stats'][6]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting L15 RBI")
                    try:
                        player['Batting Average'] = api_json['splitCategories'][0]['splits'][0]['stats'][12]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting Batting Average")
                    try:
                        player['Home Runs'] = api_json['splitCategories'][0]['splits'][0]['stats'][5]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting Home Runs")
                    try:
                        player['BA w RISP'] = api_json['splitCategories'][8]['splits'][2]['stats'][12]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting BA w RISP")
                    try:
                        player['HR v LEFT'] = api_json['splitCategories'][1]['splits'][0]['stats'][5]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting HR v LEFT")
                    try:
                        player['HR v RIGHT'] = api_json['splitCategories'][1]['splits'][1]['stats'][5]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting HR v RIGHT")
                    try:
                        player['BA v LEFT'] = api_json['splitCategories'][1]['splits'][0]['stats'][12]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting BA v LEFT")
                    try:
                        player['BA v RIGHT'] = api_json['splitCategories'][1]['splits'][1]['stats'][12]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting BA v RIGHT")
                    try:
                        player['OPS'] = api_json['splitCategories'][0]['splits'][0]['stats'][15]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting OPS")
                    try:
                        player['RBIS'] = api_json['splitCategories'][0]['splits'][0]['stats'][6]
                    except (KeyError, IndexError) as e:
                        print(f"KeyError or IndexError: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting RBIS")
            except requests.RequestException as e:
                print("Error Getting Splits")
                print(f"RequestException: {e} for player {player['Player_Name']} with ID {player['Player_ID']} when getting splits")
    except Exception as e:
        print("Overall Error")
        print(f"Error processing player {player['Player_Name']} with ID {player['Player_ID']}: {e}")

# Prepare the data to update (excluding the headers in the list)
data_to_update = []

# Get the headers from the first player dictionary
headers = list(current_players[0].keys())

# Append the player data directly
for player in current_players:
    row = [player[key] for key in headers]
    data_to_update.append(row)

# Calculate the end column letter
def get_column_letter(col_num):
    string = ""
    while col_num > 0:
        col_num, remainder = divmod(col_num - 1, 26)
        string = chr(65 + remainder) + string
    return string

end_column = get_column_letter(len(headers) + 1)

# Update the sheet, starting from cell B2
cell_range = f'B2:{end_column}{len(data_to_update) + 1}'
players_sheet.update(cell_range, data_to_update)
