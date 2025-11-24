HINTA = 5


class Kassapaate:
    def __init__(self):
        self.__myytyja_lounaita = 0

    def lataa(self, kortti, summa):
        if summa > 0:
            kortti.lataa(summa)
            return True
        return False

    def osta_lounas(self, kortti):
        if kortti.saldo() >= HINTA:
            kortti.osta(HINTA)
            self.__myytyja_lounaita = self.__myytyja_lounaita + 1
            return True
        return False