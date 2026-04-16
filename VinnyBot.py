import argparse
from datetime import timedelta, datetime
from StartGGClient import StartGGClient
from gooey import Gooey
import OutputSetup

def make_post(auth, game):
    today = datetime.now()
    last = today - timedelta(days=7)
    week = today + timedelta(days=7)
    fort = week + timedelta(days=7)
    start_client = StartGGClient(auth)

    return_dict = start_client.query_time_range(game=game, afterDate=int(last.timestamp()), beforeDate=int(fort.timestamp()))
    mystery_tournaments = []
    tournament_info = []
    for i, tournament in enumerate(return_dict):
        if not tournament['events']:
            if tournament['startAt'] >= today.timestamp() and tournament['startAt'] < week.timestamp():
                mystery_tournaments.append(tournament)
                return_dict.pop(i)
        else:
            start_times = [event['startAt'] for event in tournament['events'] 
                           if event['startAt'] >= today.timestamp() and event['startAt'] <= week.timestamp()]
            if len(start_times) != 0:
                tournament_info.append(tournament)
            
    tournament_info = sorted(tournament_info, key=lambda tournament: min([event['startAt'] for event in tournament['events'] 
                                                                          if event['startAt'] >= today.timestamp() and event['startAt'] <= week.timestamp()]))

    print('# ' + game + ' Tournaments Week of <t:' + str(int(today.timestamp())) + ':D> to <t:' + str(int(week.timestamp())) + ':D>')

    for tournament in tournament_info:
        print('**' + tournament['name'] + '**')
        print('<t:' + str(min([event['startAt'] for event in tournament['events']])) + ':F>')
        slug = None
        if tournament['shortSlug']:
            slug = tournament['shortSlug']
        else:
            slug = tournament['slug']
        print('<https://start.gg/' + slug + '>\n')

    for tournament in mystery_tournaments:
        print('**' + tournament['name'] + '**')
        print("Check page for start time.")
        slug = None
        if tournament['shortSlug']:
            slug = tournament['shortSlug']
        else:
            slug = tournament['slug']
        print('<https://start.gg/' + slug + '>\n')
    return

@Gooey()
def main():
    parser = argparse.ArgumentParser(prog='VinnyBot.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--game', choices=list(StartGGClient.game_ids.keys()), required=True,
                        help='Game to look for in query results. ')
    
    args = parser.parse_args()

    make_post(args.token, args.game)
    return

if __name__ == '__main__':
    main()