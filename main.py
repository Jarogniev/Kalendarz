# kalendarz
# -----------------------
# funkcjonalności:
# - otwiera się kiedy są jakieś wpisy danego dnia
# - włącza alarm kiedy są jakieś wpisy
# - możliwość przekonwertowania kliknięciem na głagolicę
# - na hasło
# - zmienia date i aktualizuje się przez neta

from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QGridLayout


class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()

    def interface(self):

        # Labels
        label1 = QLabel("Dzień", self)
        label2 = QLabel("Miesiąc", self)
        label3 = QLabel("Rok", self)

        # assigning widgets to the tabular layout
        grid = QGridLayout()
        grid.addWidget(label1, 0, 0)
        grid.addWidget(label2, 0, 1)
        grid.addWidget(label3, 0, 2)

        # assigning the created layout to the window
        self.setLayout(grid)

        self.setGeometry(20, 20, 500, 800)
        # self.setWindowIcon(QIcon('.png'))
        self.setWindowTitle("Kalendarz")
        self.show()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    window = Calendar()
    sys.exit(app.exec_())
