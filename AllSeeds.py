import argparse
import math
from gooey import Gooey

from StartGGClient import StartGGClient

@Gooey(encoding='UTF-8')
def main():
    parser = argparse.ArgumentParser(prog='AllSeeds.py',
                                     description='Retrieves all seeds for an event in order.')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--event', required=True,
                        help='Full slug for the event copied from a url e.g. tournament/<tournament_name>/event/<event_name>')
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)

    event_seeds = start_client.query_event_seeds(args.event)
    event_seeds = sorted(event_seeds, key = lambda seed: seed['seedNum'])
    width = (math.log10(len(event_seeds))) + 1
    for seed in event_seeds:
        print("{: <{width}} {:}".format(seed['seedNum'], seed['entrant']['name'], width=math.floor(width)))

    return

if __name__ == '__main__':
    main()

