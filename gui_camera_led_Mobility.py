# -*- coding: utf-8 -*-
"""
Created on Tue Oct 23 15:42:17 2018

@author: lab
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Sep  1 13:47:11 2018
GUI Script for controling Camera and LED
@author: lab
"""


import sys
from PyQt5.QtWidgets import (QMainWindow,QPushButton,QFileDialog, QLabel,
                             QApplication,QMenu, QAction, QLineEdit)
def wf1974():
    import visa
    
    rm = visa.ResourceManager()
    wv = rm.get_instrument("USB0::0x0D4A::0x000E::9137840::INSTR")
    print(wv.query('*IDN?'))
    wv.write(':SOURce1:VOLTage:LEVel:IMMediate:AMPLitude 5.0; OFFSet 2.5')
    wv.write(':SOURce2:VOLTage:LEVel:IMMediate:AMPLitude 5.0; OFFSet 2.5')
    numofpulse=1
    numofpulse=str(numofpulse)
    wv.write(':SOURce1:BURSt:TRIGger:NCYCles '+ numofpulse)#number of cycles output onw
    wv.write(':SOURce2:BURSt:TRIGger:NCYCles '+ numofpulse)#number of cycles output two
    wv.write(':SOURce1:FUNCtion:SHAPe PULSe')
    wv.write(':SOURce2:FUNCtion:SHAPe PULSe')
    wv.write(':TRIGger1:BURSt:SOURce EXT')
    wv.write(':TRIGger2:BURSt:SOURce EXT')
    time =100 # ms
    time = str(time) +"ms"
    wv.write(':SOURce1:PULSe:WIDTh '+ time)#control the pulse width of output one
    wv.write(':SOURce2:PULSe:WIDTh '+ time)#control the pulse width of output two
    wv.write(':SOURce1:PULSe:PERiod 0.15s')#control the pulse period of output1
    wv.write(':SOURce2:PULSe:PERiod 0.15s')#control the pulse period of output2
    wv.write(':SOURce1:BURSt:TGATe:OSTop CYCLe')
    wv.write(':SOURce2:BURSt:TGATe:OSTop CYCLe')
    wv.write('OUTPut1:STATe ON')
    wv.write('OUTPut2:STATe ON')
#    wv.write(':TRIGger1:SEQuence:IMMediate')
#    wv.write(':TRIGger2:SEQuence:IMMediate')
def labsmith_trigger(sender,output):
    import nidaqmx, time
    from datetime import datetime
    from nidaqmx.constants import LineGrouping
    trigger=bool(int(sender))
    print(trigger)
    with nidaqmx.Task () as task:
        task.do_channels.add_do_chan("Dev1/port1/line7",
                                     line_grouping=LineGrouping.CHAN_PER_LINE)
        task.write(trigger,auto_start=True)
    dt=datetime.now()
    output.write('l\t'+
                 str(dt.hour)+ '\t' +
                 str(dt.minute)+ '\t' +
                 str(dt.second)+ '\t' +
                 str(dt.microsecond)+'\n')
    time.sleep(0.1)
def capture(sender,output,wait):
    #print(sender[1])
    import nidaqmx, time
    from nidaqmx.constants import LineGrouping
    from datetime import datetime
    Color=([True,False,False],
           [True,False,True],
           [False,False,True],
           [False,False,False])
    ColorCode='UBGRW'
    import visa
    period = 500# ms 
    #numofpulse=1
    #numofpulse=str(numofpulse)
    
    rm = visa.ResourceManager()
    wv = rm.get_instrument("USB0::0x0D4A::0x000E::9137840::INSTR")
    #print(wv.query('*IDN?'))
    #wv.write(':SOURce1:BURSt:TRIGger:NCYCles '+ numofpulse)
    #wv.write(':SOURce1:PULSe:PERiod 0.5s')
    
    for num in range(5):
        if sender[num] != '':
            period=int(sender[num])
            if period >0:
                #print(period)
                period_s = str(period) +"ms"
                if period > 0 and num <= 3:
                    with nidaqmx.Task () as task:
                        task.do_channels.add_do_chan("Dev1/port1/line0:2",
                                                     line_grouping=LineGrouping.CHAN_PER_LINE)
                        task.write(Color[num],auto_start=True)
                    wv.write(':SOURce1:PULSe:WIDTh '+ period_s)
                    wv.write(':TRIGger1:SEQuence:IMMediate')
                if num == 4:
                    wv.write(':SOURce2:PULSe:WIDTh '+ period_s)
                    wv.write(':TRIGger2:SEQuence:IMMediate')
                dt=datetime.now()
                if output != '':
                    output.write(ColorCode[num]+str(period)+ 'ms\t'+
                                 str(dt.hour)+ '\t' +
                                 str(dt.minute)+ '\t' +
                                 str(dt.second)+ '\t' +
                                 str(dt.microsecond)+'\n')
                time.sleep(wait)
