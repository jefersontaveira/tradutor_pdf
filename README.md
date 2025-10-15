# Tradutor de PDF com PyQt6

Um aplicativo de desktop moderno construído em Python para traduzir o conteúdo textual de arquivos PDF, com foco na preservação do layout e da hierarquia visual do documento original.

![Screenshot da Aplicação](httpss://i.imgur.com/L1n5DkK.png)  ---

## 🚀 Funcionalidades Principais

* **Tradução de Texto em PDFs:** Extrai e traduz o texto do documento.
* **Preservação de Layout:** Mantém imagens, colunas e a estrutura visual o mais fielmente possível.
* **Preservação da Hierarquia de Fontes:** Títulos continuam como títulos e o corpo do texto mantém sua consistência, ajustando as fontes de forma inteligente.
* **Detecção Automática de Idioma:** Identifica o idioma original do documento, com opção de seleção manual.
* **Interface Gráfica Moderna:** Desenvolvido com PyQt6 para uma experiência de usuário limpa e intuitiva.

---

## 🛠️ Tecnologias Utilizadas

* **Python 3**
* **PyQt6:** Para a interface gráfica.
* **PyMuPDF (Fitz):** Para manipulação e extração de dados de PDFs.
* **googletrans:** Para o serviço de tradução.
* **PyInstaller:** Para empacotar a aplicação em um executável `.exe`.

---

## ⚙️ Como Executar o Projeto

Siga os passos abaixo para executar o projeto em seu ambiente de desenvolvimento.

**1. Pré-requisitos:**
* Ter o Python 3.9+ instalado.
* Ter o Git instalado.

**2. Clone o Repositório:**
```bash
git clone https://github.com/jefersontaveira/tradutor_pdf.git
cd tradutor_pdf