import argparse
from datetime import date, datetime
from StartGGClient import StartGGClient
from TimezoneFormatter import *
import gspread
import pandas as pd

sheets_creds = "C:\\Users\\conbr\\AppData\\Roaming\\gspread\\service_account.json"

def make_tweet(auth, data_file, region, game):
    today = datetime.now()
    today_format = today.strftime('%A (%m/%d/%y')

    start_client = StartGGClient(auth)

    print(f'{region}:\n\
    \n\
Online {region} {game} tournaments happening today, {today_format}):\n')

    if data_file is not None:
        with open(data_file) as tournament_file:
            tournament_urls = [line.trstrip() for line in tournament_file]
    else:
        gc = gspread.service_account(filename=sheets_creds)

        sh = gc.open("NA/EMEA GGST/SF6 Online Tourney Times")

        worksheet = sh.get_worksheet(0)

        dataframe = pd.DataFrame(worksheet.get_all_records())

        tournament_urls = dataframe['Tournament Permalink']

    for tournament_url in tournament_urls:
        tournament_info = None
        if 'start.gg' in tournament_url:
            tournament_info = start_client.query_tournament_start_time(game, tournament_url)
        elif 'challonge' in tournament_url:
            continue

        if tournament_info == None:
            continue
        
        start_time = tournament_info['start_time']
        
        if not (today < start_time.replace(tzinfo=None) < today + timedelta(hours=24)):
            continue
        
        tournament_name = tournament_info['tournament_name']

        if region == 'NA':
            timezone_spread = get_na_timezone_spread(start_time)
        elif region == 'EMEA':
            timezone_spread = get_emea_timezone_spread(start_time)

        print(f'{tournament_name} {timezone_spread}\n{tournament_url}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='TournamentBot.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--data_file', required=False,
                        help='Path to a file containing a list of tournament URLS, one per line')
    parser.add_argument('--region', choices=['NA', 'EMEA'], required=True,
                        help='Region of tournament for timezone purposes. Either NA or EMEA')
    parser.add_argument('--game', choices=['GGST', 'SF6'], required=True,
                        help='Game to look for in query results. Either GGST or SF6.')

    args = parser.parse_args()
    make_tweet(args.token, args.data_file, args.region, args.game)
