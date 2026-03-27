import argparse

from StartGGClient import StartGGClient


if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='OrderedStandings.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--event', required=True,
                        help='Full slug for the event e.g. tournament/<tournament_name>/event/<event_name>')
    parser.add_argument('--id', action='store_true')
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)

    event_standings = start_client.query_standings_by_slug(args.event)

    if args.id:
        for standing in event_standings:
            print(standing['entrant']['name'] + ' - ' + str(standing['entrant']['participants'][0]['user']['discriminator']) + ' - ' + str(standing['placement']))
    else:
        for standing in event_standings:
            print(standing['entrant']['name'] + ' - ' + str(standing['placement']))