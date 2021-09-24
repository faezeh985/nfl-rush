import json, math

ROW_PER_PAGE = 20

def get_player_data(sort_by=None, filter_by=None, page=1, test=False):
    file_name = 'rushing.json' if not test else 'tests_data/rushing_test.json'
    with open(file_name) as f:
        players = json.load(f)
    if filter_by:
        players = filter_by_name(players, filter_by)
    if sort_by:
        players = sort_players(players, sort_by)
    if page == 0:
        return players, 1
    return paginate(page, players)

def sort_players(players, sort_key):
    def sort_func(player):
        try:
            key = player[sort_key]
            if isinstance(key, str):
                key = key.strip('T')
                key = key.replace(',','')
                key = float(key)
            return key
        except (KeyError, ValueError):
            return 0
    players.sort(key=sort_func)
    return players

def filter_by_name(players, filter_by):
    def filter_func(player):
        try:
            name = player['Player']
        except KeyError:
            return False
        if name.lower().startswith(filter_by.lower()):
            return True
        full_name = list(name.split())
        for n in full_name:
            if n.lower().startswith(filter_by.lower()):
                return True
        return False
    if not filter_by:
        return players
    return list(filter(filter_func, players))

def paginate(page, players):
    no_player = len(players)
    pages = math.ceil(no_player/ROW_PER_PAGE)
    slice_start = ROW_PER_PAGE * (page - 1)
    slice_end = min((ROW_PER_PAGE * page), no_player)
    return players[slice_start:slice_end], pages











