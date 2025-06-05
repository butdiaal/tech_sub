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
        self.layout_tickets = QtWidgets.QVBoxLayout(self.groupBox_tickets)

        types = db.get_types()
        self.radios_types = []
        if not types:
            print("No types returned from database!")
        else:
            for type_data in types:
                radio = QtWidgets.QRadioButton(type_data[0])  # Преобразуем в строку на случай если None
                self.layout_types.addWidget(radio)
                self.radios_types.append(radio)




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Employee_Window()
    win.show()
    sys.exit(app.exec())
