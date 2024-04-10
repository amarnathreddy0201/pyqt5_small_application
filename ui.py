from PyQt5.QtWidgets import QLineEdit,QWidget,QApplication,QVBoxLayout
import sys
from PyQt5.QtCore import pyqtSlot
import ast


class GuiPyqt(QWidget):
    UPDATE_TABLE_COUNT = 0
    def __init__(self):
        QWidget.__init__(self)
        self.setup_ui()
        

    def setup_ui(self):
        self.one_edit=QLineEdit()
        self.two_edit=QLineEdit()
        self.three_edit=QLineEdit()
        self.one_avg=QLineEdit()
        self.one_std=QLineEdit()
        self.two_avg=QLineEdit()
        v_box=QVBoxLayout()
        v_box.addWidget(self.one_edit)
        v_box.addWidget(self.one_avg)
        v_box.addWidget(self.one_std)
        v_box.addWidget(self.two_edit)
        v_box.addWidget(self.two_avg)
        v_box.addWidget(self.three_edit)

        self.setLayout(v_box)

    # def update_label(self,data):
    #     self.one_edit.setText(str(data))
    @pyqtSlot(bytes)
    def send_data_to_ui(self,data):

        dict_str = data.decode("UTF-8")
        mydata = ast.literal_eval(dict_str)
        if "dia" in mydata and bool(mydata["dia"]):
            self.one_edit.setText(str(mydata["dia"]["data"]))
            self.one_avg.setText(str(mydata["dia"]["mean"]))
            self.one_std.setText(str(mydata["dia"]["std"]))


        if "inner" in mydata and bool(mydata["inner"]):
            
            data2=mydata["inner"]
            self.two_edit.setText(str(data2["data"]))
            self.two_avg.setText(str(data2["mean"]))

        if "core" in mydata and bool(mydata["core"]):
            self.three_edit.setText(str(mydata["core"]["data"]))





        