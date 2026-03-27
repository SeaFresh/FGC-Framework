import argparse
from datetime import timedelta, datetime, timezone
from StartGGClient import StartGGClient
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='SetData.py')
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

    event_standings = start_client.query_set_info(event_ids)

    with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'set id',
            'player 1 id',
            'player 1 wins',
            'player 2 id',
            'player 2 wins'
        ])
        for event in event_standings:
            for set in event['sets']['nodes']:
                display_score = set['displayScore']
                try:
                    split = display_score.find(' - ')

                    first = display_score[0:split]
                    last = display_score[split:]
                    first_wins = first.rstrip()[-1]
                    last_wins = last.rstrip()[-1]

                    if first_wins == 'W' or first_wins =='L':
                        first_wins = None
                        last_wins = None
                    else:
                        first_wins = int(first_wins)
                        last_wins = int(last_wins)

                    writer.writerow([
                        set['id'],
                        set['slots'][0]['entrant']['participants'][0]['player']['id'],
                        first_wins,
                        set['slots'][1]['entrant']['participants'][0]['player']['id'],
                        last_wins
                    ])
                except:
                    continue