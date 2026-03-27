import argparse
import csv
import math
from time import sleep
from statistics import mean, median

from StartGGClient import StartGGClient

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='DepthScore.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', required=True,
                        help='Game to look for in query results.')
    parser.add_argument('--input', required=True,
                        help='csv with rows of teams and start gg links for players')
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)

    teamscores = {}

    with open(args.input, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            team = row[0]
            teamscores[team] = []
            for i in range(1, 5):
                player = row[i]
                if player == '':
                    continue
                pathSplit = player.split('/')
                id = ''
                if pathSplit[-1] == 'details':
                    id = pathSplit[-2]
                else:
                    id = pathSplit[-1]
                results = start_client.query_recent_standings(args.game, id.strip())
                sleep(.75)
                name = list(results)[0]
                
                scores = []
                for pair in results[name]:
                    depth = math.floor(math.log2(pair[0]))
                    maxdepth = math.floor(math.log2(pair[1]))
                    scores.append(maxdepth - depth)
                
                playerScore = mean(scores)

                print(f'{name},{team},{playerScore}')

                teamscores[team].append(playerScore)

    print(' ')

    for team, scores in teamscores.items():
        print(f'{team}, {sum(scores)}')
    print(' ')
    for team, scores in teamscores.items():
        print(f'{team}, {sum(scores)/len(scores)}')
    print(' ')
    for team, scores in teamscores.items():
        if len(scores) == 3:
            print(f'{team}, {sum(scores)/len(scores)}')
        else:
            scores.remove(min(scores))
            print(f'{team}, {sum(scores)/len(scores)}')
