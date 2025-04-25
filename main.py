import sys
import calendar
import datetime

from PyQt6.QtGui import QFont
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QColorDialog, QMenuBar
from PyQt6.QtCore import Qt


class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.interface()

    def interface(self):

        layout = QVBoxLayout()

        menubar = QMenuBar(self)
        file_menu = menubar.addMenu("Test")

        layout.setMenuBar(menubar)
        self.setLayout(layout)

        self.setLayout(layout)
        self.resize(400, 400)
        self.setWindowTitle("Kalendarz")
        self.grid_layout = QGridLayout()
        self.today_date()
        self.calendar_days()
        layout.addLayout(self.grid_layout)
        self.show()

    def today_date(self):
        today = datetime.date.today()
        label = QLabel(str(today))
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.grid_layout.addWidget(label)
        # date setting "month year"

    def calendar_days(self, year=2025, month=3):
        cal = calendar.monthcalendar(year, month)
        days = ["Pon", "Wt", "Śr", "Czw", "Pt", "Sob", "Nd"]
        for col, day in enumerate(days):
            label = QLabel(day)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.grid_layout.addWidget(label, 1, col)

        self.buttons = []
        for row, week in enumerate(cal, start=2):
            for col, day in enumerate(week):
                if day != 0:
                    btn = QPushButton(str(day))
                    btn.setFixedSize(40, 40)
                    btn.clicked.connect(lambda checked, b=btn: self.cell_color(b))
                    self.grid_layout.addWidget(btn, row, col)
                    self.buttons.append(btn)

    def cell_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 12))
    window = Calendar()
    sys.exit(app.exec())
