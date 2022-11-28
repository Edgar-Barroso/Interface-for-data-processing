import sys
import pandas as pd
import sklearn
from sklearn.preprocessing import StandardScaler,OneHotEncoder
from sklearn.compose import ColumnTransformer
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QTableWidgetItem, QHeaderView, QLineEdit, \
                            QPushButton, QMainWindow, QGridLayout,QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QDoubleValidator

with open('botao.css','r',encoding='utf-8') as f:
    botao_css = f.read()

class Janela(QMainWindow):
    def __init__(self,df) -> None:
        super().__init__()
        self.esquerda = 250
        self.topo = 100
        self.largura = 1000
        self.altura = 600
        self.titulo = 'APP'
        self.cw = QWidget()
        self.cw.setStyleSheet('QWidget {background: #D2CDE0}')
        self.grid = QGridLayout(self.cw)
        
        self.tabela = TableWidget(df)
        self.setCentralWidget(self.cw)
        self.tabela.setStyleSheet('TableWidget {background: #FFFFFF}')
        self.grid.addWidget(self.tabela,0,0,1,4)

        button_aplic = QPushButton('Aplicar e Salvar')
        button_aplic.setFixedWidth(250)
        button_aplic.setStyleSheet('QPushButton {background:#56BD33}')
        button_aplic.clicked.connect(self.aplicar_salvar)
        self.grid.addWidget(button_aplic,1,0,1,1)

        self.button_excluir = QPushButton('Excluir colunas')
        self.button_excluir.setStyleSheet('QPushButton {background:#BD3333}')
        self.button_excluir.setFixedWidth(250)
        self.button_excluir.clicked.connect(self.excluir)
        self.grid.addWidget(self.button_excluir,1,3,1,1)

        self.button_onehot = QLabel('OneHotEncoder :')
        self.button_onehot.setFixedWidth(250)
        self.button_onehot.setStyleSheet(f'QLabel {botao_css}')
        self.grid.addWidget(self.button_onehot,2,0,1,1)

        self.button_scaler = QLabel('StandardScaler :')
        self.button_scaler.setFixedWidth(250)
        self.button_scaler.setStyleSheet(f'QLabel {botao_css}')
        self.grid.addWidget(self.button_scaler,3,0,1,1)


        self.qline_colunas_excluir = QLineEdit()
        self.qline_colunas_excluir.setFixedWidth(250)
        self.qline_colunas_excluir.setStyleSheet(f'QLineEdit {botao_css}')
        self.grid.addWidget(self.qline_colunas_excluir,2,3,1,1)


        self.qline_colunas_onehot = QLineEdit()
        self.qline_colunas_onehot.setFixedWidth(250)
        self.qline_colunas_onehot.setStyleSheet(f'QLineEdit {botao_css}')
        self.grid.addWidget(self.qline_colunas_onehot,2,1,1,1)


        self.qline_colunas_scaler = QLineEdit('all columns')
        self.qline_colunas_scaler.setDisabled(True)
        self.qline_colunas_scaler.setFixedWidth(250)
        self.qline_colunas_scaler.setStyleSheet(f'QLineEdit {botao_css}')
        self.grid.addWidget(self.qline_colunas_scaler,3,1,1,1)


        self.qline_colunas_arq = QLineEdit('arquivo_de_saida.csv')
        self.qline_colunas_arq.setFixedWidth(250)
        self.qline_colunas_arq.setStyleSheet(f'QLineEdit {botao_css}')
        self.grid.addWidget(self.qline_colunas_arq,1,1,1,1)


        self.grid.addWidget(QLabel('ex: dataframe.csv'),1,2,1,1)
        self.grid.addWidget(QLabel('ex: 0,1,2'),3,3,1,1)
        self.grid.addWidget(QLabel('ex: 0,1,2'),2,2,1,1)


        self.carregarJanela()

    def carregarJanela(self):
        self.setGeometry(self.esquerda,self.topo,self.largura,self.altura)
        self.setWindowTitle(self.titulo)
        self.show()
    

    def excluir(self):
        colunas_excluir = [int(i) for i in self.qline_colunas_excluir.text().split(',')]
        self.tabela.df.drop(self.tabela.df.columns[colunas_excluir],axis=1,inplace=True)
        self.qline_colunas_excluir.setText('')
        self.tabela.atualizar()

    def aplicar_salvar(self):
        data = self.tabela.df.values
        try:
            colunas = [int(i) for i in self.qline_colunas_onehot.text().split(',')]
            onehotencoder = ColumnTransformer(transformers=[('OneHot', OneHotEncoder(), colunas)], remainder='passthrough')
            data = onehotencoder.fit_transform(data)
            self.qline_colunas_onehot.setText('')
            try:
                data=data.toarray()
            except:
                pass
        except:
            pass
        try:
            scaler = StandardScaler()
            data = scaler.fit_transform(data)
        except:
            pass
        dataframe = pd.DataFrame(data)
        dataframe.to_csv(self.qline_colunas_arq.text())
        self.tabela.df = self.tabela.df0
        self.tabela.atualizar()
        

class TableWidget(QTableWidget):
    def __init__(self, df):
        super().__init__()
        self.df0= df[:]
        self.df = df
        self.setGeometry(0,0,500,500)
        self.setStyleSheet('font-size: 15px;')

        self.atualizar()

    def atualizar(self):
        nRows, nColumns = self.df.shape
        self.setColumnCount(nColumns)
        self.setRowCount(nRows)
        self.setHorizontalHeaderLabels(self.df.columns)
        self.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        for i in range(self.rowCount()):
            for j in range(self.columnCount()):
                self.setItem(i, j, QTableWidgetItem(str(self.df.iloc[i, j])))


if __name__ == '__main__':
    dataset = pd.read_csv('Data export.csv')
    aplicacao = QApplication(sys.argv)
    j = Janela(dataset)
    sys.exit(aplicacao.exec_())
