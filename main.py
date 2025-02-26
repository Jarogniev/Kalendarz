
import sys
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
    app = QApplication(sys.argv)
    window = Calendar()
    sys.exit(app.exec())
