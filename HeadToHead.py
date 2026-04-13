import argparse
from StartGGClient import StartGGClient
from gooey import Gooey
import codecs
import sys

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

@Gooey()
def main():
    parser = argparse.ArgumentParser(prog='HeadToHead.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', required=False, choices=list(StartGGClient.dropdown_games.keys()),
                        help='Game to look for in query results.')
    parser.add_argument('--player-ids',  nargs='+', required=False,
                        help='Two Start GG user slugs, separated by a space. You can copy this out of a URL i.e. 7db67915 from https://www.start.gg/user/7db67915')
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)
    
    
    record = start_client.query_head_to_head(args.game, args.player_ids)

    winners = {}
    for set in record:
        for slot in set['set']['slots']:
            if slot['standing']['placement'] == 1:
                for participant in slot['standing']['entrant']['participants']:
                    if participant['player']['gamerTag'] not in winners:
                        winners[participant['player']['gamerTag']] = 1
                    else:
                        winners[participant['player']['gamerTag']] += 1

    for player in winners:
        print('{}: {}'.format(player, str(winners[player])))

    print('\n')

    for set in record:
        print(set['set']['event']['tournament']['name'])
        print(set['set']['event']['name'])
        print(set['set']['displayScore'] + '\n')

    return

if __name__ == '__main__':
    main()