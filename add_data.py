    
from PyQt6.QtWidgets import QFileDialog
import myQwindow

def open_file(self):                                        
    self.prog_file = QFileDialog.getOpenFileName(self, "Выберите файл","","Файлы(*.bin)") # выбор файла из окна с фильтром xlsx     
    if  self.prog_file[0]:
        myQwindow.MainWindow.add_item(self,f"Добавлен файл: {self.prog_file[0]}")
    else:
        myQwindow.MainWindow.add_item(self,f"Добавлен файл: Отмена")

def read_file(self):
    try:
        with open(self.prog_file[0], 'rb') as file:
            self.file_content = file.read() # чтение файла прошивки
            self.len_file = len(self.file_content) # длина файла
    except IOError:
        print("Не удалось открыть файл.")