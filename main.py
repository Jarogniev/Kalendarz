
import sys
import calendar
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout
from PyQt6.QtCore import Qt


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

        layout = QVBoxLayout()
        cal_label = QLabel(generate_calendar())
        cal_label.setStyleSheet("font-size: 14pt;")
        layout.addWidget(cal_label)

        # TODO - current day month year
        self.setLayout(layout)
        self.resize(400, 400)
        self.setWindowTitle("Kalendarz")
        self.grid_layout = QGridLayout()
        self.calendar_days()
        layout.addLayout(self.grid_layout)
        self.show()

    def calendar_days(self):
        days = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nd"]
        for col, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(label, 0, col)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calendar()
    sys.exit(app.exec())
