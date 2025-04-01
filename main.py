import sys
import calendar
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton
from PyQt6.QtCore import Qt


class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()

    def interface(self):

        layout = QVBoxLayout()

        # TODO - current day month year
        self.setLayout(layout)
        self.resize(400, 400)
        self.setWindowTitle("Kalendarz")
        self.grid_layout = QGridLayout()
        self.calendar_days()
        layout.addLayout(self.grid_layout)
        self.show()

    def calendar_days(self, year=2025, month=3):
        cal = calendar.monthcalendar(year, month)
        days = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nd"]
        for col, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(label, 0, col)

        self.buttons = []
        for row, week in enumerate(cal, start=1):
            for col, day in enumerate(week):
                if day != 0:
                    btn = QPushButton(str(day))
                    btn.setFixedSize(40, 40)
                    # change button color
                    self.grid_layout.addWidget(btn, row, col)
                    self.buttons.append(btn)

        # def change button color


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Calendar()
    sys.exit(app.exec())
