# filament_model.py

class Filament:
    def __init__(self, typ, producent, waga_bazowa):
        self.typ = typ
        self.producent = producent
        self.waga_bazowa = waga_bazowa
        self.waga_pozostala = waga_bazowa
        self.historia = []

    def zuzyj(self, model, waga):
        if waga > self.waga_pozostala:
            return False
        self.waga_pozostala -= waga
        self.historia.append((model, waga))
        return True

    def __str__(self):
        return f"{self.typ} ({self.producent}) - {self.waga_pozostala}/{self.waga_bazowa}g"
