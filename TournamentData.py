import argparse
from datetime import date, timedelta, datetime, timezone
from StartGGClient import StartGGClient
import csv

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='TournamentData.py')
    parser.add_argument('--token', required=True,
                        help='Start GG API token')
    parser.add_argument('--games', required=True,
                        help='Games to look for in query results.', nargs='+')
    parser.add_argument('--year', required=False,
                        help='If given, returns tournaments only from that year.')
    
    args = parser.parse_args()

    start_client = StartGGClient(args.token)
    if args.year == None:
        tournaments = start_client.query_tournaments_by_game(args.games)
    else:
        start = datetime(int(args.year), 1, 1)
        end = datetime(int(args.year)+1, 1, 1)
        tournaments = start_client.query_tournaments_by_game_and_time(args.games, int(start.timestamp()), int(end.timestamp()))

    with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([
            'event id', 
            'event name', 
            'event entrants', 
            'event game', 
            'tournament_id',
            'tournament name',
            'tournament city',
            'tournament state',
            'tournament country',
            'tournament start timestamp',
            'tournament online',
            'tournament num attendees'])
        for tournament in tournaments:
            for event in tournament['events']:
                start_time = datetime.fromtimestamp(tournament['startAt'], timezone.utc).astimezone(timezone(-timedelta(hours=5)))
                start_time_format = start_time.strftime("%Y-%m-%d %H:%M")
                writer.writerow([
                    event['id'], 
                    event['name'], 
                    event['numEntrants'], 
                    event['videogame']['displayName'],
                    tournament['id'],
                    tournament['name'],
                    tournament['city'],
                    tournament['addrState'],
                    tournament['countryCode'],
                    start_time_format,
                    tournament['isOnline'],
                    tournament['numAttendees']])