# filament_gui.py

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QPushButton,
    QLineEdit, QListWidget, QMessageBox, QInputDialog
)
from filament_model import Filament  # <- importujemy logikę

class FilamentApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Magazyn Filamentu")
        self.setFixedSize(400, 500)
        self.filamenty = []

        layout = QVBoxLayout()

        self.typ_input = QLineEdit(placeholderText="Typ filamentu (np. PLA)")
        self.prod_input = QLineEdit(placeholderText="Producent")
        self.waga_input = QLineEdit(placeholderText="Waga bazowa (g)")

        layout.addWidget(QLabel("Dodaj nowy filament:"))
        layout.addWidget(self.typ_input)
        layout.addWidget(self.prod_input)
        layout.addWidget(self.waga_input)

        layout.addWidget(self._button("Dodaj filament", self.dodaj_filament))

        layout.addWidget(QLabel("Lista filamentów:"))
        self.lista = QListWidget()
        layout.addWidget(self.lista)

        layout.addWidget(self._button("Dodaj akcję (wydruk)", self.dodaj_akcje))
        layout.addWidget(self._button("Pokaż historię", self.pokaz_historie))

        self.setLayout(layout)

    def _button(self, text, callback):
        btn = QPushButton(text)
        btn.clicked.connect(callback)
        return btn

    def dodaj_filament(self):
        typ = self.typ_input.text().strip()
        prod = self.prod_input.text().strip()
        try:
            waga = float(self.waga_input.text())
        except ValueError:
            return self._blad("Waga musi być liczbą!")

        if not typ or not prod:
            return self._blad("Wypełnij wszystkie pola.")

        self.filamenty.append(Filament(typ, prod, waga))
        self.odswiez_liste()
        self.typ_input.clear(), self.prod_input.clear(), self.waga_input.clear()

    def dodaj_akcje(self):
        idx = self.lista.currentRow()
        if idx == -1:
            return self._blad("Wybierz filament z listy.")

        model, ok1 = QInputDialog.getText(self, "Model", "Nazwa modelu:")
        if not ok1 or not model.strip():
            return

        zuzycie_str, ok2 = QInputDialog.getText(self, "Zużycie", "Zużycie filamentu (g):")
        if not ok2:
            return

        try:
            zuzycie = float(zuzycie_str)
        except ValueError:
            return self._blad("Zużycie musi być liczbą!")

        filament = self.filamenty[idx]
        if not filament.zuzyj(model, zuzycie):
            return QMessageBox.critical(self, "Błąd", f"Za mało filamentu! Pozostało: {filament.waga_pozostala}g")

        QMessageBox.information(self, "Sukces", f"Zużyto {zuzycie}g na '{model}'.")
        self.odswiez_liste()

    def pokaz_historie(self):
        idx = self.lista.currentRow()
        if idx == -1:
            return self._blad("Wybierz filament z listy.")

        filament = self.filamenty[idx]
        if not filament.historia:
            return QMessageBox.information(self, "Historia", "Brak historii zużycia.")

        tekst = "\n".join(f"{i+1}. {nazwa} - {waga}g" for i, (nazwa, waga) in enumerate(filament.historia))
        QMessageBox.information(self, "Historia zużycia", tekst)

    def odswiez_liste(self):
        self.lista.clear()
        self.lista.addItems([str(f) for f in self.filamenty])

    def _blad(self, wiadomosc):
        QMessageBox.warning(self, "Błąd", wiadomosc)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = FilamentApp()
    okno.show()
    sys.exit(app.exec_())
