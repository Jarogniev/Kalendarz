
import sys
import calendar
from PyQt6.QtWidgets import QApplication, QWidget


def generate_calendar():
    year = 2025
    month = 3
    cal = calendar.month(year, month)
    return cal


class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()

    def interface(self):

        # TODO - current day month year
        self.setWindowTitle("Kalendarz")
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calendar()
    sys.exit(app.exec())
