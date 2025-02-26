# kalendarz
# -----------------------
# funkcjonalności:
# - otwiera się kiedy są jakieś wpisy danego dnia
# - włącza alarm kiedy są jakieś wpisy
# - można zaznaczać kolorami ciągi dni tygodnia/tygodnie wyjazdy itp
# - możliwość przekonwertowania kliknięciem na głagolicę
# - na hasło
# - zmienia date i aktualizuje się przez neta

from PyQt6.QtWidgets import QApplication, QWidget


# TODO - function to generate a calendar

class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()

    def interface(self):

        # TODO - current day month year
        self.setWindowTitle("Kalendarz")
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Calendar()
    # print(calendar.weekday(2025, 2, 21))
    sys.exit(app.exec())
