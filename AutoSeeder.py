import argparse
import math
from statistics import mean
from StartGGClient import StartGGClient
from time import sleep
import csv
from gooey import Gooey

def main():
    parser = argparse.ArgumentParser(prog='AutoSeeder.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', required=True, choices=list(StartGGClient.game_ids.keys()),
                        help='Game to look for in query results.')
    parser.add_argument('--slug', required=False,
                        help='')
    parser.add_argument('--input', required=False)
    parser.add_argument('--players', required=False, nargs=2)

    args = parser.parse_args()

    start_client = StartGGClient(args.token)
    if args.slug:
        record = start_client.query_tournament_user_id(args.game, args.slug)
    elif args.input:
        record = []
        with open(args.input) as f:
            reader = csv.DictReader(f)
            for row in reader:
                player = {}
                player['gamerTag'] = row['Player']
                player['id'] = row['Start GG'].rsplit('/')[-1]
                record.append(player)
    elif args.players:
        record = []
        record.append({'gamerTag': list(start_client.query_recent_standings(args.game, args.players[0]))[0],
                       'id': args.players[0]})
        record.append({'gamerTag': list(start_client.query_recent_standings(args.game, args.players[1]))[0],
                       'id': args.players[1]})
    else:
        print('Requires slug, input, or players')

    print(record)

    seeding = []

    for player in record:
        tag = player['gamerTag']
        id = str(player['id'])
        if id.strip() == '':
            continue
        results = start_client.query_recent_standings(args.game, id.strip())
        sleep(.75)
        name = list(results)[0]
        
        scores = []
        playerScore = 0.0

        if len(results[name]) > 0:
            for pair in results[name]:
                depth = math.floor(math.log2(pair[0]))
                maxdepth = math.floor(math.log2(pair[1]))
                scores.append(maxdepth - depth)
            
            playerScore = sum(scores)

        seeding.append((name, playerScore, len(scores)))

        
    if not args.input:
        seeding = sorted(seeding, key=lambda player: player[1], reverse=True)
    for player in seeding:
        print(f'{player[0]}, {player[1]}, {player[2]}')

if __name__ == '__main__':
    main()