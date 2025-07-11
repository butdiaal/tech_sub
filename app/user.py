"""Лист заявок, Создание заявки,
Удаление заявки(если статус = В ОЖИДАНИИ),
Редактирование заявки(если статус = В ОЖИДАНИИ),
Просмотр заявки(В ОТДЕЛЬНОМ ОКНЕ)"""
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMessageBox

from app.graf.user_graf import *
from app.new_ticket import Supp_Window
from app.watch_ticket import Watch_Window
from app.update_ticket import Update_Window
from database.db import select_tickets_user, delete_ticket, select_status


class User_Window(User_Ui_Form, QtWidgets.QWidget):
    def __init__(self, parent=None, user_id=None):
        super().__init__(parent)
        self.setupUi(self)
        self.user_id = user_id
        self.init_ui()

    def init_ui(self):
        """Инициализация интерфейса"""
        self.selected_ticket = None
        self.selected_ticket_id = None
        self.load_tickets = select_tickets_user(self.user_id)

        if hasattr(self, 'content_widget'):
            self.content_widget.deleteLater()

        self.content_widget = QtWidgets.QWidget(parent=self.groupBox)
        self.content_widget.setStyleSheet("""
            QGroupBox {
                background-color: #D6D1B2;
                border: none;
                border-radius: 5px;
            }
        """)
        self.ticket_frames = []

        scroll = QtWidgets.QScrollArea(self)
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.content_widget)
        scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll.setStyleSheet("""
            QScrollBar:vertical {
                border: none;
                background: #D6D1B2;
                width: 12px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #B0884C;
                min-height: 20px;
                border-radius: 6px;
            }
        """)

        if self.groupBox.layout():
            QtWidgets.QWidget().setLayout(self.groupBox.layout())

        self.groupBox.setLayout(QtWidgets.QVBoxLayout())
        self.groupBox.layout().addWidget(scroll)

        layout = QtWidgets.QVBoxLayout(self.content_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        layout.setSpacing(10)

        for i in self.load_tickets:
            ticket_frame = QtWidgets.QFrame(self.content_widget)
            ticket_frame.setFrameShape(QtWidgets.QFrame.Shape.StyledPanel)
            ticket_frame.setStyleSheet("""
                QFrame {
                    background: #D6D1B2;
                    border: none;  
                    border-radius: 5px;
                    padding: 5px;
                }
            """)
            self.ticket_frames.append(ticket_frame)

            ticket_frame.setProperty('ticket_id', i[0])
            ticket_frame.setObjectName(str(i[0]))

            ticket_frame.setCursor(Qt.CursorShape.PointingHandCursor)
            ticket_frame.mousePressEvent = lambda event, f=ticket_frame, id=i[0]: self.select_ticket(f, id)

            frame_layout = QtWidgets.QVBoxLayout(ticket_frame)
            frame_layout.setContentsMargins(5, 5, 5, 5)

            lb_info = QtWidgets.QLabel(ticket_frame)
            lb_info.setWordWrap(True)
            lb_info.setText(f'Текст заявки: {i[3]}\nСтатус заявки: {i[4]}\nДата и время заявки: {i[5]}')

            frame_layout.addWidget(lb_info)
            layout.addWidget(ticket_frame)

        self.content_widget.setMinimumWidth(620)

        self.btn_insert.clicked.connect(self.add_ticket)
        self.btn_watch.clicked.connect(self.watch_ticket)
        self.btn_delete.clicked.connect(self.delete_ticket)
        self.btn_update.clicked.connect(self.update_ticket)
        self.btn_exit.clicked.connect(self.exit_window)


    def select_ticket(self, frame, ticket_id):
        """Выбор заявки по клику на фрейм, доб обводку"""
        for f in self.ticket_frames:
            f.setStyleSheet("""
                QFrame {
                    background: #D6D1B2;
                    border: none;
                    border-radius: 5px;
                    padding: 5px;
                }
            """)

        frame.setStyleSheet("""
            QFrame {
                background: #D6D1B2;
                border: 2px solid #794E28;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        self.selected_ticket = frame
        self.selected_ticket_id = ticket_id
        print("Выбрана заявка с ID:", self.selected_ticket_id)


    def add_ticket(self):
        """Добавление заявки с последующим обновлением"""
        self.ticket_window = Supp_Window(user_id=self.user_id)
        self.ticket_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
        self.ticket_window.destroyed.connect(self.init_ui)
        self.ticket_window.show()


    def watch_ticket(self):
        """Просмотр заявки, открывается дополнительное окно"""
        if not self.selected_ticket_id:
            QMessageBox.warning(self, "Ошибка", "Выберите заявку для просмотра")
            return
        else:
            id_ticket = self.selected_ticket_id

            self.wch_window = Watch_Window(id_ticket=id_ticket)
            self.wch_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
            self.wch_window.destroyed.connect(self.init_ui)
            self.wch_window.show()


    def delete_ticket(self):
        """Удаление заявки, если статус = в обработке"""
        reply = QMessageBox.question( self, 'Подтверждение',
            'Вы уверены, что хотите удалить эту заявку?',
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        id_ticket = self.selected_ticket_id
        id_user = self.user_id

        if reply == QMessageBox.StandardButton.Yes:
            if delete_ticket(id_ticket, id_user):
                QMessageBox.information(self, "Успех", "Заявка удалена")
                select_tickets_user(self.user_id)
                self.selected_ticket_id = None
                self.init_ui()
        else:
                QMessageBox.warning(self, "Ошибка","Не удалось удалить заявку")


    def update_ticket(self):
        """Изменение заявки, если статус = в ожидании"""
        id_ticket = self.selected_ticket_id
        status = select_status(id_ticket)
        if status == "в ожидании":
            if not self.selected_ticket_id:
                QMessageBox.warning(self, "Ошибка", "Выберите заявку для изменения")
                return
            else:
                self.wch_window = Update_Window(id_ticket=id_ticket)
                self.wch_window.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)
                self.wch_window.destroyed.connect(self.init_ui)
                self.wch_window.show()
        else:
            QMessageBox.warning(self, "Ошибка", "Не удалось загрузить данные заявки или заявка уже обработана")


    def exit_window(self):
        """Закрытие окна"""
        self.close()


if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    wind = User_Window()
    wind.show()
    sys.exit(app.exec())