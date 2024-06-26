from PyQt6.QtWidgets import QApplication
import sys
import myQwindow

app = QApplication(sys.argv)
app.setStyle("Fusion")
window =  myQwindow.MainWindow()
window.show()
app.exec() 
