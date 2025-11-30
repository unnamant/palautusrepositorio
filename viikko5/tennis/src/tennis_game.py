class TennisGame:
    scores = ["Love", "Fifteen", "Thirty", "Forty"]
    
    min_points_for_endgame = 4
    advantage_diff = 1
    winning_diff = 2

    def __init__(self, player1_name, player2_name):
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.m_score1 = 0
        self.m_score2 = 0

    def won_point(self, player_name):
        if player_name == self.player1_name:
            self.m_score1 += 1
        else:
            self.m_score2 += 1

    def get_score(self):
        if self.m_score1 == self.m_score2:
            return self._tie()
        
        if self.m_score1 >= 4 or self.m_score2 >= 4:
            return self._endgame()
        
        return self._running_game()
    
    def _tie(self):
        if self.m_score1 == self.m_score2:
            if self.m_score1 < 3:
                score_name = self._point_name(self.m_score1)
                return f"{score_name}-All"
        return "Deuce"
    
    def _endgame(self):
        point_difference = self.m_score1 - self.m_score2

        if point_difference == self.advantage_diff:
            return f"Advantage {self.player1_name}"
        if point_difference == -self.advantage_diff:
            return f"Advantage {self.player2_name}"
        if point_difference >= self.winning_diff:
            return f"Win for {self.player1_name}"
        return f"Win for {self.player2_name}"

    def _running_game(self):
        self.m_score1 = self._point_name(self.m_score1)
        self.m_score2 = self._point_name(self.m_score2)
        return f"{self.m_score1}-{self.m_score2}" 
    
    def _point_name(self, points):
        return self.scores[points]
