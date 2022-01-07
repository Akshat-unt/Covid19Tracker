from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QLineEdit, QDesktopWidget
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from fetch_data import get_data
from create_pdf import export_to_pdf
from create_message import output_message
import sys


class MyWindow(QMainWindow):
    """
    Main application class that stores components and initialize UI. It inherits properties from
    QMainWindow class.
    """
    def __init__(self):
        super().__init__()
        self.setFixedSize(800, 675)
        # Centering app's window
        qt_rect = self.frameGeometry()
        center_point = QDesktopWidget().availableGeometry().center()
        qt_rect.moveCenter(center_point)
        self.move(qt_rect.topLeft())
        self.setWindowIcon(QIcon('./img/title_icon.png'))
        self.setWindowTitle('COVID-19 Python App')

        self.UI_components()

    def UI_components(self):
        """
        Method initializing each component and giving one particular attributes.
        """

        # Label used to set a background image
        self.bg_label = QtWidgets.QLabel(self)
        self.bg_label.setGeometry(0, 0, 800, 800)
        self.bg_label.setStyleSheet("background-image: url('./img/bg.jpg');")

        # Label above searching text field
        self.input_label = QtWidgets.QLabel(self)
        self.input_label.move(250, 100)
        self.input_label.resize(300, 60)
        self.input_label.setAlignment(Qt.AlignCenter)
        self.input_label.setText("Enter country's name: ")
        f = self.input_label.font()
        f.setPointSize(20)
        self.input_label.setFont(f)
        self.input_label.setStyleSheet('background-color: transparent;'
                                       'color: #fff;'
                                       'font-weight: bold;')

        # Country's input text field
        self.input_country = QLineEdit(self)
        self.input_country.move(275, 175)
        self.input_country.resize(250, 60)
        self.input_country.setAlignment(Qt.AlignCenter)
        f = self.input_country.font()
        f.setPointSize(16)
        self.input_country.setFont(f)
        self.input_country.setStyleSheet('background-color: #fafafa; '
                                         'color: #111;'
                                         'border-style: outset;'
                                         'border-width: 5px;'
                                         'border-radius: 30px;'
                                         'border-color: #00d0f5;'
                                         'padding: 4px;'
                                         'font-weight: bold;')

        # Submit button
        self.submit_btn = QtWidgets.QPushButton(self)
        self.submit_btn.move(325, 270)
        self.submit_btn.resize(150, 50)
        self.submit_btn.setText('Submit')
        f = self.submit_btn.font()
        f.setPointSize(14)
        self.submit_btn.setFont(f)
        self.submit_btn.clicked.connect(self.submit)
        self.submit_btn.setStyleSheet('background-color: #00d0f5;'
                                      'color: #fff;'
                                      'border-style: outset;'
                                      'border-width: 3px;'
                                      'border-radius: 3px;'
                                      'font-weight: bold;')

        # Utility components (labels and buttons)
        self.info_label = QtWidgets.QLabel(self)
        self.download_label = QtWidgets.QLabel(self)
        self.error_label = QtWidgets.QLabel(self)

        self.delete_btn = QtWidgets.QPushButton(self)
        self.delete_btn.hide()
        self.download_btn = QtWidgets.QPushButton(self)
        self.download_btn.hide()

    def submit(self):
        self.download_label.hide()
        country = self.input_country.text()
        self.input_country.setText('')

        try:
            response = get_data(country)
        except requests.exceptions.RequestException:
            print('Check your Internet connection!')
            response = None
        if response is not None:
            try:
                data = response.json()
                newest_data = data[-1]
            except KeyError:
                self.create_error_label()
                self.info_label.hide()
                self.delete_btn.hide()
                return
            else:
                title, date, message = output_message(newest_data)
                self.info_label.show()
                self.create_info_label(title, date, message)
                self.create_delete_btn()
                self.create_download_btn(data)
                self.error_label.setText('')

    def create_info_label(self, title, date, message):
        self.info_label.move(200, 360)
        self.info_label.resize(400, 250)
        self.info_label.setAlignment(Qt.AlignCenter)
        self.info_label.setText(f"{title}\n\nDate: {date}\n{message}")
        self.info_label.setStyleSheet('background-color: rgba(0, 0, 0, 0.6);'
                                      'color: #fff;'
                                      'border-style: outset;'
                                      'border-width: 3px;'
                                      'border-radius: 3px;'
                                      'border-color: #00d0f5;'
                                      'font-weight: bold;'
                                      'font-size: 21px')

    def create_error_label(self):
        self.download_btn.hide()
        self.error_label.move(150, 30)
        self.error_label.resize(500, 70)
        self.error_label.setText('There was an error retrieving the data\nPlease try again')
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setStyleSheet('color: red;'
                                       'font-size: 26px;')

    def create_download_label(self):
        self.download_label.show()
        self.download_label.move(200, 30)
        self.download_label.resize(400, 40)
        self.download_label.setAlignment(Qt.AlignCenter)
        self.download_label.setStyleSheet('color: green;'
                                          'font-size: 16px;'
                                          'font-weight: bold;')

    def create_delete_btn(self):
        self.delete_btn.show()
        self.delete_btn.move(335, 640)
        self.delete_btn.resize(130, 50)
        self.delete_btn.setText('Clear')
        self.delete_btn.clicked.connect(self.clear_content)
        self.delete_btn.setStyleSheet('background-color: rgb(220, 20, 60);'
                                      'color: #fff;'
                                      'border-style: outset;'
                                      'border-radius: 5px;'
                                      'font-weight: bold;'
                                      'font-size: 20px;')

    def create_download_btn(self, data):
        self.download_btn.show()
        self.download_btn.move(320, 30)
        self.download_btn.resize(140, 40)
        self.download_btn.setText('Download PDF')
        self.download_btn.clicked.connect(lambda: self.create_pdf_plot(data))
        self.download_btn.setStyleSheet('background-color: #fff;'
                                        'color: #777;'
                                        'border-style: outset;'
                                        'border-width: 3px;'
                                        'border-color: rgb(220, 20, 60);'
                                        'border-radius: 5px;'
                                        'font-size: 16px;'
                                        'font-weight: bold;'
                                        'padding: 5px;')

    def create_pdf_plot(self, data):
        export_to_pdf(data)
        self.download_btn.hide()
        self.create_download_label()
        self.download_label.setText(f"You've downloaded the file successfully!\n "
                                     f"Path: /stats/{data[-1]['Country']}.pdf")

        # Disconnect event listener to avoid multiple downloading
        self.download_btn.disconnect()

    def clear_content(self):
        self.info_label.hide()
        self.delete_btn.hide()
        self.download_btn.hide()
        self.download_label.hide()


def window():
    app = QApplication(sys.argv)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    window()




