import unittest
from statistics_service import StatisticsService
from player import Player

class PlayerReaderStub:
    def get_players(self):
        return [
            Player("Semenko", "EDM", 4, 12),  #  4+12 = 16
            Player("Lemieux", "PIT", 45, 54), # 45+54 = 99
            Player("Kurri",   "EDM", 37, 53), # 37+53 = 90
            Player("Yzerman", "DET", 42, 56), # 42+56 = 98
            Player("Gretzky", "EDM", 35, 89)  # 35+89 = 124
        ]

class TestStatisticsService(unittest.TestCase):
    def setUp(self):
        # annetaan StatisticsService-luokan oliolle "stub"-luokan olio
        self.stats = StatisticsService(
            PlayerReaderStub()
        )

    def test_search_returns_player_when_substring_matches(self):
        p = self.stats.search("Gret")
        self.assertIsNotNone(p)
        self.assertEqual(p.name, "Gretzky")

    def test_no_match_returns_none(self):
        self.assertIsNone(self.stats.search("Unkown"))

    def test_filters_by_team(self):
        self.assertEqual([p.name for p in self.stats.team("EDM")], ["Semenko", "Kurri", "Gretzky"])

    def test_return_empty_list_when_team_has_no_players(self):
        self.assertEqual(self.stats.team("NYR"), [])

    def test_sorted_by_points_and_top_returns_how_many_plus_one(self):
        top2 = self.stats.top(2)
        self.assertEqual(len(top2), 2)
        self.assertEqual([p.name for p in top2][:2], ["Gretzky", "Lemieux"])

    def test_top_raises_index_error_when_request_exceeds_list(self):
        with self.assertRaises(IndexError):
            self.stats.top(10)