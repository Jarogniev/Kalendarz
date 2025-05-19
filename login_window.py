from PyQt6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Logowanie")
        self.setFixedSize(300, 120)

        layout = QVBoxLayout()
        self.label = QLabel("Podaj hasło:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)

        self.login_button = QPushButton("Zaloguj")
        self.login_button.clicked.connect(self.check_password)

        layout.addWidget(self.label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)

        self.setLayout(layout)

    def check_password(self):
        from main import Calendar
        if self.password_input.text() == "123":
            self.calendar = Calendar()
            self.calendar.show()
            self.close()
        else:
            QMessageBox.warning(self, "Błąd", "Kaktus! \n Nieprawidłowe hasło!")
