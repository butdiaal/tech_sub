from PyQt6 import *
from app.graf.employees_graf import *
import database.db as db


class Employee_Window(QtWidgets.QWidget, Employee_Ui_Form):
    def __init__(self, parent=None, employee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id
        # self.init_ui()

        self.layout_types = QtWidgets.QVBoxLayout(self.groupBox_types)
        self.layout_status = QtWidgets.QVBoxLayout(self.groupBox_status)

        types = db.get_types()
        self.radios_types = []
        for type in types:
            radio_types = QtWidgets.QRadioButton(type[0])
            self.layout_types.addWidget(radio_types)
            self.radios_types.append(radio_types)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Employee_Window()
    win.show()
    sys.exit(app.exec())
