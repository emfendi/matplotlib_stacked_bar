from PyQt4.QtGui import *
from PyQt4.QtCore import *
import sys
import os

import stackedGenus 
import biclustering
import pca
from loadData import load_groupData

class CheckBox(QWidget):

    buttonList = []

    def __init__(self, parent = None):
      super(CheckBox, self).__init__(parent)
        
    def create(self) :
        
      layout = QHBoxLayout()
      
      self.btn = []
      for n in range(len(self.buttonList)) :
        self.btn.append(QCheckBox(self.buttonList[n]))
        if n < 2 :
            self.btn[n].setChecked(True)
        self.btn[n].toggled.connect(lambda:self.btnstate(self.btn[n]))
        layout.addWidget(self.btn[n])

      self.setLayout(layout)
      self.setWindowTitle("select two groups")

    def btnstate(self,b):
        for n in range(len(self.buttonList)) :
            if b.text() == self.buttonList[n] :
                if b.isChecked() == True :
                    print b.text()+" is selected"
                else:
                    print b.text()+" is deselected"
    
class MyDialog(QDialog):
    def __init__(self):
        QDialog.__init__(self)
        self.genus_filename = ""
        self.species_filename = ""
        self.group_filename = ""

        # label,Edit,button control        
        lblName = QLabel("Visualization")
        # editName = QLineEdit()
        self.cbo = QComboBox()

        self.cbo.addItem("Stacked Bar")
        self.cbo.addItem("Biclustering")
        self.cbo.addItem("PCA")

        upload_lable = []
        upload_lable.append(QLabel("genus file"))
        upload_lable.append(QLabel("species file"))
        upload_lable.append(QLabel("group file"))
        
        btnUpload = []
        for n in range(3) :
        	btnUpload.append(QPushButton("upload"))
        
       	self.upload_file_name  = []
       	for n in range(3) :
       		self.upload_file_name.append(QLabel("__________________"))
        
        btnOk = QPushButton("OK")
       
        # layout
        self.layout = QGridLayout()
        
        for n in range(3) :
        	self.layout.addWidget(upload_lable[n], n, 0)
        	self.layout.addWidget(self.upload_file_name[n], n, 1)
        	self.layout.addWidget(btnUpload[n], n, 2)
        
        self.layout.addWidget(lblName, 4, 0)
        self.layout.addWidget(self.cbo, 4, 1)
        self.layout.addWidget(btnOk, 4, 2)

        #set layout to dialog
        self.setLayout(self.layout)

        btnUpload[0].clicked.connect(self.btnUploadClicked_genus)
        btnUpload[1].clicked.connect(self.btnUploadClicked_species)
        btnUpload[2].clicked.connect(self.btnUploadClicked_group)
        btnOk.clicked.connect(self.btnOkClicked)

        self.cbo.currentIndexChanged.connect(self.selectionChanged)
    
    #file upload
    def btnUploadClicked_genus(self) :
    	self.genus_filename = QFileDialog.getOpenFileName(self, 'Open File', './data', '(*.csv)')
        filename = os.path.basename(str(self.genus_filename))
        print filename
        self.upload_file_name[0].setText(filename)
        self.setLayout(self.layout)
    def btnUploadClicked_species(self) :
    	self.species_filename = QFileDialog.getOpenFileName(self, 'Open File', './data', '(*.csv)')
        filename = os.path.basename(str(self.species_filename))
        print filename
        self.upload_file_name[1].setText(filename)
        self.setLayout(self.layout)
    def btnUploadClicked_group(self) :
    	self.group_filename = QFileDialog.getOpenFileName(self, 'Open File', './data', '(*.csv)')
        filename = os.path.basename(str(self.group_filename))
        print filename
        self.upload_file_name[2].setText(filename)
        self.setLayout(self.layout)

    #biclustering needs 2 groups
    def selectionChanged(self):
        idx = self.cbo.currentIndex()
        if idx == 1 :
            ex = CheckBox()
            x, ex.buttonList = load_groupData(self.group_filename)
            ex.create()
            ex.show()

    def btnOkClicked(self):
	    txt = self.cbo.currentText()
	    idx = self.cbo.currentIndex()
        
	    if idx == 0 : #Stacked Bar
	    	stackedGenus.run(self.genus_filename, self.species_filename)
	    elif idx == 1 : #Biclustering
	    	biclustering.run(self.genus_filename, self.group_filename)
	    elif idx ==2 : #PCA
	    	pca.run(self.genus_filename, self.group_filename)
	    else :
			QMessageBox.information(self, "Info", "ERROR")


# App
app = QApplication([])
dialog = MyDialog()
dialog.show()
app.exec_()