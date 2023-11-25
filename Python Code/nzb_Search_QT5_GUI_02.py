from pickle import FALSE
from PyQt5.QtWidgets import *
from PyQt5 import uic
from nzb_search_db_connection import nzb_search_connection
from nzb_search import nzb_search_helper
import logging

class MyGUI(QMainWindow):
    
    def __init__(self):
            super(MyGUI, self).__init__()
            # uic.loadUi(r"c:\Users\latto\OneDrive\DEV\NZB Search\nzb-search\Python Code\BroUI.ui", self)
            uic.loadUi(r"C:\Projects\nzb-search\Python Code\\BroUI.ui", self)
            self.show()

            self.cls_nzb = nzb_search_helper()

            # Get data from database
            self.sql = "SELECT ID, description from movies where ID<1000;"
            self.cls_db_connection = nzb_search_connection(1)
            self.conn = self.cls_db_connection.create_connection()
            self.cur = self.conn.cursor()
            self.cur.execute(self.sql)
            self.rows = self.cur.fetchall()
            print("Number of rows: " + str(self.cur.rowcount))
            #print("Number of columns: " + str(cur))

            # Need to declare variables so IDE can get methods/attributes/etc. for the design elements in the UI file.
            # Ideally, will need one line per element on the UI design.
            self.pushButton = self.findChild(QPushButton, "pushButton")
            self.lineEdit = self.findChild(QLineEdit, "lineEdit")
            self.pushButton_2 = self.findChild(QPushButton, "pushButton_2")
            self.textEdit = self.findChild(QTextEdit, "textEdit")
            self.tableWidget = self.findChild(QTableWidget, "tableWidget")
            self.pushButton_Run_Main = self.findChild(QPushButton, "pushButton_Run_Main")
            self.textEdit_status = self.findChild(QTextEdit, "textEdit_status")
            #self.textEdit_status.setAcceptRichText(False) #QTextEdit by default accepts rich text. Need to use this line to only accept text.
            self.pushButton_write_to_textedit = self.findChild(QPushButton, "pushButton_write_to_textedit")
            self.lineEdit_textbox_string = self.findChild(QLineEdit, "lineEdit_textbox_string")
            self.pushButton_clear_textbox_string = self.findChild(QPushButton, "pushButton_clear_textbox_string")
            self.pushButton_get_value_from_table = self.findChild(QPushButton, "pushButton_get_value_from_table")
            self.listWidget_movie_type = self.findChild(QListWidget, "listWidget_movie_type")
            self.pushButton_reload_table = self.findChild(QPushButton, "pushButton_reload_table")
            self.lineEdit_date = self.findChild(QLineEdit, "lineEdit_date")
            self.lineEdit_sid = self.findChild(QLineEdit, "lineEdit_sid")
            self.tableWidget_file_password = self.findChild(QTableWidget, "tableWidget_file_password")
            self.pushButton_load_password = self.findChild(QPushButton, "pushButton_load_password")
            self.pushButton_save_params = self.findChild(QPushButton, "pushButton_save_params")
            self.pushButton_get_value_list_widget = self.findChild(QPushButton, "pushButton_get_value_list_widget")
            self.tableWidget_bus_exp = self.findChild(QTableWidget, "tableWidget_bus_exp")
            self.pushButton_status_clear = self.findChild(QPushButton, "pushButton_status_clear")
            self.tableWidget_nzb_series = self.findChild(QTableWidget, "tableWidget_nzb_series")
            self.pushButton_nzb_series = self.findChild(QPushButton, "pushButton_nzb_series")
            self.pushButton_nzb_series_clear = self.findChild(QPushButton, "pushButton_nzb_series_clear")

            self.tableWidget_file_password.verticalHeader().setVisible(False)

            self.lineEdit_date.setText("2022-09-19")
            self.lineEdit_sid.setText("1")

            #
            # QTableWidget code to load table, set column/row appearance, etc.
            #
            # Initialize the table with zero rows. When iterating through rows, rows will be added as necessary.
            self.tableWidget.setRowCount(0)

            # Set column row initial width, in pixels. Note, the width is still user adjustable.
            self.tableWidget.setColumnWidth(0,0)
            self.tableWidget.setColumnWidth(1,800)
            
            # Iterate through all rows, and then through all columns in that row
            for row_number, row_data in enumerate(self.rows):
                self.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

            # Assign pushButton events to functions:
            self.pushButton.clicked.connect(self.login)
            self.pushButton_2.clicked.connect(lambda: self.say_it(self.textEdit.toPlainText())) # Notice the lambda function when an argument is needed.
            self.pushButton_Run_Main.clicked.connect(self.nzb_search_main)
            self.pushButton_write_to_textedit.clicked.connect(self.dev_write_to_textedit)
            self.pushButton_clear_textbox_string.clicked.connect(self.clear_input_string)
            self.pushButton_reload_table.clicked.connect(self.reload_table)
            self.pushButton_load_password.clicked.connect(self.load_password_table)
            self.pushButton_save_params.clicked.connect(self.update_params)
            self.pushButton_get_value_list_widget.clicked.connect(self.print_movie_list_to_status)
            self.pushButton_status_clear.clicked.connect(self.clear_status_text)
            self.pushButton_nzb_series.clicked.connect(self.load_nzb_series)
            self.pushButton_nzb_series_clear.clicked.connect(self.clear_nzb_series)

            self.load_business_test()

    def bro_function(self):
        pass

    def clear_nzb_series(self):
        self.tableWidget_nzb_series.setRowCount(0)

    def load_nzb_series(self):
        date = self.lineEdit_date.text()
        sid = self.lineEdit_sid.text()
        
        # Get data from database
        sql = "SELECT ID, download_date, series_id, description, filename, password, note, nzb_created, nzb_exception, dl_comments, movie_url, movie_type FROM movies WHERE download_date = '" + date + "' AND series_id = " + sid + ";"
        cls_db_connection = nzb_search_connection(1)
        conn = cls_db_connection.create_connection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print("Number of Rows in Series: " + str(cur.rowcount))

        for row_number, row_data in enumerate(rows):
            self.tableWidget_nzb_series.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_nzb_series.setItem(row_number, column_number, QTableWidgetItem(str(data)))
        
    
    def print_movie_list_to_status(self):
        row = self.listWidget_movie_type.currentRow()
        # selection = self.listWidget_movie_type.item(row).text()
        selection = self.listWidget_movie_type.currentItem().text()
        print("List Box Selection: " + str(selection))
        self.textEdit_status.setPlainText(selection)
    
    def login(self):
        if self.lineEdit.text() == "Bro" and self.lineEdit_2.text() == "pw":
            self.textEdit.setEnabled(True)
            self.pushButton_2.setEnabled(True)
        else:
            message = QMessageBox()
            message.setText("Invalid")
            message.exec_()

    def reload_table(self):
        # Load table widget by interating through i) all rows; ii) all columns in each row
        # Note: make sure 'rows' variable has the data needed to the table to be loaded, may have to make a 
        # new connection and/or cursor for the data.
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(self.rows):
            self.tableWidget.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

    def load_combo_box(self):
        pass

    def load_password_table(self):
        string_password = ""
        self.tableWidget_file_password.setColumnWidth(0,50)
        self.tableWidget_file_password.setColumnWidth(1,150)
        self.tableWidget_file_password.setColumnWidth(2,150)
        date = self.lineEdit_date.text()
        series_id = self.lineEdit_sid.text()
        if date == '':
            message = QMessageBox()
            message.setText("Please enter in a date in teh following format: yyyy-mm-dd")
            message.exec_()
            return
        else:
            if series_id == '':
                message = QMessageBox()
                message.setText("Please enter in a series_id.")
                message.exec_()
                return
            
        sql = "select series_id, filename, password from movies where download_date='" + date + "' and series_id = " + series_id + " and nzb_created is null and nzb_exception is null; "
        print("Password query:" + "\n" + sql)
        rows = self.cur
        self.cur.execute(sql)
        rows = self.cur.fetchall()
        print("Number of rows in password query: " + str(self.cur.rowcount)) 
        self.tableWidget_file_password.setRowCount(0)
        for row_number, row_data in enumerate(rows):
            self.tableWidget_file_password.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_file_password.setItem(row_number, column_number, QTableWidgetItem(str(data)))

        self.password_to_status()

    def password_to_status(self):
        string_password_list = ""
        i = 0
        while i < self.tableWidget_file_password.rowCount():
            print(str(i) + ") First row pw value: " + self.tableWidget_file_password.item(i,1).text())
            if string_password_list == "":
                string_password_list = self.lineEdit_date.text() + " " + self.lineEdit_sid.text() + " Password List: " + "\n" + self.tableWidget_file_password.item(i,1).text() + ", " + self.tableWidget_file_password.item(i,2).text()
            else:
                string_password_list = string_password_list + "\n" + self.tableWidget_file_password.item(i,1).text() + ", " + self.tableWidget_file_password.item(i,2).text()
            i += 1
        string_password_list = self.textEdit_status.toPlainText() + "\n" + string_password_list
        self.textEdit_status.setPlainText(string_password_list)

    def clear_status_text(self):
        self.textEdit_status.setText("")

    def clear_input_string(self):
        text = ""
        self.lineEdit_textbox_string.setText(text)
    
    def say_it(self, msg):
        message = QMessageBox()
        message.setText(msg)
        message.exec_()

    def write_status(self, status_text):
        status_text = "Bro"
        
    def print_status_content(self):
        text = self.textEdit_status.toPlainText()
        print("Text Box Contents: " + text)

    def nzb_search_main(self):
        # Get data from database
        # self.sql = "SELECT ID, description from movies where ID<1000;"
        cls_nzb = nzb_search_helper()
        cls_db_connection = nzb_search_connection(1)
        conn = cls_db_connection.create_connection()
        cur = conn.cursor()
        #self.cur.execute(self.sql)
        #self.rows = self.cur.fetchall()
        #print("Number of rows: " + str(self.cur.rowcount))
        #print("Number of columns: " + str(cur))
        
        # Database stuff
        self.update_params()
        cls_nzb.select_all_movies()
        self.print_status_content()
        self.textEdit_status.setPlainText("This is a test")

    def update_params(self):
        date = self.lineEdit_date.text()
        sid = self.lineEdit_sid.text()
        sql_update_db_date = "UPDATE app_parameters SET param_value = '" + date + "' WHERE ID = 1;"
        sql_update_db_sid = "UPDATE app_parameters SET param_value = '" + sid + "' WHERE ID = 2;"

        db_connection = nzb_search_connection(1)
        conn = self.cls_db_connection.create_connection()
        cur1 = self.conn.cursor()
        cur2 = self.conn.cursor()
        cur1.execute(sql_update_db_date)
        cur2.execute(sql_update_db_sid)
        self.conn.commit()

    def dev_write_to_textedit(self):
        old_text = self.textEdit_status.toPlainText()
        if old_text == "":
            new_text = self.lineEdit_textbox_string.text()
        else:
            new_text = old_text + "\n" +self.lineEdit_textbox_string.text()
        self.textEdit_status.setPlainText(new_text)

    def load_business_test(self):
        # Get data from database
        sql = "SELECT * FROM Expenses;"
        cls_db_connection = nzb_search_connection(3)
        conn = cls_db_connection.create_connection()
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print("Number of Business rows: " + str(cur.rowcount))

        for row_number, row_data in enumerate(rows):
            self.tableWidget_bus_exp.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.tableWidget_bus_exp.setItem(row_number, column_number, QTableWidgetItem(str(data)))

def main():
    app = QApplication([])
    window = MyGUI()
    app.exec_()

if __name__ == '__main__':
    main()