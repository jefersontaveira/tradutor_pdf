# Arquivo: translator_core.py

import fitz  # PyMuPDF
from collections import defaultdict
from googletrans import Translator, LANGUAGES

# Cria um dicionário reverso para buscar o código do idioma pelo nome
# Ex: "English" -> "en"
CODIGOS_IDIOMAS = {lang.capitalize(): code for code, lang in LANGUAGES.items()}


class PdfTranslator:
    def __init__(self, caminho_arquivo, idioma_origem, idioma_destino):
        self.caminho_arquivo = caminho_arquivo

        # Converte os nomes dos idiomas para os códigos que a API entende
        self.idioma_origem = "auto" if idioma_origem == "Detectar Automaticamente" else CODIGOS_IDIOMAS.get(
            idioma_origem, "auto")
        self.idioma_destino = CODIGOS_IDIOMAS.get(idioma_destino)

        self.dados_do_pdf = []
        self.mapeamento_de_fontes = {}
        self.translator = Translator()  # Instancia o tradutor uma vez para reutilização
        self.doc = fitz.open(self.caminho_arquivo)  # Abre o doc uma vez

    def run_translation(self):
        try:
            print("Fase 1: Lendo e analisando o PDF...")
            self.analisar_pdf()

            print("\nFase 2: Agrupando fontes e calculando novos tamanhos...")
            self.agrupar_e_calcular_fontes()

            # Futuras fases aqui...
            return True
        except Exception as e:
            print(f"Ocorreu um erro em run_translation: {e}")
            # Fecha o documento em caso de erro
            if self.doc and not self.doc.is_closed:
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

            menor_fonte_do_grupo = float(tamanho_original)

            for i, bloco in enumerate(blocos):
                texto_original = bloco["texto"]
                rect = fitz.Rect(bloco["coordenadas"])

                try:
                    traducao = self.translator.translate(texto_original, src=self.idioma_origem,
                                                         dest=self.idioma_destino)
                    texto_traduzido = traducao.text
                except Exception as e:
                    print(
                        f"  - Aviso: Falha na tradução do texto '{texto_original[:20]}...'. Usando original. Erro: {e}")
                    texto_traduzido = texto_original

                fonte_necessaria = self._calcular_fonte_ajustada(rect, texto_traduzido, tamanho_original)

                if fonte_necessaria < menor_fonte_do_grupo:
                    menor_fonte_do_grupo = fonte_necessaria

                print(f"  - Bloco {i + 1}/{len(blocos)}: Fonte necessária: {fonte_necessaria:.2f}pt")

            self.mapeamento_de_fontes[tamanho_original] = menor_fonte_do_grupo

        print("\n--- Mapeamento de Fontes Concluído ---")
        for original, novo in self.mapeamento_de_fontes.items():
            print(f"Textos com {original}pt serão reescritos com {novo:.2f}pt.")
        print("-------------------------------------")

    def _calcular_fonte_ajustada(self, rect, texto, tamanho_inicial):
        """
        Mede o texto e reduz a fonte até que ele caiba no retângulo (rect) fornecido.
        """
        tamanho_fonte_atual = float(tamanho_inicial)
        pagina_temp = self.doc.new_page()

        while tamanho_fonte_atual > 4:  # Define um limite mínimo de 4pt
            transbordou = pagina_temp.insert_textbox(rect, texto, fontsize=tamanho_fonte_atual)
            if transbordou < 1:
                break
            tamanho_fonte_atual -= 0.5

        self.doc.delete_page(pagina_temp.number)
        return tamanho_fonte_atual