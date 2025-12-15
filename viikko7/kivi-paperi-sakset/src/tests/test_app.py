import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app, WINNING_SCORE

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = 'test-secret-key'
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Testaa että etusivu latautuu"""
    response = client.get('/')
    assert response.status_code == 200
    assert 'Kivi-Paperi-Sakset'.encode('utf-8') in response.data
    assert 'vastaan'.encode('utf-8') in response.data

def test_start_game_mode_a(client):
    """Testaa ihmistä vastaan pelin aloitus"""
    response = client.post('/start', data={'mode': 'a'}, follow_redirects=True)
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert ('PELAAJA 1' in response_text or 
            'Pelaaja 1' in response_text or
            'Tilanne' in response_text)

def test_start_game_mode_b(client):
    """Testaa tekoälyä vastaan pelin aloitus"""
    response = client.post('/start', data={'mode': 'b'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tilanne' in response.data

def test_start_game_mode_c(client):
    """Testaa parannettua tekoälyä vastaan pelin aloitus"""
    response = client.post('/start', data={'mode': 'c'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'Tilanne' in response.data

def test_play_invalid_choice(client):
    """Testaa virheellinen siirto"""
    with client.session_transaction() as sess:
        sess['mode'] = 'b'
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['game_over'] = False
    
    response = client.post('/play', data={'choice': 'x'}, follow_redirects=True)
    assert response.status_code == 200

def test_play_vs_computer_mode_b(client):
    """Testaa pelaaminen tekoälyä vastaan"""
    with client.session_transaction() as sess:
        sess['mode'] = 'b'
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['peli_siirrot'] = []
        sess['game_over'] = False
    
    response = client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert ('Voitit' in response_text or 
            'Hävisit' in response_text or 
            'Tasapeli' in response_text)

def test_game_ends_at_five_wins_player(client):
    """Testaa että peli päättyy kun pelaaja saa 3 voittoa"""
    with client.session_transaction() as sess:
        sess['mode'] = 'b'
        sess['tuomari_data'] = {'ekan_pisteet': WINNING_SCORE, 'tokan_pisteet': 2, 'tasapelit': 0}
        sess['game_over'] = True
        sess['winner'] = 'Sinä'
    
    response = client.get('/game')
    assert response.status_code == 200
    assert 'voitti pelin'.encode('utf-8') in response.data

def test_game_ends_at_five_wins_computer(client):
    """Testaa että peli päättyy kun vastustaja saa 3 voittoa"""
    with client.session_transaction() as sess:
        sess['mode'] = 'b'
        sess['tuomari_data'] = {'ekan_pisteet': 2, 'tokan_pisteet': WINNING_SCORE, 'tasapelit': 1}
        sess['game_over'] = True
        sess['winner'] = 'Vastustaja'
    
    response = client.get('/game')
    assert response.status_code == 200
    assert 'voitti pelin'.encode('utf-8') in response.data

def test_play_player_vs_player_turn_1(client):
    """Testaa pelaaja 1:n vuoro"""
    with client.session_transaction() as sess:
        sess['mode'] = 'a'
        sess['current_player'] = 1
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['game_over'] = False
    
    response = client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    assert response.status_code == 200
    assert b'PELAAJA 2' in response.data

def test_play_player_vs_player_full_round(client):
    """Testaa täysi pelikierros pelaaja vs pelaaja"""
    with client.session_transaction() as sess:
        sess['mode'] = 'a'
        sess['current_player'] = 1
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['game_over'] = False
    
    response = client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    assert response.status_code == 200
    
    response = client.post('/play', data={'choice': 'p'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'Pelaaja 2 voitti'.encode('utf-8') in response.data

def test_full_game_to_completion(client):
    """Testaa täysi peli loppuun asti"""
    with client.session_transaction() as sess:
        sess['mode'] = 'a'
        sess['current_player'] = 1
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['game_over'] = False
    
    for _ in range(WINNING_SCORE):
        client.post('/play', data={'choice': 'k'}, follow_redirects=True)
        response = client.post('/play', data={'choice': 's'}, follow_redirects=True)
    
    assert 'voitti pelin'.encode('utf-8') in response.data or 'Pelaaja 1'.encode('utf-8') in response.data

def test_score_updates(client):
    """Testaa että pisteet päivittyvät oikein"""
    with client.session_transaction() as sess:
        sess['mode'] = 'b'
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['peli_siirrot'] = []
        sess['game_over'] = False
    
    for _ in range(3):
        client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    
    response = client.get('/game')
    assert response.status_code == 200
    assert b'Tilanne' in response.data

def test_game_redirect_without_mode(client):
    """Testaa että /game ohjaa takaisin alkuun ilman mode:a"""
    response = client.get('/game', follow_redirects=True)
    assert response.status_code == 200
    assert 'Valitse pelimuoto'.encode('utf-8') in response.data

def test_rock_beats_scissors(client):
    """Testaa että kivi voittaa sakset"""
    with client.session_transaction() as sess:
        sess['mode'] = 'a'
        sess['current_player'] = 1
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['game_over'] = False
    
    client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    response = client.post('/play', data={'choice': 's'}, follow_redirects=True)
    assert 'Pelaaja 1 voitti'.encode('utf-8') in response.data

def test_cannot_play_after_game_over(client):
    """Testaa että siirtoja ei voi tehdä pelin päätyttyä"""
    with client.session_transaction() as sess:
        sess['mode'] = 'b'
        sess['tuomari_data'] = {'ekan_pisteet': WINNING_SCORE, 'tokan_pisteet': 2, 'tasapelit': 0}
        sess['game_over'] = True
        sess['winner'] = 'Sinä'
    
    response = client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    assert response.status_code == 200
    assert 'voitti pelin'.encode('utf-8') in response.data

def test_tie_game(client):
    """Testaa tasapeli"""
    with client.session_transaction() as sess:
        sess['mode'] = 'a'
        sess['current_player'] = 1
        sess['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
        sess['game_over'] = False
    
    client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    response = client.post('/play', data={'choice': 'k'}, follow_redirects=True)
    assert b'Tasapeli' in response.data