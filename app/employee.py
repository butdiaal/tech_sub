from PyQt6 import *
from app.graf.employees_graf import *
import database.db as db


class Employee_Window(QtWidgets.QWidget, Employee_Ui_Form):
    def __init__(self, parent=None, employee_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.employee_id = employee_id
        # self.init_ui()

        self.layout_types = QtWidgets.QVBoxLayout(self.scrollArea_types)
        self.layout_status = QtWidgets.QVBoxLayout(self.scrollArea_status)
        self.layout_tickets = QtWidgets.QVBoxLayout(self.scrollArea_tickets)
        self.scroll_widget_types = QtWidgets.QWidget()
        self.layout_types = QtWidgets.QVBoxLayout(self.scroll_widget_types)
        self.scrollArea_types.setWidget(self.scroll_widget_types)

        # Для статусов
        self.scroll_widget_status = QtWidgets.QWidget()
        self.layout_status = QtWidgets.QVBoxLayout(self.scroll_widget_status)
        self.scrollArea_status.setWidget(self.scroll_widget_status)

        # Для тикетов
        self.scroll_widget_tickets = QtWidgets.QWidget()
        self.layout_tickets = QtWidgets.QVBoxLayout(self.scroll_widget_tickets)
        self.scrollArea_tickets.setWidget(self.scroll_widget_tickets)

        self.scrollArea_types.verticalScrollBar()
        self.scrollArea_status.verticalScrollBar()
        self.scrollArea_tickets.verticalScrollBar()

        types = db.get_types()
        self.radios_types = []
        if not types:
            print("No types returned from database!")
        else:
            for type_data in types:
                radio = QtWidgets.QRadioButton(type_data[0])  # Преобразуем в строку на случай если None
                self.layout_types.addWidget(radio)
                self.radios_types.append(radio)

        statuses = db.get_statuses()
        self.radios_statuses = []
        if not statuses:
            print("No statuses returned from database!")
        else:
            for status in statuses:
                radio = QtWidgets.QRadioButton(status[0])  # Преобразуем в строку на случай если None
                self.layout_status.addWidget(radio)
                self.radios_statuses.append(radio)




if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    win = Employee_Window()
    win.show()
    sys.exit(app.exec())
