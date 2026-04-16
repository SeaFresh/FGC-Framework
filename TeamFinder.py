import argparse
from StartGGClient import StartGGClient
from gooey import Gooey
import OutputSetup

@Gooey()
def main():
    parser = argparse.ArgumentParser(prog='TeamFinder.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--slug', required=True,
                        help='Tournament slug')
    parser.add_argument('--tag', required=True,
                        help='Team tag to look for.')
    
    args = parser.parse_args()
    start_client = StartGGClient(args.token)
    participants = start_client.query_participants(args.slug)

    for participant in participants:
        if participant['prefix'] is not None and args.tag == participant['prefix']:
            print(f"{participant['prefix']} {participant['gamerTag']}")

    return


if __name__ == '__main__':
    main()