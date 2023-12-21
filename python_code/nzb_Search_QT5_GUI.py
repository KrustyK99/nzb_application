from PyQt5.QtWidgets import *
from PyQt5.QtGui import QFont

def main():
    app = QApplication([])
    window = QWidget()
    window.setGeometry(100,100,200,300)
    window.setWindowTitle("NZB Search")

    layout = QVBoxLayout()

    label = QLabel("Press the Button to Run NZB Search")
    textbox = QTextEdit()
    button = QPushButton("Run")

    button.clicked.connect(lambda: on_clicked(textbox.toPlainText()))

    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    # label.setText("Hello World")
    # label.setFont(QFont("Arial", 16))
    # label.move(50,100)

    window.setLayout(layout)

    window.show()
    app.exec_()

def on_clicked(msg):
    print("Button pressed")
    message = QMessageBox()
    message.setText(msg)
    message.exec_()

if __name__ == '__main__':
    main()
    

