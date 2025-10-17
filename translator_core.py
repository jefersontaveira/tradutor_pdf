# translator_core.py

import fitz  # PyMuPDF
from collections import defaultdict
<<<<<<< HEAD
from googletrans import Translator, LANGUAGES

# Cria um dicionário reverso para buscar o código do idioma pelo nome
# Ex: "English" -> "en"
CODIGOS_IDIOMAS = {lang.capitalize(): code for code, lang in LANGUAGES.items()}
=======
>>>>>>> 729d5c4a7b2389179f52c26c8ab317d3828d6939


class PdfTranslator:
    def __init__(self, caminho_arquivo, idioma_origem, idioma_destino):
        self.caminho_arquivo = caminho_arquivo
<<<<<<< HEAD

        # Converte os nomes dos idiomas para os códigos que a API entende
        self.idioma_origem = "auto" if idioma_origem == "Detectar Automaticamente" else CODIGOS_IDIOMAS.get(
            idioma_origem, "auto")
        self.idioma_destino = CODIGOS_IDIOMAS.get(idioma_destino)

        self.dados_do_pdf = []
        self.mapeamento_de_fontes = {}
        self.translator = Translator()  # Instancia o tradutor uma vez para reutilização
        self.doc = fitz.open(self.caminho_arquivo)  # Abre o doc uma vez

    def run_translation(self):
=======
        self.idioma_origem = idioma_origem
        self.idioma_destino = idioma_destino
        self.dados_do_pdf = []
        self.mapeamento_de_fontes = {}
    def run_translation(self):
        """
        Orquestra todo o processo de tradução.
        Retorna True se bem-sucedido, False se ocorrer um erro.
        """
>>>>>>> 729d5c4a7b2389179f52c26c8ab317d3828d6939
        try:
            print("Fase 1: Lendo e analisando o PDF...")
            self.analisar_pdf()

            print("\nFase 2: Agrupando fontes e calculando novos tamanhos...")
            self.agrupar_e_calcular_fontes()

<<<<<<< HEAD
            # Futuras fases aqui...
            return True
        except Exception as e:
            print(f"Ocorreu um erro em run_translation: {e}")
            # Fecha o documento em caso de erro
            self.doc.close()
            return False
        finally:
            # Garante que o documento seja fechado ao final do processo
            if self.doc and not self.doc.is_closed:
                self.doc.close()

    def analisar_pdf(self):
        for num_pagina, pagina in enumerate(self.doc):
            blocos = pagina.get_text("dict")["blocks"]
            for bloco in blocos:
                if bloco["type"] == 0:
                    for linha in bloco["lines"]:
                        for span in linha["spans"]:
                            self.dados_do_pdf.append({
                                "pagina": num_pagina,
                                "texto": span["text"].strip(),
                                "tamanho_fonte": round(span["size"]),
                                "coordenadas": span["bbox"]
                            })
        print(f"Análise concluída. Foram extraídos {len(self.dados_do_pdf)} blocos de texto.")

    def agrupar_e_calcular_fontes(self):
        if not self.dados_do_pdf: return

        grupos_de_fonte = defaultdict(list)
        for bloco in self.dados_do_pdf:
            if bloco["texto"]:  # Ignora blocos de texto vazios
                grupos_de_fonte[bloco["tamanho_fonte"]].append(bloco)

        print(f"Encontrados {len(grupos_de_fonte)} grupos de fontes distintos: {sorted(grupos_de_fonte.keys())}")

        for tamanho_original, blocos in grupos_de_fonte.items():
            print(f"\nProcessando grupo de fonte: {tamanho_original}pt (contém {len(blocos)} blocos)")

            # Começamos assumindo que a menor fonte necessária será a original
            menor_fonte_do_grupo = float(tamanho_original)

            for i, bloco in enumerate(blocos):
                texto_original = bloco["texto"]
                rect = fitz.Rect(bloco["coordenadas"])

                # 1. TRADUZIR O TEXTO
                try:
                    # A API tem um limite, então textos muito grandes podem falhar.
                    # Idealmente, eles seriam quebrados, mas por agora isso é suficiente.
                    traducao = self.translator.translate(texto_original, src=self.idioma_origem,
                                                         dest=self.idioma_destino)
                    texto_traduzido = traducao.text
                except Exception as e:
                    print(
                        f"  - Aviso: Falha na tradução do texto '{texto_original[:20]}...'. Usando original. Erro: {e}")
                    texto_traduzido = texto_original

                # 2. CALCULAR A FONTE AJUSTADA
                fonte_necessaria = self._calcular_fonte_ajustada(rect, texto_traduzido, tamanho_original)

                # 3. ATUALIZAR A MENOR FONTE DO GRUPO
                if fonte_necessaria < menor_fonte_do_grupo:
                    menor_fonte_do_grupo = fonte_necessaria

                print(f"  - Bloco {i + 1}/{len(blocos)}: Fonte necessária: {fonte_necessaria:.2f}pt")

            # Armazenamos o resultado final para este grupo
            self.mapeamento_de_fontes[tamanho_original] = menor_fonte_do_grupo

        print("\n--- Mapeamento de Fontes Concluído ---")
        for original, novo in self.mapeamento_de_fontes.items():
            print(f"Textos com {original}pt serão reescritos com {novo:.2f}pt.")
        print("-------------------------------------")

    def _calcular_fonte_ajustada(self, rect, texto, tamanho_inicial):
        """
        Mede o texto e reduz a fonte até que ele caiba no retângulo (rect) fornecido.
        Este é um método "privado", indicado pelo underscore no início.
        """
        tamanho_fonte_atual = float(tamanho_inicial)

        # Cria uma página temporária apenas para medir o texto
        pagina_temp = self.doc.new_page()

        # Loop para reduzir a fonte
        while tamanho_fonte_atual > 7:  # Define um limite mínimo de 4pt
            # O método insert_textbox com render=False nos diz quanto texto "transbordou"
            transbordou = pagina_temp.insert_textbox(rect, texto, fontsize=tamanho_fonte_atual)

            # Se não transbordou (ou o transbordamento é mínimo), a fonte serve
            if transbordou < 1:
                break

            # Reduz a fonte para a próxima tentativa
            tamanho_fonte_atual -= 0.5

        # Remove a página temporária para não usar memória
        self.doc.delete_page(pagina_temp.number)

        return tamanho_fonte_atual
=======
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
>>>>>>> 729d5c4a7b2389179f52c26c8ab317d3828d6939
