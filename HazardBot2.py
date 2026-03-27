import argparse
from datetime import date, datetime
from StartGGClient import StartGGClient
from TimezoneFormatter import *

sheets_creds = "C:\\Users\\conbr\\AppData\\Roaming\\gspread\\service_account.json"

def make_tweet(auth, game):
    today = datetime.now()
    today_format = today.strftime('%A (%m/%d/%y')

    start_client = StartGGClient(auth)

    tomorrow = today + timedelta(days=1)
    week = tomorrow + timedelta(days=8)
    last = today - timedelta(days=7)
    start_client = StartGGClient(auth)

    return_dict= start_client.query_time_range(game=game, afterDate=int(last.timestamp()), beforeDate=int(week.timestamp()))
 
    mystery_tournaments = []
    tournament_info = []
    for i, tournament in enumerate(return_dict):
        if not tournament['events']:
            if tournament['startAt'] >= today.timestamp() and tournament['startAt'] < tomorrow.timestamp():
                mystery_tournaments.append(tournament)
                return_dict.pop(i)
        else:
            start_times = [event['startAt'] for event in tournament['events'] 
                           if event['startAt'] >= today.timestamp() and event['startAt'] <= tomorrow.timestamp()]
            if len(start_times) != 0:
                tournament_info.append(tournament)

    tournament_info = sorted(tournament_info, key=lambda tournament: min([event['startAt'] for event in tournament['events']
                                                                          if event['startAt'] >= today.timestamp() and event['startAt'] <= tomorrow.timestamp()]))

    print(f'Online {game} tournaments happening today, {today_format}):\n')

    for tournament in tournament_info:
        
        tournament_name = tournament['name']

        start_time = datetime.fromtimestamp(
            min([event['startAt'] for event in tournament['events']]), 
            timezone.utc)

        timezone_spread = get_na_timezone_spread(start_time)

        if tournament['shortSlug']:
            slug = tournament['shortSlug']
        else:
            slug = tournament['slug']
        tournament_url = 'https://start.gg/' + slug + '\n'

        print(f'{tournament_name} {timezone_spread}\n{tournament_url}')

    for tournament in mystery_tournaments:
        tournament_name = tournament['name']

        if tournament['shortSlug']:
            slug = tournament['shortSlug']
        else:
            slug = tournament['slug']
        tournament_url = 'https://start.gg/' + slug + '\n'

        print(f'{tournament_name} "Check page for start time."\n{tournament_url}')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='HazardBot2.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', required=True,
                        help='Game to look for in query results.')

    args = parser.parse_args()
    make_tweet(args.token, args.game)
