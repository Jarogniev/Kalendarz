from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox, QApplication


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logowanie")
        self.setFixedSize(300, 150)

        self.attempts = 0
        self.max_attempts = 3

        layout = QVBoxLayout()

        self.label = QLabel("Podaj hasło:")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.returnPressed.connect(self.check_password)

        self.login_button = QPushButton("Zaloguj")
        self.login_button.clicked.connect(self.check_password)

        self.exit_button = QPushButton("Zamknij")
        self.exit_button.clicked.connect(QApplication.quit)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)

    def check_password(self):
        from main import Calendar

        password = self.password_input.text()
        if password == "123":
            self.attempts = 0
            self.calendar = Calendar()
            self.calendar.show()
            self.close()
        else:
            self.attempts += 1
            remaining = self.max_attempts - self.attempts

            if remaining <= 0:
                QMessageBox.critical(self, "Błąd", "Za dużo nieudanych prób. Aplikacja zostanie zamknięta.")
                QApplication.quit()
            else:
                QMessageBox.warning(
                    self,
                    "Błąd",
                    f"Kaktus! \n Nieprawidłowe hasło! Pozostało prób: {remaining}"
                )
                self.password_input.clear()


