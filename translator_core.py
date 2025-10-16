# translator_core.py

import fitz  # PyMuPDF
from collections import defaultdict


class PdfTranslator:
    def __init__(self, caminho_arquivo, idioma_origem, idioma_destino):
        self.caminho_arquivo = caminho_arquivo
        self.idioma_origem = idioma_origem
        self.idioma_destino = idioma_destino
        self.dados_do_pdf = []
        self.mapeamento_de_fontes = {}
    def run_translation(self):
        """
        Orquestra todo o processo de tradução.
        Retorna True se bem-sucedido, False se ocorrer um erro.
        """
        try:
            print("Fase 1: Lendo e analisando o PDF...")
            self.analisar_pdf()

            print("\nFase 2: Agrupando fontes e calculando novos tamanhos...")
            self.agrupar_e_calcular_fontes()

            # Cada fase vem aqui:
            # print("Fase 3: Traduzindo textos...")
            # print("Fase 4: Reconstruindo o novo PDF...")

            # Se tudo certo até, retorna sucesso.
            return True
        except Exception as e:
            print(f"Ocorreu um erro em run_translation: {e}")
            return False

    def analisar_pdf(self):
        """
        Abre o PDF e extrai blocos de texto com suas propriedades (posição, fonte).
        """
        # Abre o documento PDF
        doc = fitz.open(self.caminho_arquivo)
        print(f"O documento tem {len(doc)} páginas.")

        # Itera por cada página do documento
        for num_pagina, pagina in enumerate(doc):
            # Usei "dict" para obter a estrutura de dados detalhada
            blocos = pagina.get_text("dict")["blocks"]

            # Itera por cada bloco de conteúdo na página
            for bloco in blocos:
                # Verifica se o bloco é de texto (type 0)
                if bloco["type"] == 0:
                    for linha in bloco["lines"]:
                        for span in linha["spans"]:
                            # Extraí as informações que preciso
                            texto = span["text"]
                            tamanho_fonte = round(span["size"])  # Arredondamos para agrupar melhor
                            coordenadas = span["bbox"]  # (x0, y0, x1, y1)

                            # Guarda os dados na lista
                            self.dados_do_pdf.append({
                                "pagina": num_pagina,
                                "texto": texto,
                                "tamanho_fonte": tamanho_fonte,
                                "coordenadas": coordenadas
                            })

        doc.close()
        print(f"Análise concluída. Foram extraídos {len(self.dados_do_pdf)} blocos de texto.")
        # Imprime só os 5 primeiros para depuração:
        print("--- Amostra dos dados extraídos ---")
        for item in self.dados_do_pdf[:5]:
            print(item)
        print("---------------------------------")

    def agrupar_e_calcular_fontes(self):
        """
        Agrupa os textos por tamanho de fonte e determina a nova fonte para cada grupo.
        """
        if not self.dados_do_pdf:
            print("Nenhum dado de PDF para analisar.")
            return

        # 1. Agrupar os blocos de texto pelo tamanho da fonte original
        # defaultdict(list) cria um dicionário onde cada item novo é uma lista vazia
        grupos_de_fonte = defaultdict(list)
        for bloco in self.dados_do_pdf:
            grupos_de_fonte[bloco["tamanho_fonte"]].append(bloco)

        print(f"Encontrados {len(grupos_de_fonte)} grupos de fontes distintos: {sorted(grupos_de_fonte.keys())}")

        # 2. Para cada grupo, calcula o "tamanho de fonte mestre"
        for tamanho_original, blocos in grupos_de_fonte.items():
            print(f"\nProcessando grupo de fonte: {tamanho_original}pt (contém {len(blocos)} blocos)")

            # --- SIMULAÇÃO DA LÓGICA DE CÁLCULO ---
            # No futuro, aqui entra a lógica complexa de:
            #   a. Traduzir cada texto do grupo.
            #   b. Medir o espaço que o texto traduzido ocupa.
            #   c. Reduzir a fonte até caber na caixa original.
            #   d. Encontrar a menor fonte calculada DENTRO deste grupo.
            #
            # POR ENQUANTO, vou apenas simular que a nova fonte é 1pt menor.
            nova_fonte_mestre = tamanho_original - 1
            # ----------------------------------------

            # Armazenamos o resultado no nosso mapeamento
            self.mapeamento_de_fontes[tamanho_original] = nova_fonte_mestre

        print("\n--- Mapeamento de Fontes Concluído ---")
        for original, novo in self.mapeamento_de_fontes.items():
            print(f"Textos com {original}pt serão reescritos com {novo}pt.")
        print("-------------------------------------")