# ui_main_window.py

import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QComboBox, QFileDialog
)
from googletrans import LANGUAGES

# A classe que define a interface.
class TradutorPDFApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Tradutor de PDF")
        self.setGeometry(100, 100, 600, 350)
        self.setFixedSize(600, 350)

        # --- Layouts ---
        layout_principal = QVBoxLayout(self)
        layout_principal.setContentsMargins(40, 40, 40, 40)
        layout_principal.setSpacing(15)
        layout_arquivo = QHBoxLayout()
        layout_idiomas = QHBoxLayout()

        # --- Widgets (Componentes) ---
        label_anexar = QLabel("Selecione o arquivo PDF:")
        self.caminho_arquivo_edit = QLineEdit()
        self.caminho_arquivo_edit.setPlaceholderText("Nenhum arquivo selecionado...")
        self.caminho_arquivo_edit.setReadOnly(True)
        self.botao_anexar = QPushButton("Anexar")
        layout_arquivo.addWidget(self.caminho_arquivo_edit)
        layout_arquivo.addWidget(self.botao_anexar)

        label_idioma_origem = QLabel("Idioma Original:")
        self.combo_idioma_origem = QComboBox()
        label_idioma_destino = QLabel("Idioma de Destino:")
        self.combo_idioma_destino = QComboBox()
        layout_origem = QVBoxLayout()
        layout_origem.addWidget(label_idioma_origem)
        layout_origem.addWidget(self.combo_idioma_origem)
        layout_destino = QVBoxLayout()
        layout_destino.addWidget(label_idioma_destino)
        layout_destino.addWidget(self.combo_idioma_destino)
        layout_idiomas.addLayout(layout_origem)
        layout_idiomas.addLayout(layout_destino)

        self.botao_traduzir = QPushButton("Traduzir PDF")
        self.botao_traduzir.setFixedHeight(40)

        # --- Conectando os Sinais ---
        self.botao_anexar.clicked.connect(self.abrir_seletor_de_arquivo)

        # --- Populando os ComboBox de Idiomas ---
        self.popular_idiomas()

        # --- Montando a Interface ---
        layout_principal.addWidget(label_anexar)
        layout_principal.addLayout(layout_arquivo)
        layout_principal.addLayout(layout_idiomas)
        layout_principal.addStretch()
        layout_principal.addWidget(self.botao_traduzir)

        self.aplicar_estilo()

    def popular_idiomas(self):
        nomes_idiomas = [lang.capitalize() for lang in LANGUAGES.values()]
        self.combo_idioma_origem.addItem("Detectar Automaticamente")
        self.combo_idioma_origem.addItems(sorted(nomes_idiomas))
        self.combo_idioma_destino.addItems(sorted(nomes_idiomas))
        try:
            self.combo_idioma_destino.setCurrentText("English")
        except:
            self.combo_idioma_destino.setCurrentIndex(0)

    def abrir_seletor_de_arquivo(self):
        caminho_arquivo, _ = QFileDialog.getOpenFileName(
            self,
            "Selecionar PDF",
            "",
            "Arquivos PDF (*.pdf);;Todos os arquivos (*.*)"
        )
        if caminho_arquivo:
            self.caminho_arquivo_edit.setText(caminho_arquivo)

    def aplicar_estilo(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #2E3440;
                color: #D8DEE9;
                font-family: Arial, sans-serif;
                font-size: 14px;
            }
            QLabel {
                color: #88C0D0;
                margin-bottom: 5px;
            }
            QLineEdit {
                background-color: #4C566A;
                border: 1px solid #5E81AC;
                border-radius: 5px;
                padding: 8px;
            }
            QComboBox {
                background-color: #4C566A;
                border: 1px solid #5E81AC;
                border-radius: 5px;
                padding: 8px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
            QPushButton:pressed {
                background-color: #88C0D0;
            }
        """)