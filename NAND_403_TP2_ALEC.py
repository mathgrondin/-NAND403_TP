from PySide6.QtWidgets import QWidget, QLabel, QCheckBox, QVBoxLayout, QPushButton, QMessageBox ,QHBoxLayout, QLineEdit, QFileDialog
from maya import cmds

import json
import random

class MessageBoard(QWidget): 

    def __init__(self):      # Constructeur
        super().__init__() #Constructeur QWidget
        self.setWindowTitle("Programme cool") 
        self.create_ui()

    def create_ui(self):                   

        #region ui setup

        button = QPushButton("Organise Outliner")
        button_browse = QPushButton("Browse")
        layout_main = QVBoxLayout(self)
        label_json = QLabel("Enter Json rule path ")
        self.json_line_edit = QLineEdit()
        self.checkbox_selection = QCheckBox("Apply on selection only")
        self.checkbox_color = QCheckBox("Apply color")
        self.checkbox_reorder = QCheckBox("Apply reorder")
        vertical_box_1 = QVBoxLayout()

        #endregion

        #region vertical box setup
        vertical_box_1.addWidget(label_json)
        vertical_box_1.addWidget(self.json_line_edit)
        vertical_box_1.addWidget(button_browse)
        vertical_box_1.addWidget(self.checkbox_selection)
        vertical_box_1.addWidget(self.checkbox_color)
        vertical_box_1.addWidget(self.checkbox_reorder)
        vertical_box_1.addWidget(button)
        #endregion

        button.pressed.connect(self.on_button_clicked)
        button_browse.pressed.connect(self.on_browse_clicked)
  
        layout_main.addLayout(vertical_box_1)

    def on_browse_clicked(self):           
       
        file_path, _ = QFileDialog.getOpenFileName(self,"Select JSON File") 

        self.json_line_edit.setText(file_path)       

    def on_button_clicked(self):#grosse fonction ici

        self.json_file = self.json_line_edit.text() #variable Json
        
        try: 
          data = open(self.json_file)
          self.fichier_json = json.load(data)
        except:
         print("error")
       

        cmds.undoInfo(openChunk=True) #ctrl z 

        try:

            #region selection

            if self.checkbox_selection.isChecked(): #hardcode prefix
                self.selected_objects = cmds.ls("SM_*", "FX_*", "LGT_*", selection=True)

            else:
            
                self.selected_objects = cmds.ls("SM_*", "FX_*", "LGT_*")

            #endregion

            #region color
            if self.checkbox_color.isChecked():


                for obj in self.selected_objects:  

                 for  prefix in self.fichier_json.keys(): 

                    if obj.startswith(prefix):
                    
                      cmds.setAttr(obj + ".useOutlinerColor", True)
                      cmds.setAttr(obj + ".outlinerColor", self.fichier_json[prefix][0], self.fichier_json[prefix][1], self.fichier_json[prefix][2], type="double3")

        #endregion

            #region reorder    
            if self.checkbox_reorder.isChecked():

                objects = sorted(self.selected_objects)

                for obj in reversed(objects):

                    cmds.reorder(obj, front=True)  
            #endregion

        finally:
            cmds.undoInfo(closeChunk=True) #ctrl z

def main():                      
    
    global widget
    try:
        widget.close()
    except Exception:
        pass

     
    widget = MessageBoard()
    widget.show()
 
main()

