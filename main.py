# main.py

import sys
from PyQt6.QtWidgets import QApplication, QMessageBox

from ui_main_window import TradutorPDFApp
from translator_core import PdfTranslator

# Cria uma classe controladora para separar a lógica da UI
class MainController:
    def __init__(self):
        # Cria a aplicação e a janela
        self.app = QApplication(sys.argv)
        self.janela = TradutorPDFApp()

        # --- Conectando os Sinais da UI aos Métodos do Controlador ---
        self.janela.botao_traduzir.clicked.connect(self.iniciar_traducao)

    def iniciar_traducao(self):
        """Pega os dados da UI, valida e inicia o processo de tradução."""
        # 1. Obter os dados da interface
        caminho_pdf = self.janela.caminho_arquivo_edit.text()
        idioma_origem_selecionado = self.janela.combo_idioma_origem.currentText()
        idioma_destino_selecionado = self.janela.combo_idioma_destino.currentText()

        # 2. Validar os dados
        if not caminho_pdf:
            QMessageBox.warning(self.janela, "Atenção", "Por favor, selecione um arquivo PDF primeiro.")
            return # Para a execução aqui se não houver arquivo

        if idioma_origem_selecionado == idioma_destino_selecionado:
            QMessageBox.warning(self.janela, "Atenção", "O idioma de origem e de destino não podem ser iguais.")
            return

        # 3. Instanciar e executar o motor de tradução
        try:
            # Desabilitar o botão para evitar cliques duplos e dar feedback
            self.janela.botao_traduzir.setEnabled(False)
            self.janela.botao_traduzir.setText("Traduzindo...")
            # Força a UI a se redesenhar imediatamente
            self.app.processEvents()

            # --- Ponto Chave da Conexão ---
            # Cria uma instância do nosso motor de tradução com os dados da UI
            tradutor = PdfTranslator(
                caminho_arquivo=caminho_pdf,
                idioma_origem=idioma_origem_selecionado,
                idioma_destino=idioma_destino_selecionado
            )
            # Chama o método principal do motor, que executa a análise do PDF
            sucesso = tradutor.run_translation()
            # --------------------------------

            if sucesso:
                QMessageBox.information(self.janela, "Sucesso", "A análise do PDF foi concluída com sucesso! (Tradução ainda não implementada)")
            else:
                QMessageBox.critical(self.janela, "Erro", "Ocorreu um erro durante a análise do PDF.")

        except Exception as e:
            QMessageBox.critical(self.janela, "Erro Crítico", f"Ocorreu um erro inesperado: {e}")
        finally:
            # Reabilita o botão, não importa se deu sucesso ou erro
            self.janela.botao_traduzir.setEnabled(True)
            self.janela.botao_traduzir.setText("Traduzir PDF")

    def run(self):
        """Exibe a janela e inicia o loop da aplicação."""
        self.janela.show()
        sys.exit(self.app.exec())


if __name__ == '__main__':
    controlador = MainController()
    controlador.run()