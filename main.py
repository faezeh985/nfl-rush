import  csv
import json

from flask import Flask, request, Response, render_template, session, send_file
import service

app = Flask(__name__)
app.secret_key = 'gu38eUHHi2'

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/players', methods=['GET'])
def get_players():
    session.clear()
    page = request.args.get('page', 1, type=int)
    data, pages= service.get_player_data(page=page)
    return render_template('players.html', players=data, pages=pages)

@app.route('/players/datatable', methods=['GET'])
def get_players_datatable():
    data, pages= service.get_player_data(page=0)
    return render_template('players_dup.html', players=data)

@app.route('/players/condition', methods=['GET'])
def get_players_conditioned():
    sort_by = request.args.get('sortBy','')
    valid_sort = ['Lng','Yds', 'TD','']
    if sort_by not in valid_sort:
        return Response(json.dumps({'error' : 'Not a Valid Sort'}), status=400)
    filter_by = request.args.get('filterBy')
    test = request.args.get('test', False, type=bool)
    page = request.args.get('page', 1, type=int)
    session['sort_by'] = sort_by
    session['filter_by'] = filter_by
    data, pages= service.get_player_data(sort_by=sort_by, filter_by=filter_by, page=page, test=test)
    return {'players' : data, 'pages':pages}

@app.route('/players/download', methods=['GET'])
def download_players():
    sort_by = session.get('sort_by')
    filter_by = session.get('filter_by')
    data, pages = service.get_player_data(sort_by=sort_by, filter_by=filter_by, page=0)
    columns = ['Player',
               'Team',
               'Position',
               'Rushing Attempts Per Game Average',
               'Rushing Attempts',
               'Total Rushing Yards',
               'Rushing Average Yards Per Attempt',
               'Rushing Yards Per Game',
               'Total Rushing Touchdowns',
               'Longest Rush',
               '(Rushing First Down',
               'Rushing First Down Percentage',
               'Rushing 20+ Yards Eac',
               'Rushing 40+ Yards Each',
               'Rushing Fumbles']
    with open('players.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(columns)
        for player in data:
            write.writerow(player.values())
    return send_file('players.csv', mimetype='text/csv', download_name='players.csv', as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)