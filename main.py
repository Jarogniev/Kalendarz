import json
import os
import sys
import calendar
import datetime

from PyQt6.QtGui import QFont, QAction, QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QColorDialog, \
    QMenuBar, QMenu, QInputDialog, QHBoxLayout
from PyQt6.QtCore import Qt


class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.notes = {}  # key: "YYYY-MM-DD"
        self.note_file = "notes.json"
        self.interface()

    def interface(self):

        layout = QVBoxLayout()

        self.setLayout(layout)
        self.resize(400, 400)
        self.setWindowTitle("Kalendarz")
        self.grid_layout = QGridLayout()
        menubar = self.create_menu()
        layout.setMenuBar(menubar)
        self.today_date()
        self.load_notes()

        # navigation through months
        nav_layout = QHBoxLayout()
        prev_button = QPushButton("< Poprzedni")
        next_button = QPushButton("Następny >")
        self.month_label = QLabel()
        prev_button.clicked.connect(self.prev_month)
        next_button.clicked.connect(self.next_month)
        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(self.month_label)
        nav_layout.addWidget(next_button)
        layout.addLayout(nav_layout)

        self.calendar_days()
        layout.addLayout(self.grid_layout)
        self.show()

    def create_menu(self):
        menubar = QMenuBar(self)

        menubar.addMenu(self.create_options())
        menubar.addMenu(self.create_edit_menu())

        return menubar

    def create_options(self):
        file_menu = QMenu("Opcje", self)

        open_action = QAction("Otwórz", self)
        exit_action = QAction("Zamknij", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(open_action)
        file_menu.addAction(exit_action)

        return file_menu

    def create_edit_menu(self):
        edit_menu = QMenu("Edycja", self)

        change_action = QAction("Zmiana Alfabetu", self)
        edit_menu.addAction(change_action)

        return edit_menu

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
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    btn.setProperty("date_str", date_str)
                    note = self.notes.get(date_str)
                    if note:
                        btn.setToolTip(note)
                        btn.setStyleSheet("background-color: lightblue")
                    btn.setFixedSize(40, 40)
                    btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                    btn.customContextMenuRequested.connect(lambda pos, b=btn: self.edit_note(b))
                    # btn.clicked.connect(lambda checked, b=btn: self.cell_color(b))
                    self.grid_layout.addWidget(btn, row, col)
                    self.buttons.append(btn)

    def edit_note(self, button):
        menu = QMenu()
        edit_action = QAction("Edytuj notatkę", self)
        delete_action = QAction("Usuń notatkę", self)

        menu.addAction(edit_action)
        menu.addAction(delete_action)

        edit_action.triggered.connect(lambda: self.add_or_edit_note(button))
        delete_action.triggered.connect(lambda: self.delete_note(button))

        menu.exec(QCursor.pos())

    def add_or_edit_note(self, button):
        date_str = button.property("date_str")
        current_note = self.notes.get(date_str, "")
        text, ok = QInputDialog.getText(self, "Notatka", "Edytuj notatkę:", text=current_note)
        if ok:
            self.notes[date_str] = text
            button.setToolTip(text)
            button.setStyleSheet("background-color: lightblue" if text.strip() else "")
            self.save_notes()

    def delete_note(self, button):
        date_str = button.property("date_str")
        if date_str in self.notes:
            del self.notes[date_str]
        button.setToolTip("")
        button.setStyleSheet("")
        self.save_notes()

    def save_notes(self):
        with open(self.note_file, "w", encoding="utf-8") as f:
            json.dump(self.notes, f, ensure_ascii=False, indent=2)

    def load_notes(self):
        if os.path.exists(self.note_file):
            with open(self.note_file, "r", encoding="utf-8") as f:
                self.notes = json.load(f)

    def prev_month(self):
        pass

    def next_month(self):
        pass

    def cell_color(self, button):
            color = QColorDialog.getColor()
            if color.isValid():
                button.setStyleSheet(f"background-color: {color.name()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 12))
    window = Calendar()
    sys.exit(app.exec())
