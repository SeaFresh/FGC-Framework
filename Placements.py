import argparse
from StartGGClient import StartGGClient
from gooey import Gooey
import OutputSetup

@Gooey()
def main():
    parser = argparse.ArgumentParser(prog='Placements.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', required=False, choices=list(StartGGClient.dropdown_games.keys()),
                        help='Game to look for in query results.')
    parser.add_argument('--user', required=True,
                            help='Start GG user slug. You can copy this out of a URL i.e. 7db67915 from https://www.start.gg/user/7db67915')

    args = parser.parse_args()
    start_client = StartGGClient(args.token)
    placements = start_client.query_user_placements(args.user, args.game)
    for placement in placements:
        print(str(placement['placement']) + '/' + str(placement['entrants']) + ' at ' + placement['slug'])

if __name__ == '__main__':
    main()