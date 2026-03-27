import argparse
import math
from statistics import mean
from StartGGClient import StartGGClient
from time import sleep
import csv
from gooey import Gooey

@Gooey
def main():
    parser = argparse.ArgumentParser(prog='AutoSeeder.py',
                                     description=(
                            'Program for automatically seeding a tournament based on recent player performance.\n'
                            'The first number is their score, the depth they\'ve made it in their last 20 tournaments.\n'
                            'The second is a number 0-20, representing how many entries they have for this game. Less entries means a less confident score.'))
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', required=True, choices=list(StartGGClient.dropdown_games.keys()),
                        help='Game to look for in query results.')
    parser.add_argument('--slug', required=True,
                        help='Tournament name copied from url e.g. aegis-esports-x-zenmarket-25-na-server-2xko-tournament')

    args = parser.parse_args()

    start_client = StartGGClient(args.token)
    record = start_client.query_tournament_user_id(args.game, args.slug)

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

    seeding = sorted(seeding, key=lambda player: player[1], reverse=True)
    for player in seeding:
        print(f'{player[0]}, {player[1]}, {player[2]}')
    return

if __name__ == '__main__':
    main()