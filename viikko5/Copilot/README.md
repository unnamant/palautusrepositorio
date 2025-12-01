# Palautusrepositorio — web scaffold

Tämä on minimal Flask + SQLite -sovellus kurssitehtävän palautusta varten. Se tarjoaa:
- Useiden varastojen luomisen ja listauksen
- Tuotteiden lisäämisen ja poistamisen jokaisessa varastossa
- Helpon käynnistysohjeen

Asennus ja ajo:
1. Asenna riippuvuudet Poetryllä:
	poetry install
2. Aktivoi Poetryn virtuaaliympäristö:
	poetry shell
3. Aja sovellus:
	poetry run python app.py
4. Avaa selaimessa http://127.0.0.1:5000

Huom:
- Tämä scaffold on tarkoitus olla varmistus palautukselle, jos Copilot ei ehdi luoda PR:ää.
- Tehtävänannossa halutaan yleensä Copilotin luoma PR ja View session -näytön tallenne. Muista suorittaa Copilot‑flows myös, jos tehtävänanto vaatii sen.
