from datetime import datetime, timezone
import json
from time import sleep
from collections import OrderedDict

import requests


class StartGGClient:

    game_ids = {
    'GGST': 33945,
    'SF6': 43868,
    'GBVSR': 48548,
    'T8': 49783,
    'UNI2': 50203,
    'UNI2CAPS': 50149,
    'KOFXV': 36963,
    'MBTL': 36865,
    'MBAACC': 22407,
    'MK1': 48599,
    'SSBU': 1386,
    'TFH': 1150,
    'SKUGS': 32,
    'XRD': 36,
    'DBFZ': 287,
    '2XKO': 64423,
    'ROA': 24,
    'ROA2': 53945,
    'SSBM': 1,
    'COTW': 73221,
    'TFS': 107706,
    'BBCF': 37
    }

    dropdown_games = game_ids
    del dropdown_games['UNI2CAPS']

    dropdown_games = OrderedDict(sorted(dropdown_games.items()))

    api_url = 'https://api.start.gg/gql/alpha'

    tournament_query = '''
        query TournamentQuery($slug: String, $eventFilter: EventFilter) {
            tournament(slug: $slug) {
                id
                name
                participants(query: {page: 0, perPage: 500}) {
                    nodes {
                        id,
                        player {
                            id,
                            gamerTag
                        }
                    }
                }
                events(filter:$eventFilter) {
                    name
                    id
                    startAt
                    videogame {
                        id
                        slug
                    }
                }
            }
        }'''
    
    tournament_user_id_query = '''
        query TournamentUserIdQuery($slug: String, $eventFilter: EventFilter, $page: Int) {
            tournament(slug: $slug) {
                name
                events(filter: $eventFilter) {
                    name
                    entrants(query: {page: $page}) {
                        nodes {
                            participants {
                                user {
                                    discriminator
                                    player {
                                        gamerTag
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }'''
    
    tournament_by_game_query = '''
        query TournamentsByVideogame($videogameIds: [ID]!, $page: Int!) {
            tournaments(query: {
                perPage: 100
                page: $page
                sortBy: "startAt desc"
                filter: {
                past: true
                videogameIds: $videogameIds
                }
            }){
                nodes {
                    id
                    name
                    city
                    addrState
                    countryCode
                    startAt
                    isOnline
                    numAttendees
                    events(filter: {
                        videogameId: $videogameIds
                    }) {
                        id
                        name
                        numEntrants
                        videogame {
                            id
                            displayName
                        }
                    }
                }
            }
        }
    '''

    tournament_by_game_and_time_query = '''
        query TournamentsByVideogameAndTime($videogameIds: [ID]!, $page: Int!, $filter: TournamentPageFilter) {
            tournaments(query: {
                perPage: 100
                page: $page
                sortBy: "startAt desc"
                filter: $filter
            }){
                nodes {
                    id
                    name
                    city
                    addrState
                    countryCode
                    startAt
                    isOnline
                    numAttendees
                    events(filter: {
                        videogameId: $videogameIds
                    }) {
                        id
                        name
                        numEntrants
                        videogame {
                            id
                            displayName
                        }
                    }
                }
            }
        }
    '''

    event_standings_query = '''
        query EventStandings($eventId: ID!, $page: Int!) {
            event(id: $eventId) {
                id
                sets(page: $page, perPage: 50, sortType: RECENT, 
                    filters: {
                        showByes: false
                        eventIds: [$eventId]
                }){
                    nodes {
                        id,
                        winnerId
                        slots {
                            entrant {
                                name,
                                participants {
                                    player {
                                        id
                                    }
                                }
                                standing {
                                    placement
                                }
                            }
                            seed {
                                seedNum
                            }
                            standing {
                                placement
                            }
                        }
                    }
                }
            }
        }
    '''

    event_set_results_query = '''
        query EventStandings($eventId: ID!, $page: Int!) {
            event(id: $eventId) {
                id
                sets(page: $page, perPage: 100, sortType: RECENT, 
                    filters: {
                        showByes: false
                        eventIds: [$eventId]
                }){
                    nodes {
                        id
                        displayScore
                        slots {
                            entrant {
                                name,
                                participants {
                                    player {
                                        id
                                    }
                                }
                            }
                        }
                    }
                }
            }
        }
    '''
    event_standings_by_slug_query = '''
        query EventStandings($eventSlug: String!, $page: Int!) {
            event(slug: $eventSlug) {
                standings(query: {
                    perPage: 32,
                    page: $page
                }){ 
                    nodes {
                        placement
                        entrant {
                            id
                            name
                            participants {
                                user {
                                    discriminator
                                }
                            }
                        }
                        isFinal
                    }
                }
            }
        }'''
    
    time_query = '''
        query timeRange($query: TournamentQuery!, $filter: EventFilter) {
            tournaments(query: $query) {
                nodes {
                    name
                    shortSlug
                    slug
                    startAt
                    events(filter: $filter) {
                        isOnline
                        name
                        startAt
                    }
                }
            }
        }'''
    
    event_start_time_query = '''
        query startTime($eventSlug: String!) {
            event(slug: $eventSlug) {
                startAt
            }
        }'''

    sets_by_player_query = '''
        query sets($id: ID!, $setFilters: SetFilters, $page: Int!) {
            player(id: $id) {
                sets(page: $page, perPage: 200, filters: $setFilters) {
                    nodes {
                        id
                        displayScore
                        event {
                            name
                            tournament {
                                name
                            }
                            videogame {
                                id
                            }
                        }
                    }
                }
            }
        }'''
    
    sets_by_player_simple_query = '''
        query sets($id: ID!, $setFilters: SetFilters) {
            player(id: $id) {
                sets(page: 0, perPage: 300, filters: $setFilters) {
                    nodes {
                        displayScore
                        event {
                            videogame {
                                id
                            }
                        }
                    }
                }
            }
        }'''
    
    set_by_id_query = '''
        query set_by_id($id: ID!) {
            set(id: $id) {
                id
                displayScore
                event {
                    name
                    tournament {
                        name
                    }
                }
                slots {
                    entrant {
                        name,
                        participants {
                            player {
                                id
                            }
                        }
                    }
                }
            }
        }'''
    
    recent_standings_by_user_query = '''
        query UserQuery($slug: String, $game: ID) {
            user(slug: $slug) {
                player {
                    gamerTag
                    recentStandings(videogameId: $game, limit: 20) {
                        placement
                        container {
                            ... on Event {
                                numEntrants
                                tournament {
                                    name
                                }
                            }
                        }
                    }
                }
            }
        }'''
    
    recent_events_by_user_query = '''
        query UserEvents($slug: String!, $page: Int!) {
            user(slug: $slug) {
                events(query: {
                    perPage: 10
                    page: $page
                    sortBy: "startAt desc"
                }) {
                    nodes {
                        startAt
                        tournament {
                            slug
                        }
                    }
                }
            }
        }'''
    
    tournament_participants_query = '''
        query ParticipantQuery($slug: String, $query: ParticipantPaginationQuery!) {
            tournament(slug: $slug) {
                participants(query: $query, isAdmin: false) {
                    nodes {
                        prefix
                        gamerTag
                    }
                }
            }
        }'''
    
    user_displayscore_time_query = '''
        query DisplayScoreQuery($slug: String, $setFilters: SetFilters, $page: Int) {
            user(slug: $slug) {
                player {
                    sets(page: $page, perPage: 50, filters: $setFilters) {
                        nodes {
                            slots {
                                standing {
                                    placement
                                    entrant {
                                        participants {
                                            player {
                                                gamerTag
                                            }
                                        }
                                    }
                                }
                            }
                            event {
                                videogame {
                                    id
                                }
                            }
                        }
                    }
                }
            }
        }'''
    
    all_seeds_query = '''
        query Seeds($eventSlug: String!, $page: Int!) {
            event(slug: $eventSlug) {
                phases {
                    seeds(query : {page: $page, perPage: 50}) {
                            nodes {
                            groupSeedNum
                            seedNum
                            entrant {
                                name
                            }
                        }
                    }
                }
            }
        }'''
    
    headers = ''

    retries = 2

    def __init__(self, auth):
        self.auth = auth
        self.headers = {'Authorization' : 'Bearer ' + self.auth}

    def make_request(self, params):
        retries = self.retries
        while True:
            r = requests.get(self.api_url, headers=self.headers, params=params)
            return_dict = {}
            try:
                return_dict = json.loads(r.text)
            except json.decoder.JSONDecodeError:
                print('Decode failed, retrying.')

            if not retries or 'data' in return_dict:
                break

            retries -= 1
            sleep(.75)

        return return_dict

    def query_tournament_data(self, game, tournament_url):
        path = tournament_url.rsplit('/')

        slug = path[-1].strip()
        if slug == 'details' or slug == 'events':
            slug = path[-2].strip()

        variables = {
        'slug': slug,
        'eventFilter': {
            'videogameId': [self.game_ids[game]]
            }
        }

        params = {'query' : self.tournament_query,
                'variables' : json.dumps(variables)}

        return_dict = self.make_request(params)

        return return_dict
        
    def query_tournament_start_time(self, game, tournament_url):
        return_dict = self.query_tournament_data(game, tournament_url)
        
        if return_dict['data']['tournament'] is None:
            return None
        
        if len(return_dict['data']['tournament']['events']) == 0:
            return None

        start_time = datetime.fromtimestamp(
            return_dict['data']['tournament']['events'][0]['startAt'], 
            timezone.utc)

        tournament_name = return_dict['data']['tournament']['name']

        return {'start_time':start_time, 'tournament_name':tournament_name}
    
    def query_time_range(self, game, afterDate, beforeDate):
        page = 1
        tournaments = []
        while page < 100:
            variables = {
                'query': 
                    {
                        'page': page,
                        'perPage': 100,
                    'filter': {
                        'afterDate': afterDate,
                        'beforeDate': beforeDate,
                        'videogameIds': [self.game_ids[game]],
                        'hasOnlineEvents': True
                    },
                    'sort': 'startAt'
                    },
                'filter': {
                    "videogameId": self.game_ids[game]
                }
            }

            params = {'query': self.time_query,
                    'variables': json.dumps(variables)}
            
            return_dict = self.make_request(params)
            if len(return_dict['data']['tournaments']['nodes']) == 0:
                break
            tournaments.extend(return_dict['data']['tournaments']['nodes'])

            page += 1

        if game == 'UNI2':
            extra_games = self.query_time_range('UNI2CAPS', afterDate, beforeDate)
            tournaments.extend(extra_games)

        return tournaments
    
    def query_event_start_time(self, slug):
        variables = {
            'eventSlug': slug
        }

        params = {'query': self.event_start_time_query,
                  'variables': json.dumps(variables)}
        
        return_dict = self.make_request(params)
        return return_dict
    
    def query_players(self, game, tournament_url):
        return_dict = self.query_tournament_data(game, tournament_url)
        players = []

        for id in return_dict['data']['tournament']['participants']['nodes']:
            players.append(id['player'])

        return players

    def query_head_to_head(self, game, player_ids):
        test_set_ids = {}

        for player in player_ids:
            page = 1
            while page < 100:
                variables = {
                    'id': player,
                    'page': page
                }

                params = {'query': self.sets_by_player_query,
                        'variables': json.dumps(variables)}
                
                return_dict = self.make_request(params)

                if len(return_dict['data']['player']['sets']['nodes']) == 0:
                    break

                for set in return_dict['data']['player']['sets']['nodes']:
                    if set['id'] not in test_set_ids:
                        test_set_ids[set['id']] = 0
                    else:
                        test_set_ids[set['id']] += 1
                
                page += 1

        print('Retrieved sets.')

        head_to_head_set_ids = []

        for set in test_set_ids:
            if test_set_ids[set] > 0:
                head_to_head_set_ids.append(set)

        print('Found ' + str(len(head_to_head_set_ids)) + ' head to head sets.')

        head_to_head_set_data = []

        for set in head_to_head_set_ids:
            variables = {
                'id': set
            }

            params = {'query': self.set_by_id_query,
                    'variables': json.dumps(variables)}
            
            return_dict = self.make_request(params)
            sleep(.75)
            head_to_head_set_data.append(return_dict['data'])
            
        return head_to_head_set_data
    
    def query_score(self, game, player_id):
        variables = {
                'id': player_id,
                'setFilters': {
                    'hideEmpty': True,
                    'showByes': False,
                    'updatedAfter': 1690917837
                }
            }

        params = {'query': self.sets_by_player_simple_query,
                'variables': json.dumps(variables)}
        
        return_dict = self.make_request(params)

        sets = []

        try:
            sets = return_dict['data']['player']['sets']['nodes']
        except:
            print(return_dict)

        return_sets = []

        for set in sets:
            if set['event']['videogame']['id'] == self.game_ids[game]:
                return_sets.append(set)

        return return_sets

    def query_tournaments_by_game(self, games):
        tournaments = []
        page = 1
        query_ids = [self.game_ids[game] for game in games]
        while page < 500:
            variables = {
                'page': page,
                'videogameIds': query_ids
            }

            params = {'query': self.tournament_by_game_query,
                    'variables': json.dumps(variables)}
            print("Page: " + str(page))
            return_dict = self.make_request(params)         

            try:
                if len(return_dict['data']['tournaments']['nodes']) == 0:
                    break
            except TypeError:
                print("Error on this page, stopping now to write csv.")
                break

            tournaments.extend(return_dict['data']['tournaments']['nodes'])
            
            page += 1
        
        return tournaments
    
    def query_tournaments_by_game_and_time(self, games, start, end):
        tournaments = []
        page = 1
        query_ids = [self.game_ids[game] for game in games]
        while page < 500:
            variables = {
                'page': page,
                'videogameIds': query_ids,
                'filter': {
                    'afterDate': start,
                    'beforeDate': end,
                    'videogameIds': query_ids,
                    'past': True
                },
            }

            params = {'query': self.tournament_by_game_and_time_query,
                    'variables': json.dumps(variables)}
            print("Page: " + str(page))
            return_dict = self.make_request(params)         

            try:
                if len(return_dict['data']['tournaments']['nodes']) == 0:
                    break
            except TypeError:
                print("Error on this page, stopping now to write csv.")
                break

            tournaments.extend(return_dict['data']['tournaments']['nodes'])
            
            page += 1
        
        return tournaments
    
    def query_standings_by_event(self, events):
        event_standings = []
        for event in events:
            print("Event: " + str(event))
            page = 1
            while page < 200:
                variables = {
                    'page': page,
                    'eventId': event
                }
                params = {'query': self.event_standings_query,
                          'variables': json.dumps(variables)}
                print("Page: " + str(page))
                sleep(.75)
                return_dict = self.make_request(params)
                try:
                    if len(return_dict['data']['event']['sets']['nodes']) == 0:
                        break
                except (TypeError,KeyError) as e:
                    print("Given malformed return:")
                    print(return_dict)
                    print("Continuing.")
                    break

                event_standings.append(return_dict['data']['event'])

                page += 1
        return event_standings
    
    def query_set_info(self, events):
        event_standings = []
        for event in events:
            print("Event: " + str(event))
            page = 1
            while page < 200:
                variables = {
                    'page': page,
                    'eventId': event
                }
                params = {'query': self.event_set_results_query,
                          'variables': json.dumps(variables)}
                print("Page: " + str(page))
                sleep(.75)
                return_dict = self.make_request(params)
                try:
                    if len(return_dict['data']['event']['sets']['nodes']) == 0:
                        break
                except (TypeError,KeyError) as e:
                    print("Given malformed return:")
                    print(return_dict)
                    print("Continuing.")
                    break

                event_standings.append(return_dict['data']['event'])

                page += 1

        return event_standings

    def query_recent_standings(self, game, userId):
        variables = {
            'slug': userId,
            'game': self.game_ids[game]
        }

        params = {'query': self.recent_standings_by_user_query,
                'variables': json.dumps(variables)}
        
        return_dict = self.make_request(params)

        results = {}
        try:
            if len(return_dict['data']['user']['player']['recentStandings']) == 0:
                print(return_dict)
                print(userId)
        except:
            print(return_dict)

        try:
            tag = return_dict['data']['user']['player']['gamerTag']
        except:
            print(return_dict)
            print(userId)
        results[tag] = []
        standings = return_dict['data']['user']['player']['recentStandings']

        if standings == None:
            return results

        for standing in standings:
            try:
                results[tag].append((standing['placement'], 
                                     standing['container']['numEntrants'], 
                                     standing['container']['tournament']['name']))
            except:
                print(standing)
                continue

        return results
    
    def query_recent_events(self, userId):
        variables = {
            'slug': userId,
            'page': 1
        }

        params = {'query': self.recent_events_by_user_query,
                'variables': json.dumps(variables)}
        
        return_dict = self.make_request(params)

        return return_dict
        
    def query_tournament_user_id(self, game, slug):
        page = 1
        players = []
        while page < 100:
            variables = {
                'slug': slug,
                'eventFilter': {
                        'videogameId': [self.game_ids[game]]
                    },
                'page': page
            }

            params = {'query': self.tournament_user_id_query,
                    'variables': json.dumps(variables)}
            
            return_dict = self.make_request(params)
            
            
            try:
                if len(return_dict['data']['tournament']['events'][0]['entrants']['nodes']) == 0:
                    break
            except:
                print(return_dict)
                break
            
            for participant in return_dict['data']['tournament']['events'][0]['entrants']['nodes']:
                for p in participant['participants']:
                    player = {}
                    player['gamerTag'] = p['user']['player']['gamerTag']
                    player['id'] = p['user']['discriminator']
                    players.append(player)

            page += 1

        return players
    
    def query_participants(self, slug):
        page = 1
        participants = []
        while page < 100:
            variables = {
                'slug': slug,
                'query': {
                        'page': page,
                        'perPage': 500
                    }
            }

            params = {'query': self.tournament_participants_query,
                    'variables': json.dumps(variables)}
            
            return_dict = self.make_request(params)
            try:
                if len(return_dict['data']['tournament']['participants']['nodes']) == 0:
                    break
            except:
                print(return_dict)
                break

            for participant in return_dict['data']['tournament']['participants']['nodes']:
                participants.append(participant)

            page += 1
        
        return participants
    
    def query_user_scores(self, userId, date):
        page = 1
        sets = []
        while page < 100:
            variables = {
                'slug': userId,
                'setFilters': {
                        'updatedAfter': date
                    },
                'page': page
            }

            params = {'query': self.user_displayscore_time_query,
                    'variables': json.dumps(variables)}
            
            return_dict = self.make_request(params)

            try:
                if len(return_dict['data']['user']['player']['sets']['nodes']) == 0:
                    break
            except:
                print(return_dict)
                break
            
            sets.extend(return_dict['data']['user']['player']['sets']['nodes'])

            page += 1

        return sets
    
    def query_standings_by_slug(self, eventSlug):
        page = 1
        standings = []
        while page < 100:
            variables = {
                'eventSlug': eventSlug,
                'page': page
            }

            params = {'query': self.event_standings_by_slug_query,
                    'variables': json.dumps(variables)}
            
            return_dict = self.make_request(params)

            try:
                if len(return_dict['data']['event']['standings']['nodes']) == 0:
                    break
            except:
                print(return_dict)
                break

            standings.extend(return_dict['data']['event']['standings']['nodes'])

            page += 1

        return standings

    def query_event_seeds(self, eventSlug):
        page = 1
        seeds = []
        while page < 100:
            variables = {
                'eventSlug': eventSlug,
                'page': page
            }

            params = {'query': self.all_seeds_query,
                    'variables': json.dumps(variables)}
            
            return_dict = self.make_request(params)

            try:
                if len(return_dict['data']['event']['phases'][0]['seeds']['nodes']) == 0:
                    break
                if return_dict['data']['event']['phases'][0]['seeds']['nodes'][0]['entrant'] == None:
                    break
            except:
                print(return_dict)
                break

            seeds.extend(return_dict['data']['event']['phases'][0]['seeds']['nodes'])

            page += 1

        return seeds