import requests

class Player:
    def __init__(self, dict):
        self.name = dict['name']
        self.team = dict['team']
        self.goals = dict['goals'] 
        self.nationality = dict['nationality']
        self.assists = dict['assists']

    def __str__(self):
        return f"{self.name} {self.team} {self.goals} + {self.assists} = {self.goals + self.assists}"

class PlayerReader:
    def __init__(self, url: str):
        self.url = url

    def get_players(self):
        response = requests.get(self.url).json()

        players = []
        for player_dict in response: 
            player = Player(player_dict) 
            players.append(player)

        return players

class PlayerStats:
    def __init__(self, reader: PlayerReader):
        self.reader = reader
        self.players = reader.get_players()

    def top_scorers_by_nationality(self, nationality: str):
        players = []
        for player in self.players:
            if player.nationality == nationality:
                players.append(player)
        sorted_players = sorted(players, key=lambda player: player.goals + player.assists, reverse=True)
        return sorted_players

    def __str__(self):
        return (player for player in self.players)
