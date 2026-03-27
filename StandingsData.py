import argparse
from datetime import timedelta, datetime, timezone
from StartGGClient import StartGGClient
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='StandingsData.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--input', required=True,
                        help='Path to csv file with "event id" as a header.')
    
    args = parser.parse_args()

    event_ids = []

    with open(args.input, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=',')
        for row in reader:
            event_ids.append(row['event id'])

    start_client = StartGGClient(args.token)

    event_standings = start_client.query_standings_by_event(event_ids)

    with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'event id',
            'set id',
            'loser placement',
            'winner placement',
            'winner id',
            'player 1 id',
            'player 1 name',
            'player 1 seed',
            'player 1 victory',
            'player 2 id',
            'player 2 name',
            'player 2 seed',
            'player 2 victory'])
        for event in event_standings:
            for set in event['sets']['nodes']:
                try:
                    loser_placement = None
                    winner_placement = None
                    winner_id = None
                    if set['slots'][0]['standing']['placement'] == 1:
                        loser_placement = set['slots'][1]['entrant']['standing']['placement']
                        winner_placement = set['slots'][0]['entrant']['standing']['placement']
                        winner_id = set['slots'][0]['entrant']['participants'][0]['player']['id']
                    else:
                        loser_placement = set['slots'][0]['entrant']['standing']['placement']
                        winner_placement = set['slots'][1]['entrant']['standing']['placement']
                        winner_id = set['slots'][1]['entrant']['participants'][0]['player']['id']
                    writer.writerow([
                        event['id'],
                        set['id'],
                        loser_placement,
                        winner_placement,
                        winner_id,
                        set['slots'][0]['entrant']['participants'][0]['player']['id'],
                        set['slots'][0]['entrant']['name'],
                        set['slots'][0]['seed']['seedNum'],
                        set['slots'][0]['standing']['placement'] == 1,
                        set['slots'][1]['entrant']['participants'][0]['player']['id'],
                        set['slots'][1]['entrant']['name'],
                        set['slots'][1]['seed']['seedNum'],
                        set['slots'][1]['standing']['placement'] == 1,
                    ])
                except:
                    continue