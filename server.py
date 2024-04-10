import threading
from flask import Flask,request
import time
import logging
from ui import GuiPyqt
import sys
from PyQt5.QtWidgets import QApplication
import numpy as np
from PyQt5.QtCore import QObject, QThread, pyqtSignal
import json
import copy


DEVIATION_POINTS_LENGTH=20

logging.basicConfig(
    filename="server.log",
    format="Date-Time : %(asctime)s - %(levelname)s -  Line No. : %(lineno)d - Messages. :%(message)s -Filename: %(filename)s ",
    level=logging.DEBUG,
)
# # Gets or creates a logger
logger = logging.getLogger(__name__)
start=0
j=0
app=Flask(__name__)

import random







class Worker(QObject):
    finished = pyqtSignal()
    progress = pyqtSignal(bytes)
    progress1=pyqtSignal(bytes)

    outer_circular_core_gray_metrics_signal=pyqtSignal(bytes)
    

    def __init__(self, parent=None):
        super(Worker,self).__init__(parent)
        self.body = []
        self.video_streaming_images=None
        self.should_terminate = False
        self.outer_dia_data={}
        self.circular_data={}
        self.core_load_data={}
        self.coreload_spike_data={}
        self.total_data={}

        self.circular_list=[]
        self.outer_dia_list = []
        self.core_list=[]

        app.add_url_rule('/data/', methods=["POST"], view_func=self.handle_update_metrics_request)
        
    def calculate_mean_std_values(self, data):
        return round(np.mean(data), 5), round(np.std(data), 5)

    def conver_data_to_bytes(self, data):
        return json.dumps(data, indent=2).encode("utf-8")
    
        
    def run_in_worker(self):
        
        """Long-running task."""
        # Do my long running task: the flask server.
        
        while not self.should_terminate:
            
            print(self.body)
            if "dia" in self.body and bool(self.body["dia"]):
                outer_dia = self.body["dia"]
                logger.info(outer_dia)
                
                self.outer_dia_data = {
                    "data": outer_dia,
                    "mean":random.randint(1,200),
                    "std":random.randint(1,200)
                    
                }
                logger.info(self.outer_dia_data)

                #Total data in one signal
                self.total_data["dia"] = copy.deepcopy(self.outer_dia_data)
                self.outer_dia_data.clear()
                
            if "inner" in self.body and bool(self.body["inner"]):
                inner_dia = self.body["inner"]

                self.circular_data = {
                    "data": inner_dia,
                    "mean":random.randint(1,200),
                    
                    
                }

                # Data sent in one signal
                self.total_data["inner"] = copy.deepcopy(
                    self.circular_data
                )
                self.circular_data.clear()

            if "core" in self.body:
                
                core_dia_data = self.body["core"]


                self.core_load_data = {
                    "data": core_dia_data,
                    # "mean":random.randint(1,4)
                    
                    
                }

                # Sent data in one signal
                self.total_data["core"] = copy.deepcopy(
                    self.core_load_data
                )
                self.core_load_data.clear()

            if self.total_data:
                user_encode_data = json.dumps(self.total_data, indent=2).encode("utf-8")

                logger.info(user_encode_data)
                self.total_data.clear()
                # one signal
                self.outer_circular_core_gray_metrics_signal.emit(user_encode_data)
        self.finished.emit()
    def handle_update_metrics_request(self):
        if request.method == "POST":
            body = request.json
            self.body = copy.deepcopy(body)
            logger.info(f'Comes here: {body}')
            return "succ"
        
class Server:
    def __init__(self,gui:GuiPyqt):
        self.gui=gui

        # 1. Create a QThread object and connect the flask route listener.
        self.thread = QThread()
        self.worker = Worker()
        #self.worker.progress.connect(self.gui_pyqt.send_data_to_ui)
        
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run_in_worker)
        self.worker.finished.connect(self.thread.quit)
        self.thread.start()
       
        self.worker.outer_circular_core_gray_metrics_signal.connect(self.gui.send_data_to_ui)

        
        threading.Thread(
            target=lambda: app.run(
                host="127.0.0.1",
                port=4004,
                debug=True,
                use_reloader=False,
            )
        ).start()

    

if __name__=="__main__":
    app1 = QApplication(sys.argv)

    #First create the GUI

    gui_pyqt = GuiPyqt()
    #Start the Web Server and associate GUI

    http_flask_server = Server(gui_pyqt)

    #Display the GUI
    gui_pyqt.show()

    sys.exit(app1.exec_())
