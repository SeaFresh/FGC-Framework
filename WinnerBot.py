import argparse
from datetime import datetime, timedelta
from gooey import Gooey
from StartGGClient import StartGGClient
import OutputSetup

@Gooey()
def main():
    parser = argparse.ArgumentParser(prog='WinnerBot.py',
                                     description='Checks to see how many sets you\'ve won and who you\'re winning against.')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', choices=list(StartGGClient.dropdown_games.keys()), required=True,
                        help='Game to look for in query results. ')
    parser.add_argument('--user', required=True,
                        help='Start GG user slug. You can copy this out of a URL i.e. 7db67915 from https://www.start.gg/user/7db67915')
    parser.add_argument('--months', required=True,
                        help='Number of months to search back.')
    
    args = parser.parse_args()

    today = datetime.now()
    start_bound = today - timedelta(days=int(args.months)*30.4375)

    start_client = StartGGClient(args.token)
    sets = start_client.query_user_scores(args.user, int(start_bound.timestamp()))
    losers = {}
    for set in sets:
        if set['event']['videogame']['id'] != start_client.game_ids[args.game]:
            continue
        try:
             for slot in set['slots']:
                  if slot['standing']['placement'] == 2:
                       for participant in slot['standing']['entrant']['participants']:
                            if participant['player']['gamerTag'] not in losers:
                                losers[participant['player']['gamerTag']] = 1
                            else:
                                 losers[participant['player']['gamerTag']] += 1
        except:
                continue
    
    losers = sorted(losers.items(), key=lambda item: item[1], reverse=True)
    for entry in losers:
        print(entry[0] + ' beaten ' + str(entry[1]) + ' time(s)')

    return



if __name__ == '__main__':
    main()