from PyQt6.QtWidgets import QMainWindow, QWidget,QVBoxLayout,QGridLayout,QListWidget,QProgressBar 
from PyQt6.QtCore import QSize,QElapsedTimer
from PyQt6.QtGui import QIcon,QPixmap
import add_data
import myQbutton
import myThread
import myHID


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.prog_file = ('','')
        self.file_content = None # файл прошивки в формате bytes
        self.len_file = 0        # размер прошивки в байтах
        vid = 1155               # значениие по умолчанию для STM устройств
        pid = 22352              # значениие по умолчанию для STM устройств
        self.myDevice = None     # подключенное устройство
        # self.progress = 0      # проверить нужен ли вообще!!!
        self.list_content = None
        self.file_list = None    # файла прошивки преобразованый в массив по 65 значений в каждой строке
        self.rowItem = 0         # номер последней строки QListWidget
        
        my_thread = myThread.loadThread(self)
        my_thread.finished.connect(lambda: (self.update_progress_bar(int(self.len_file)), # при завершении потока обнавить загрузочную чтроку до 100%
                                            self.timer.invalidate(), # выелючить таймер
                                            self.add_item(str(self.timer.elapsed()/10000000)+" sec"), # вывести время прошивки в sec 
                                            self.add_item("__END__"))) 
        my_thread.progress_signal.connect(self.update_progress_bar) # сигнал обнавления загрузочной строки во время выполнения потока

        self.timer = QElapsedTimer() # обект таймера
    
        central_widget = QWidget() # главное окно
        self.setCentralWidget(central_widget) 
        set_style(central_widget,"#78909C","white","Verdana") # цвет фона, цвет текста, шрифт главного окна
        self.setWindowTitle("USB Bootloader") # заголовок
        
        pixmap = QPixmap("icon.png") # добавление иконки на титульную полоску
        icon = QIcon(pixmap) 
        self.setWindowIcon(icon)

        layout = QVBoxLayout(central_widget)
        self.setFixedSize(QSize(400, 300)) # размер главного окна
        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)

        self.button_file = myQbutton.MyButton("Open file...",self,state=True,
                                              clicked=lambda:(add_data.open_file(self), # открытие файла прошивки
                                                              add_data.read_file(self) if self.prog_file else None, # сохранить содержимое прошивки в перемнную
                                                              self.loadingBar.setRange(0,int(self.len_file)), # задать диапазон значений для полоски загрузки
                                                              self.button_device.update_state(True) if self.prog_file[0] else False )) # разблокировать кнопку "Connect"
        grid_layout.addWidget(self.button_file,1,0) # положение кнопки в сетке

        self.button_device = myQbutton.MyButton("Connect...",self,state=False,
                                                clicked=lambda:(myHID.connect(vid,pid,self), # подключиться к устройству
                                                                self.add_item(self.myDevice.product) if self.myDevice else None, # вывести имя подключенного устройства
                                                                self.bytes_to_list() if self.myDevice else None, # преобразовать данные прошивки для отправки по USB
                                                                self.program_file.update_state(True) if self.myDevice else None)) # разблокировать кнопку "Program"
        grid_layout.addWidget(self.button_device,1,1) # положение кнопки в сетке

        self.program_file = myQbutton.MyButton("Program...",self,clicked=lambda:(my_thread.start(), # при нажатии кнопки запустить новый поток
                                                                                 self.timer.start()),# запуск таймера
                                                                                 state=False) # по умолчанию кнопка не активна
        grid_layout.addWidget(self.program_file,2,0) # положение кнопки в сетке
        
        self.loadingBar = QProgressBar()
        grid_layout.addWidget(self.loadingBar,3,0,4,0) # положение загрузочной полоски по всей ширине
        self.loadingBar.setRange(0,int(self.len_file)) # установить диапазон загрузочной полоски
        set_style(self.loadingBar,"#B0BEC5","#1B4F72","italic") 

        self.notification_list_widget = QListWidget() # создание списка
        layout.addWidget(self.notification_list_widget)
        set_style(self.notification_list_widget,"#B0BEC5","#1B4F72","italic")

    def add_item(self, str):                        # добавить текст в список
        self.notification_list_widget.addItem(str)
        self.rowItem+=1
    def del_item(self):                        # удалить последняя значение в списоке
        self.notification_list_widget.takeItem(self.rowItem)
        self.rowItem-=1
    
    def bytes_to_list(self):
        file_list_bytes = list(self.file_content) # преобразование bytes в list
        self.file_list = [file_list_bytes[i:i+64] for i in range(0, self.len_file, 64)] # разбить на массив по 64 значения в строке  
        size64 = len(self.file_list) # количество строк
        for i in range(size64):
            self.file_list[i].insert(0, 0) # добавить в начало строки байт для отправки USB HID ID
    def update_progress_bar(self, value): # обнавить строку загрузки новым значением
        self.loadingBar.setValue(value)

def set_style(obj,bcolor,color,font):   # изменить дизайн обекта
        obj.setStyleSheet(f"""
            background-color: {bcolor};
            color: {color};
            font: {font};
        """)





        