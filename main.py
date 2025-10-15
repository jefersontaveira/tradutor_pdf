# main.py

import sys
from PyQt6.QtWidgets import QApplication
from ui_main_window import TradutorPDFApp

# Este é o ponto de entrada da nossa aplicação. Cria e mostra a interface
if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = TradutorPDFApp() # Cria uma instância da nossa UI
    janela.show()
    sys.exit(app.exec())