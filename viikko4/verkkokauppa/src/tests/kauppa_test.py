import unittest
from unittest.mock import Mock, ANY, call
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):

    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()

        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

        self.varasto_mock = Mock()            

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 6
            if tuote_id == 3:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "murot", 2)
            if tuote_id == 3:
                return Tuote(3, "kahvi", 0)
            
        # otetaan toteutukset käyttöön
        self.varasto_mock.saldo.side_effect = varasto_saldo
        self.varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        self.kauppa = Kauppa(self.varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)


        # tehdään ostokset
    def test_yhden_tuotteen_osto(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_kahden_tuotteen_osto(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "09876")

        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "09876", "33333-44455", 7)

    def test_loppunut_tuote(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.lisaa_koriin(3)
        self.kauppa.tilimaksu("sointu", "54321")

    # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("sointu", 42, "54321", "33333-44455", 2)
    # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_uusi_asioniti_nollaa_aikaisemman(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(2)
        self.kauppa.tilimaksu("sointu", "54321")

        self.viitegeneraattori_mock.uusi.return_value = 42
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "09876")

        self.pankki_mock.tilisiirto.assert_called_with("matti", 42, "09876", "33333-44455", 5)

    def test_jokaiselle_maksulle_uusi_viitenumero(self):
        self.viitegeneraattori_mock.uusi.side_effect = [1, 2]

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("pekka", "11111")

        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.tilimaksu("matti", "22222")

        self.assertEqual(self.viitegeneraattori_mock.uusi.call_count, 2)

        self.pankki_mock.tilisiirto.assert_has_calls([
            call("pekka", 1, "11111", "33333-44455", 5),
            call("matti", 2, "22222", "33333-44455", 5),
        ])

    def test_tuotteen_poistaminen_korista(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.lisaa_koriin(1)
        self.kauppa.lisaa_koriin(2)
        self.kauppa.poista_korista(2)
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_tilimaksu_ei_kutsu_pankkia_jos_kori_tyhja(self):
        self.kauppa.aloita_asiointi()
        self.kauppa.tilimaksu("pekka", "12345")

        self.pankki_mock.tilisiirto.assert_not_called()