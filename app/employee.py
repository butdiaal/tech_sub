from PyQt6 import *
from app.graf.employees_graf import *
from database.db import *

class Employee_Window(QtWidgets, Employee_Ui_Form):
    def __init__(self, parent=None, employee_id = None):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id
        # self.init_ui()

        self.layout_types = QtWidgets.QVBoxLayout(self.groupBox_types)
        self.layout_status = QtWidgets.QVBoxLayout(self.groupBox_status)


        types =
        for type in types:












if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Employee_Ui_Form()
    win.show()
    sys.exit(app.exec())
