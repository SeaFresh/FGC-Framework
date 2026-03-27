import argparse
from StartGGClient import StartGGClient


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='HeadToHead.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--slug', required=False,
                        help='Slug of tournament path')
    parser.add_argument('--game', required=True, choices=list(StartGGClient.dropdown_games.keys()),
                        help='Game to look for in query results.')
    parser.add_argument('--player-ids',  nargs='+', required=False)
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)

    if args.slug and args.player_ids:
        print("Requires either a slug to get the player ids for a tournament or the player ids to get the set info, not both.")
    elif args.slug:
        record = start_client.query_players(args.game, args.slug)
        for player in record:
            print(player['gamerTag'] +': ' + str(player['id']) + '\n')
    elif args.player_ids:
        record = start_client.query_head_to_head(args.game, args.player_ids)
        for set in record:
            print(set['set']['event']['tournament']['name'])
            print(set['set']['event']['name'])
            print(set['set']['displayScore'] + '\n')
    else:
        print("Requires either a slug to get the player ids for a tournament or the player ids to get the set info.")