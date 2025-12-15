from kps_pelaaja_vs_pelaaja import KPSPelaajaVsPelaaja
from kps_tekoaly import KPSTekoaly
from kps_parempi_tekoaly import KPSParempiTekoaly


def luo_peli(tyyppi: str):
    if tyyppi == "a":
        return KPSPelaajaVsPelaaja()
    if tyyppi == "b":
        return KPSTekoaly()
    if tyyppi == "c":
        return KPSParempiTekoaly()
    return None