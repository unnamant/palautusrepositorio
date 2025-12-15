from flask import Flask, render_template, request, session, redirect, url_for
import secrets
from tehdas import luo_peli

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

WINNING_SCORE = 3

@app.route('/')
def index():
    session.clear()
    return render_template('index.html')

@app.route('/start', methods=['POST'])
def start():
    mode = request.form.get('mode')
    session['mode'] = mode
    session['tuomari_data'] = {'ekan_pisteet': 0, 'tokan_pisteet': 0, 'tasapelit': 0}
    session['peli_siirrot'] = []
    session['game_over'] = False
    session['winner'] = None
    
    if mode == 'a':
        session['current_player'] = 1
        session['player1_move'] = None
        return redirect(url_for('game'))
    
    return redirect(url_for('game'))

@app.route('/game')
def game():
    if 'mode' not in session:
        return redirect(url_for('index'))
    
    mode = session.get('mode')
    
    if session.get('game_over'):
        return render_template('game_over.html', 
                             tuomari=session.get('tuomari_data'),
                             winner=session.get('winner'),
                             mode=mode)
    
    if mode == 'a' and session.get('current_player') == 2:
        return render_template('game_player2.html', tuomari=session.get('tuomari_data'))
    
    return render_template('game.html', 
                         tuomari=session.get('tuomari_data'),
                         current_player=session.get('current_player', 1))

@app.route('/play', methods=['POST'])
def play():
    player_move = request.form.get('choice')
    mode = session.get('mode')
    
    if not mode or player_move not in ['k', 'p', 's']:
        return redirect(url_for('index'))
    
    if session.get('game_over'):
        return redirect(url_for('game'))
    
    if mode == 'a' and session.get('current_player') == 1:
        session['player1_move'] = player_move
        session['current_player'] = 2
        return redirect(url_for('game'))
    
    if mode == 'a':
        computer_move = player_move
        player_move = session.get('player1_move')
        session['current_player'] = 1
    elif mode == 'b':
        import random
        computer_move = random.choice(['k', 'p', 's'])
    elif mode == 'c':
        siirrot = session.get('peli_siirrot', [])
        if siirrot:
            viimeisin = siirrot[-1]
            if viimeisin == 'k':
                computer_move = 'p'
            elif viimeisin == 'p':
                computer_move = 's'
            else:
                computer_move = 'k'
        else:
            import random
            computer_move = random.choice(['k', 'p', 's'])
        
        siirrot.append(player_move)
        session['peli_siirrot'] = siirrot
    else:
        import random
        computer_move = random.choice(['k', 'p', 's'])
    
    tuomari_data = session.get('tuomari_data')
    
    if player_move == computer_move:
        tuomari_data['tasapelit'] += 1
        result = 'Tasapeli!'
    elif (player_move == 'k' and computer_move == 's') or \
         (player_move == 's' and computer_move == 'p') or \
         (player_move == 'p' and computer_move == 'k'):
        tuomari_data['ekan_pisteet'] += 1
        result = 'Pelaaja 1 voitti!' if mode == 'a' else 'Voitit!'
    else:
        tuomari_data['tokan_pisteet'] += 1
        result = 'Pelaaja 2 voitti!' if mode == 'a' else 'Hävisit!'
    
    session['tuomari_data'] = tuomari_data
    session['last_result'] = {
        'player': player_move,
        'computer': computer_move,
        'message': result
    }
    
    if tuomari_data['ekan_pisteet'] >= WINNING_SCORE:
        session['game_over'] = True
        session['winner'] = 'Pelaaja 1' if mode == 'a' else 'Sinä'
    elif tuomari_data['tokan_pisteet'] >= WINNING_SCORE:
        session['game_over'] = True
        session['winner'] = 'Pelaaja 2' if mode == 'a' else 'Vastustaja'
    
    return redirect(url_for('game'))

if __name__ == '__main__':
    app.run(debug=True)