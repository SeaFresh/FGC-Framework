import argparse
from time import sleep
import csv

from StartGGClient import StartGGClient



if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='PlisnoBot.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', required=True,
                        help='Game to look for in query results.')
    parser.add_argument('--slug', required=True)
    parser.add_argument('--entrants', required=False, type=int, default=1)
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)
    record = start_client.query_tournament_user_id(args.game, args.slug)

    events = {}
    players = {}
    for player in record:
        tag = player['gamerTag']
        id = str(player['id'])
        if id.strip() == '':
            continue
        results = start_client.query_recent_standings(args.game, id.strip())
        sleep(.75)
        players[tag] = {}
        for event in results[tag]:
            if not event[2] in events:
                events[event[2]] = {'size': event[1], 'entrants': 0}
            players[tag][event[2]] = event[0]
            events[event[2]]['entrants'] += 1
    
    to_remove = []
    for event in events:
        if events[event]['entrants'] <= args.entrants:
            to_remove.append(event)
    
    for event in to_remove:
        del events[event]
        for player in players:
            if event in player:
                del player[event]
    
    with open('placements.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerow(['Player'] + [event + ': ' + str(events[event]['size']) for event in events])
        for player in players:
            row = [player]
            for event in events:
                if event in players[player]:
                    row.append(players[player][event])
                else:
                    row.append(0)
            writer.writerow(row)