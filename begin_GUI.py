import sys
from PyQt5.QtWidgets import (QWidget, QLabel, QLineEdit, QTextEdit, QGridLayout, QApplication, QPushButton)
import pickle

class Example(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.initUI()
    
    def initUI(self):
        definitions = QLabel('Definitions')
        generalized_coordinate_list = QLabel('Generalized Coordinates')
        coefficent_list = QLabel('Coefficients')
        other_functions = QLabel('Dummie Functions')
        T_replace_dict = QLabel('T Replace Dictionary')
        U_replace_dict = QLabel('U Replace Dictionary')
        T_func_format = QLabel('T Function Format')
        U_func_format = QLabel('U Function Format')
        generalized_coordinate_initial_condition = QLabel('Generalized Coordinate I.C.')
        parameter_initial_condition = QLabel('Parameter I.C.')
        linear = QLabel('Linear')
        t = QLabel('t')

        grid = QGridLayout()
        grid.setSpacing(10)

        self.definitionsText = QTextEdit()
        self.generalized_coordinate_listLine = QLineEdit()
        self.coefficent_listLine = QLineEdit()
        self.other_functionsLine = QLineEdit()
        self.T_replace_dictText = QTextEdit()
        self.T_func_formatText = QTextEdit()
        self.U_replace_dictText = QTextEdit()
        self.U_func_formatText = QTextEdit()
        self.generalized_coordinate_initial_conditionLine = QLineEdit()
        self.parameter_initial_conditionText = QTextEdit()
        self.linearLine = QLineEdit()
        self.tLine = QLineEdit()

        grid.addWidget(generalized_coordinate_list, 1, 0)
        grid.addWidget(self.generalized_coordinate_listLine, 1, 1)

        grid.addWidget(coefficent_list, 2, 0)
        grid.addWidget(self.coefficent_listLine, 2, 1)

        grid.addWidget(definitions, 4, 0)
        grid.addWidget(self.definitionsText, 4, 1, 1, 1)

        grid.addWidget(other_functions, 5, 0)
        grid.addWidget(self.other_functionsLine, 5, 1)

        grid.addWidget(T_replace_dict, 6, 0)
        grid.addWidget(self.T_replace_dictText, 6, 1)

        grid.addWidget(T_func_format, 7, 0)
        grid.addWidget(self.T_func_formatText, 7, 1, 1, 1)

        grid.addWidget(U_replace_dict, 8, 0)
        grid.addWidget(self.U_replace_dictText, 8, 1, 1, 1)

        grid.addWidget(U_func_format, 9, 0)
        grid.addWidget(self.U_func_formatText, 9, 1, 1, 1)

        grid.addWidget(generalized_coordinate_initial_condition, 10, 0)
        grid.addWidget(self.generalized_coordinate_initial_conditionLine, 10, 1)

        grid.addWidget(parameter_initial_condition, 11, 0)
        grid.addWidget(self.parameter_initial_conditionText, 11, 1, 1, 1)

        grid.addWidget(linear, 12, 0)
        grid.addWidget(self.linearLine, 12, 1)

        grid.addWidget(t, 13, 0)
        grid.addWidget(self.tLine, 13, 1)

        start = QPushButton('start')
        abort = QPushButton('abort')
        grid.addWidget(start, 14, 0)
        grid.addWidget(abort, 14, 1)
        start.clicked.connect(self.save)
        
        self.setLayout(grid) 
        
        self.setGeometry(300, 300, 500, 500)
        self.setWindowTitle('Euler-Lagrange ODE Solver')    
        self.show()
    
    def save(self):
        q_str = self.generalized_coordinate_listLine.text()
        coeff_str = self.coefficent_listLine.text()
        other_func_str = self.other_functionsLine.text()
        definitions_str = self.definitionsText.toPlainText()
        T_repalce_dict_str = self.T_replace_dictText.toPlainText()
        T_func_str = self.T_func_formatText.toPlainText()
        U_replace_dict_str = self.U_replace_dictText.toPlainText()
        U_func_str = self.U_func_formatText.toPlainText() 
        q_IC_str = self.generalized_coordinate_initial_conditionLine.text()
        parameter_IC_str = self.parameter_initial_conditionText.toPlainText()
        linear_str = self.linearLine.text()
        t_str = self.tLine.text()

        str_list = [q_str, coeff_str, definitions_str, other_func_str, T_repalce_dict_str, T_func_str, U_replace_dict_str, U_func_str, q_IC_str, 
                    parameter_IC_str, linear_str, t_str]
        
        str_raw = open('str_list.pkl', 'wb')
        pickle.dump(str_list, str_raw)
        
if __name__ == '__main__':
    
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())