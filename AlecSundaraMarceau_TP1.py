# correction
import sys 
from PySide6.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QPushButton, QLineEdit,  QMessageBox
import json
from pathlib import Path
from PySide6.QtCore import Qt

# setup

#pour runner en terminal sur mon ordi a maison :    cd "C:\Users\A\Documents\repo\Alec_Sundara_Marceau_TP1"
#                                                   python .\AlecSundaraMarceau_TP1.py data_large.json


app = QApplication(sys.argv) 

class MainWindow(QMainWindow):        
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My App")

        self.ref_tableau = get_tableau()
        self.ref_fichier, ref_taille, ref_nb_elements = get_file_info()

        # Search bar
        search_bar = QLineEdit()
        search_bar.textChanged.connect(self.search_text)

        search_result = QLabel("search_result : ")   

        verticle_box = QVBoxLayout()
        verticle_box.addWidget(search_bar)  
        verticle_box.addWidget(search_result)  
        verticle_box.addWidget(self.ref_tableau)
        verticle_box.addWidget(self.ref_fichier)
        verticle_box.addWidget(ref_taille)
        verticle_box.addWidget(ref_nb_elements)
        main_widget = QWidget()
        main_widget.setLayout(verticle_box)
        self.setCentralWidget(main_widget) 

    def search_text(self, search_for): #dois faire ca car le connect est dans la classe,sinon on a pas acces au texte entrer
        row_count = self.ref_tableau.rowCount()
        column_count = self.ref_tableau.columnCount()

        

        for i in range(row_count):
            for j in range(column_count):

                 self.ref_tableau.setRowHidden(i,True)

            #accede au texte a linterieur de la case
                 item = self.ref_tableau.item(i,j) #stock la position case
                 text_case = item.text()        #stock le texte

                 
                 if search_for in text_case: #si le text est dans la case 
                       self.ref_tableau.setRowHidden(i, False) #cache cette case
                       break #arrete la loop sinon il cache tout
                        
def get_file_info():                  
    path = get_json_path()
    fichier_json = get_json()

    nom_fichier = QLabel("Nom : " + path.name)
    taille_fichier = QLabel("Taille : " + str(path.stat().st_size) + " octets")
    nb_elements = QLabel("Nombre d'éléments : " + str(len(fichier_json))) 

    return (nom_fichier, taille_fichier, nb_elements)
       
def get_tableau():                    
    tableau = QTableWidget() 
    ref_fichier_json = get_json()
    ref_header_labels = get_json_keys()

    row_count = (len(ref_fichier_json))
    column_count = (len(ref_header_labels))

    tableau.setColumnCount(column_count)
    tableau.setRowCount(row_count)
    tableau.setHorizontalHeaderLabels(ref_header_labels)
    tableau.setSortingEnabled(True)

    #remplir tableau

    for row, value in enumerate(ref_fichier_json):

        for column, keys in enumerate(ref_header_labels):

            test = value[keys]

            tableau.setItem(row,column, QTableWidgetItem(str(test)))


    return tableau

def get_json_path():                  
     path = Path(sys.argv[1])
     #path = Path(__file__).parent / "data_large.json" hardcode

     return (path)
        
def get_json_keys():                  
    

    ref_json = get_json()

    # header_labels = []
    
    # for object in ref_json:
    #     for key in object:
    #         if (key not in header_labels):
    #             header_labels.append(key)
    #         else:
    #            break

    header_labels = list(ref_json[0].keys())
    return header_labels

def get_json():                       

    error_box = QMessageBox()
    error_box.setWindowTitle("Error")
    error_box.setText("Erreur dans le fichier .json")

   # path = Path(__file__).parent / "data_large.json" #hardcode

    
    json_file = sys.argv[1]

    try: 
        data = open(json_file)
        fichier_json = json.load(data)
    except:
        print("error")


    # try:
    #     with path.open("r", encoding="utf-8") as fichier:
    #         fichier_json = json.load(fichier) 

    # except json.JSONDecodeError:

    #     error_box.exec()


    return (fichier_json)

def run_app():                        
    
    window = MainWindow() 
    window.show()

    app.exec()

def debug():                          
    print("habibi!")

run_app()


