from PyQt6.QtWidgets import QPushButton

class MyButton(QPushButton):
    def __init__(self, str, parent=None, clicked = None, state = False):
        super().__init__(str, parent)
        self.state = state
        if clicked:
            self.clicked.connect(clicked)
        self.button_state()
    def button_state(self):                       # состояние кнопки
        self.setEnabled(self.state)
        if self.state:
            set_style(self,"#78909C","#263238","bold")     # активная кнопка
        else:
            set_style(self,"#78909C","grey","Verdana")      # неактивная кнопка
    
    def update_state(self, newstate):
        self.state = newstate
        self.button_state()
 

def set_style(obj,bcolor,color,font):   # изменить дизайн обекта
        obj.setStyleSheet(f"""
            background-color: {bcolor};
            color: {color};
            font: {font};
        """)