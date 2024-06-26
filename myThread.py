from PyQt6.QtCore import QThread, pyqtSignal
import myHID
class loadThread(QThread):
    finished = pyqtSignal()  # сигнал о завершении потока
    progress_signal = pyqtSignal(int) # сигнал обнавления загрузочной строки
    def __init__(self,obj):
        super().__init__()
        self.obj = obj # передать в поток обект MainWindow
        
    def run(self):
        '''выполняется в отдельном потоке'''
        myHID.send_bin(self)                    # передача прошивки на устройство
        self.finished.emit()                    # отправляем сигнал о завершении
