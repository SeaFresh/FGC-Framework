import argparse

from StartGGClient import StartGGClient
from time import sleep
from datetime import datetime, timedelta
from gooey import Gooey
import codecs
import sys

if sys.stdout.encoding != 'UTF-8':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
if sys.stderr.encoding != 'UTF-8':
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

@Gooey()
def main():
    parser = argparse.ArgumentParser(prog='DoubleBracket.py',
                                     description='Attempts to find double bracketers by seeing if they\'ve entered anything an hour before or after your bracket.')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--event', required=True,
                        help='Full slug for the event e.g. tournament/<tournament_name>/event/<event_name>')
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)

    start_time = datetime.fromtimestamp(start_client.query_event_start_time(args.event)['data']['event']['startAt'])

    users = start_client.query_standings_by_slug(args.event)

    for standing in users:
        for participant in standing['entrant']['participants']:
            events = start_client.query_recent_events(participant['user']['discriminator'])['data']['user']['events']['nodes']
            for event in events:
                pair_start = datetime.fromtimestamp(event['startAt'])
                difference = abs(start_time - pair_start)
                if difference <= timedelta(hours=1):
                    if event['tournament']['slug'] != '/'.join(args.event.split('/')[0:-2]):
                        print('Entrant {} may be double bracketing in <https://start.gg/{}>'.format(
                            standing['entrant']['name'], event['tournament']['slug']))
    return


if __name__ == '__main__':
    main()