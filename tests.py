import unittest, math
from flask import json
from main import app
from service import ROW_PER_PAGE

TEST_LENGTH = 326

class BaseClass(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()

    def test_sort_by(self):
        response = self.app.get('/players/condition', query_string={'sortBy': 'Lng', 'test':True})
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert isinstance(data['players'], list)
        assert len(data['players']) == ROW_PER_PAGE
        pages = math.ceil(TEST_LENGTH/ROW_PER_PAGE)
        assert pages == data['pages']
        prev = data['players'][0]
        for p in data['players']:
            key = p['Lng']
            key_prev = prev['Lng']
            if isinstance(key_prev, str):
                key = key_prev.strip('T')
                key = key_prev.replace(',', '')
                key_prev = float(key_prev)
            if isinstance(key, str):
                key = key.strip('T')
                key = key.replace(',', '')
                key = float(key)
            assert key >= key_prev
            prev = p
    def test_filter_by(self):
        no_joe = 3
        filter_by = 'joe'
        response = self.app.get('/players/condition', query_string={'filterBy': filter_by, 'test' : True})
        data = json.loads(response.get_data(as_text=True))
        assert response.status_code == 200
        assert isinstance(data['players'], list)
        assert len(data['players']) == no_joe
        for p in data['players']:
            checked = False
            name = p['Player']
            if name.lower().startswith(filter_by):
                checked = True
            full_name = list(name.split())
            for n in full_name:
                if n.lower().startswith(filter_by):
                    checked = True
            assert checked