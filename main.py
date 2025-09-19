import json
import os
import sys
import calendar
import datetime

from PyQt6.QtGui import QFont, QAction, QCursor
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QGridLayout, QPushButton, QColorDialog, \
    QMenuBar, QMenu, QInputDialog, QHBoxLayout, QTextEdit, QLineEdit, QListWidget
from PyQt6.QtCore import Qt

from login_window import LoginWindow


class Calendar(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.current_year = datetime.date.today().year
        self.current_month = datetime.date.today().month
        self.notes = {}  # key: "YYYY-MM-DD"
        self.note_file = "notes.json"
        self.interface()

    def interface(self):
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)
        self.resize(700, 400)
        self.setWindowTitle("Kalendarz")

        # --- LEWA STRONA: To-do lista ---
        todo_layout = QVBoxLayout()
        todo_label = QLabel("Lista rzeczy do zrobienia:")
        self.todo_input = QLineEdit()
        self.todo_input.setPlaceholderText("Wpisz zadanie i naciśnij Enter")
        self.todo_input.returnPressed.connect(self.add_todo)

        self.todo_list = QListWidget()
        self.todo_list.itemDoubleClicked.connect(self.remove_todo)

        todo_layout.addWidget(todo_label)
        todo_layout.addWidget(self.todo_input)
        todo_layout.addWidget(self.todo_list)

        # --- PRAWA STRONA: Kalendarz ---
        right_layout = QVBoxLayout()

        self.grid_layout = QGridLayout()
        menubar = self.create_menu()
        right_layout.setMenuBar(menubar)

        nav_layout = QHBoxLayout()
        prev_button = QPushButton("Poprzedni")
        next_button = QPushButton("Następny")
        self.month_label = QLabel()
        self.month_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        prev_button.clicked.connect(self.prev_month)
        next_button.clicked.connect(self.next_month)

        nav_layout.addWidget(prev_button)
        nav_layout.addWidget(self.month_label)
        nav_layout.addWidget(next_button)
        right_layout.addLayout(nav_layout)
        right_layout.addLayout(self.grid_layout)

        self.note_display = QTextEdit()
        self.note_display.setReadOnly(True)
        right_layout.addWidget(self.note_display)

        # Dodaj obie kolumny
        main_layout.addLayout(todo_layout, 1)
        main_layout.addLayout(right_layout, 3)

        # Wczytaj dane
        self.load_notes()
        self.calendar_days()
        self.update_note_display()
        self.update_todo_list()

    def add_todo(self):
        task = self.todo_input.text().strip()
        if task:
            self.notes.setdefault("todos", []).append(task)
            self.todo_input.clear()
            self.update_todo_list()
            self.save_notes()

    def remove_todo(self, item):
        task = item.text()
        if "todos" in self.notes and task in self.notes["todos"]:
            self.notes["todos"].remove(task)
            self.update_todo_list()
            self.save_notes()

    def update_todo_list(self):
        self.todo_list.clear()
        for task in self.notes.get("todos", []):
            self.todo_list.addItem(task)

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

    def calendar_days(self):
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        year = self.current_year
        month = self.current_month
        self.month_label.setText(f"{calendar.month_name[month]} {year}")

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
                    date_str = f"{year}-{month:02d}-{day:02d}"
                    btn.setProperty("date_str", date_str)
                    note = self.notes.get(date_str)
                    if note:
                        btn.setToolTip(note)
                        btn.setStyleSheet("background-color: lightblue")
                    btn.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
                    btn.customContextMenuRequested.connect(lambda pos, b=btn: self.edit_note(b))
                    btn.clicked.connect(lambda checked, b=btn: self.cell_color(b))
                    self.grid_layout.addWidget(btn, row, col)
                    self.buttons.append(btn)

    def edit_note(self, date_str):
        text, ok = QInputDialog.getText(self, "Dodaj notatkę", f"Notatka dla {date_str}:")
        if ok and text.strip():
            # jeśli brak listy, twórz nową
            self.notes.setdefault(date_str, [])
            if isinstance(self.notes[date_str], str):
                # jeśli stara wersja była stringiem, zamień na listę
                self.notes[date_str] = [self.notes[date_str]]
            self.notes[date_str].append(text.strip())

            self.save_notes()
            self.update_note_display()
            # self.!xyz!(date_str)

    def add_or_edit_note(self, button):
        date_str = button.property("date_str")
        current_note = self.notes.get(date_str, "")
        text, ok = QInputDialog.getText(self, "Notatka", "Edytuj notatkę:", text=current_note)
        if ok:
            self.notes[date_str] = text
            button.setToolTip(text)
            button.setStyleSheet("background-color: lightblue" if text.strip() else "")
            self.save_notes()
            self.update_note_display()

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
        self.current_month -= 1
        if self.current_month < 1:
            self.current_month = 12
            self.current_year -= 1
        self.calendar_days()
        self.update_note_display()

    def next_month(self):
        self.current_month += 1
        if self.current_month > 12:
            self.current_month = 1
            self.current_year += 1
        self.calendar_days()
        self.update_note_display()

    def update_note_display(self):
        current_notes = []
        for date_str, note in self.notes.items():
            try:
                date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
                if date.year == self.current_year and date.month == self.current_month:
                    current_notes.append(f"{date_str}: {note}")
            except ValueError:
                pass

        if current_notes:
            self.note_display.setText("\n".join(sorted(current_notes)))
        else:
            self.note_display.setText("Brak notatek w tym miesiącu.")

    def cell_color(self, button):
        color = QColorDialog.getColor()
        if color.isValid():
            button.setStyleSheet(f"background-color: {color.name()}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setFont(QFont("Arial", 12))
    login = LoginWindow()
    login.show()
    sys.exit(app.exec())
