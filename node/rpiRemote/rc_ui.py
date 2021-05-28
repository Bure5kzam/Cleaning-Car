from PyQt5.QtWidgets import * 
from PyQt5.uic import * 
from PyQt5.QtCore import * 
from PyQt5 import QtSql 

class MyApp(QMainWindow): 
    def __init__(self): 
        super().__init__() 
        loadUi("rc_ui.ui", self) 
         
        self.db = QtSql.QSqlDatabase.addDatabase('QMYSQL') 
        self.db.setHostName("3.35.8.78")         
        self.db.setDatabaseName("DB_15_04") 
        self.db.setUserName("SSAFY15_04_2") 
        self.db.setPassword("1234") 

        ok = self.db.open() 
        if not ok: print(self.db.lastError().text())      

        self.query = QtSql.QSqlQuery() 
        self.timer = QTimer() 
        self.timer.setInterval(100) 
        self.timer.timeout.connect(self.pollingQuery) 
        self.timer.start() 
        self.auto = 0

    def pollingQuery(self): 
        self.query = QtSql.QSqlQuery("select * from command_02"); 
        self.text.clear() 
        while (self.query.next()): 
            self.record = self.query.record() 
            str = "%s | %10s | %10s | %4d" % (self.record.value(0).toString(), self.record.value(1), self.record.value(2), self.record.value(3)) 
            self.text.appendPlainText(str) 

    def commandQuery(self, cmd, arg): 
        self.query.prepare("insert into command_02 (time, cmd_string, arg_string, is_finish) values (:time, :cmd, :arg, :finish)"); 
        time = QDateTime().currentDateTime() 
        self.query.bindValue(":time", time) 
        self.query.bindValue(":cmd", cmd) 
        self.query.bindValue(":arg", arg) 
        self.query.bindValue(":finish", 0) 
        self.query.exec() 

    def clickedRight(self): 
        self.query.prepare("insert into command_02 (time, cmd_string, arg_string, is_finish) values (:time, :cmd, :arg, :finish)"); 
        time = QDateTime().currentDateTime() 
        self.query.bindValue(":time", time) 
        self.query.bindValue(":cmd", "right") 
        self.query.bindValue(":arg", "1 sec") 
        self.query.bindValue(":finish", 0) 
        self.query.exec() 

    def clickedRight(self): 
        self.commandQuery("right", "1 sec")     
    def clickedLeft(self): 
        self.commandQuery("left", "1 sec") 
    def clickedGo(self): 
        self.commandQuery("go", "1 sec") 
    def clickedBack(self): 
        self.commandQuery("back", "1 sec")     
    def clickedMid(self): 
        self.commandQuery("mid", "1 sec") 
    def toggleAuto(self) :
        if self.auto == 0 :
            self.auto = 1
            self.commandQuery("auto_on", "1 sec") 
        else :
            self.auto = 0
            self.commandQuery("auto_off", "1 sec")
         
app = QApplication([]) 
win = MyApp() 
win.show() 
app.exec()