def stage_control(axis,sender):
    import serial
    sender=sender.rstrip("\n")+'\r\n'
    if axis=='s':
        ser = serial.Serial(port='COM7',baudrate=9600, bytesize=8, parity='N', stopbits=1,timeout=1)
    elif axis=='z':
        ser = serial.Serial(port='COM5',baudrate=38400, bytesize=8, parity='N', stopbits=1,timeout=1)
        
    senderbytes=sender.encode('utf-8') 
    ser.write(senderbytes)
    ser.write(b'G:\r\n')
    ser.write(b'!:\r\n')
    stage_status=ser.readline().decode('ascii')
    stage_status=stage_status[0]
    while (stage_status is 'B' or stage_status is 'N'):
        ser.write(b'!:\r\n')
        stage_status=ser.readline().decode('ascii')
        if len(stage_status) <3 :
            stage_status='B'
        else:
            stage_status=stage_status[0]
    ser.close()
    
class Example(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
        
    def initUI(self):

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('File')
        
        impMenu = QAction('read sequence file', self)
        fileMenu.addAction(impMenu)
        impMenu.triggered.connect(self.menuClicked)
        
        btn1 = QPushButton('WF1974', self)
        btn1.move(180, 50) 
        btn1.clicked.connect(self.buttonClicked)
        
        btn3 = QPushButton('Sequence', self)
        btn3.move(180, 130) 
        btn3.clicked.connect(self.buttonClicked)      
        
        btn2 = QPushButton('Snap', self)
        btn2.move(180, 100) 
        btn2.clicked.connect(self.buttonClicked)
        self.qle_UV=QLineEdit(self)
        self.qle_UV.move(70,100)
        lbl_UV = QLabel('UV (ms)', self)
        lbl_UV.move(15, 100)        
#        self.qle_UV.textChanged[str].connect(self.onChanged)

        self.qle_Blue=QLineEdit(self)
        self.qle_Blue.move(70,130)
        lbl_Blue = QLabel('Blue (ms)', self)
        lbl_Blue.move(15, 130)
#        self.qle_Blue.textChanged[str].connect(self.onChanged)

        
        self.qle_Green=QLineEdit(self)
        self.qle_Green.move(70,160)
        lbl_Green = QLabel('Green (ms)', self)
        lbl_Green.move(15, 160)
#        self.qle_Green.textChanged[str].connect(self.onChanged)

        

        self.qle_Red=QLineEdit(self)
        self.qle_Red.move(70,190)
        lbl_Red = QLabel('Red (ms)', self)
        lbl_Red.move(15, 190)     
#        self.qle_Red.textChanged[str].connect(self.onChanged)
        
        self.qle_White=QLineEdit(self)
        self.qle_White.move(70,220)
        lbl_White = QLabel('Bright (ms)', self)
        lbl_White.move(15, 220) 
        
        self.statusBar()
        self.fname='commandlist.txt'
        self.setGeometry(0, 0, 300, 300)        
        self.setWindowTitle('Camera exposure control')
        self.show()
        
        
#    def closeEvent(self, event):
#        
#        reply = QMessageBox.question(self, 'Message',
#            "Are you sure to quit?", QMessageBox.Yes | 
#            QMessageBox.No, QMessageBox.No)
#
#        if reply == QMessageBox.Yes:
#            event.accept()
#        else:
#            event.ignore()        

    def menuClicked(self):
        inputfname = QFileDialog.getOpenFileName(self, 'Open file', '')
        if inputfname: self.fname=inputfname[0]
        print(self.fname)
    def buttonClicked(self):
        sender = self.sender()
        if sender.text() =="WF1974":
            wf1974()
        elif sender.text()=="Snap":
            exposure=[self.qle_UV.text(),
                  self.qle_Blue.text(),
                  self.qle_Green.text(),
                  self.qle_Red.text(),
                  self.qle_White.text()]
            output=''
            capture(exposure,output,0.5)
        elif sender.text()=="Sequence":
            from datetime import datetime
            dt=datetime.now()
            filename=str(dt.year) + '{0:02d}'.format(dt.month)+ '{0:02d}'.format(dt.day)+ \
            '{0:02d}'.format(dt.hour)+ '{0:02d}'.format(dt.minute)+ \
            '{0:02d}'.format(dt.second) + 'exposure.txt'
            print(filename)
            f=open(self.fname, 'r', encoding='utf-8-sig')
            output=open(filename,'w',encoding='utf-8-sig')
            exposure=[self.qle_UV.text(),
                      self.qle_Blue.text(),
                      self.qle_Green.text(),
                      self.qle_Red.text(),
                      self.qle_White.text()]
            for line in f:
                #print (line[0])
                if (line[0] == 's') or (line[0]=='z'):
                    #print(isinstance(line[2:],str))
                    stage_control(line[0],line[2:])
                elif line[0] == 'c':
                    parameter = line.split(",")
                    #print(parameter[1])
                    wait=float(parameter[2].rstrip("\n"))
                    for num in range(int(parameter[1])):
                        capture(exposure, output,wait)
                elif line[0] =='l':
                    labsmith_trigger(line[2:],output)
                    
            f.close()
            output.close()
        #self.statusBar().showMessage(sender.text() + ' was pressed') 
    
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())