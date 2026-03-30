import argparse
from datetime import datetime, timedelta
from gooey import Gooey
import locale

from StartGGClient import StartGGClient

@Gooey(encoding=locale.getpreferredencoding())
def main():
    parser = argparse.ArgumentParser(prog='LoserBot.py',
                                     description='Checks to see how many sets you\'ve won and who you\'re losing to.')
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
    winners = {}
    for set in sets:
        if set['event']['videogame']['id'] != start_client.game_ids[args.game]:
            continue
        try:
             for slot in set['slots']:
                  if slot['standing']['placement'] == 1:
                       for participant in slot['standing']['entrant']['participants']:
                            if participant['player']['gamerTag'] not in winners:
                                winners[participant['player']['gamerTag']] = 1
                            else:
                                 winners[participant['player']['gamerTag']] += 1
        except:
                continue
    
    winners = sorted(winners.items(), key=lambda item: item[1], reverse=True)
    for entry in winners:
        print(entry[0] + ' ' + str(entry[1]))

    return



if __name__ == '__main__':
    main()