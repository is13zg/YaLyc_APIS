import maps
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QHBoxLayout, QRadioButton
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtCore import Qt

import sys

SCREEN_SIZE = [760, 460]


class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.coords = -1
        self.z = 16
        self.l = "map"

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Up:
            self.btn_up.click()

        elif e.key() == Qt.Key_Down:
            self.btn_down.click()

        elif e.key() == Qt.Key_Left:
            self.btn_left.click()

        elif e.key() == Qt.Key_Right:
            self.btn_right.click()

        elif e.key() == Qt.Key_PageUp:
            self.btn_big.click()

        elif e.key() == Qt.Key_PageDown:
            self.btn_small.click()

    def show_map(self):
        params = {"ll": self.coords,
                  "l": self.l,
                  "z": self.z}
        self.pixmap.loadFromData(maps.bytes_map(params))
        self.image.setPixmap(self.pixmap)

    def show_map_btn(self):
        self.coords = maps.get_coords(str(self.text.text()))
        if self.coords == -1:
            QMessageBox.about(self, "Error", "adress not found")
        elif self.coords == -2:
            QMessageBox.about(self, "Error", "server not response")
        else:
            self.show_map()

    def change_z(self):
        if type(self.coords) == int:
            QMessageBox.about(self, "Error", "no show")
            return
        if self.sender().text() == "+":
            self.z += 1
        else:
            self.z -= 1
        self.z = max(min(19, self.z), 2)
        self.show_map()

    def change_view(self):
        if self.sender().text() == "Scheme":
            self.l = "map"
        elif self.sender().text() == "Satellite":
            self.l = "sat"
        elif self.sender().text() == "Combo":
            self.l = "sat,skl"
        self.show_map()

    def change_ll(self):
        if type(self.coords) == int:
            QMessageBox.about(self, "Error", "no show")
            return
        delta = {
            19: 0.001,
            18: 0.002,
            17: 0.003,
            16: 0.004,
            15: 0.007,
            14: 0.01,
            13: 0.016,
            12: 0.03,
            11: 0.07,
            10: 0.15,
            9: 0.3,
            8: 0.6,
            7: 1.2,
            6: 2.4,
            5: 4.8,
            4: 9,
            3: 18,
            2: 36
        }

        coords = list(map(lambda x: float(x), self.coords.split(",")))

        if self.sender().text() == "←":
            coords[0] -= delta[self.z]
        elif self.sender().text() == "↓":
            coords[1] -= delta[self.z] / 2.0
        elif self.sender().text() == "→":
            coords[0] += delta[self.z]
        elif self.sender().text() == "↑":
            coords[1] += delta[self.z] / 2.0
        coords[0] = min(max(-180.0, coords[0]), 180.0)
        coords[1] = min(max(-85.0, coords[1]), 85.0)
        self.coords = ",".join(map(str, coords))
        self.show_map()

    def initUI(self):
        self.setGeometry(200, 200, *SCREEN_SIZE)
        self.setWindowTitle('Отображение картинки')

        ##поля текста
        self.text = QLineEdit(self)
        self.text.setText("казань гагарина 8")
        self.text.setGeometry(610, 5, 140, 25)
        # self.btn_right.clicked.connect()

        ##кнопка показаь карты
        self.btn_show = QPushButton('Show map', self)
        self.btn_show.setGeometry(680, 35, 70, 25)
        self.btn_show.clicked.connect(self.show_map_btn)

        ##кнопка увеличить масштаб
        self.btn_big = QPushButton('+', self)
        self.btn_big.setGeometry(610, 385, 30, 30)
        self.btn_big.clicked.connect(self.change_z)

        ##кнопка уменьшить масштаб
        self.btn_small = QPushButton('-', self)
        self.btn_small.setGeometry(610, 415, 30, 30)
        self.btn_small.clicked.connect(self.change_z)

        ##кнопка лево
        self.btn_left = QPushButton('←', self)
        self.btn_left.setGeometry(660, 415, 30, 30)
        self.btn_left.clicked.connect(self.change_ll)

        ##кнопка низ
        self.btn_down = QPushButton('↓', self)
        self.btn_down.setGeometry(690, 415, 30, 30)
        self.btn_down.clicked.connect(self.change_ll)

        ##кнопка вверх
        self.btn_up = QPushButton('↑', self)
        self.btn_up.setGeometry(690, 385, 30, 30)
        self.btn_up.clicked.connect(self.change_ll)

        ##кнопка право
        self.btn_right = QPushButton('→', self)
        self.btn_right.setGeometry(720, 415, 30, 30)
        self.btn_right.clicked.connect(self.change_ll)

        ##кнопки вида
        self.btn_scheme = QPushButton('Scheme', self)
        self.btn_scheme.setGeometry(610, 80, 50, 20)
        self.btn_scheme.clicked.connect(self.change_view)

        self.btn_satellite = QPushButton('Satellite', self)
        self.btn_satellite.setGeometry(660, 80, 50, 20)
        self.btn_satellite.clicked.connect(self.change_view)

        self.btn_сombo = QPushButton('Combo', self)
        self.btn_сombo.setGeometry(710, 80, 50, 20)
        self.btn_сombo.clicked.connect(self.change_view)

        ## Изображение
        self.pixmap = QPixmap()
        self.image = QLabel(self)
        self.image.setGeometry(5, 5, 600, 450)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    sys.exit(app.exec())
