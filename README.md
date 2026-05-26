# 📊 Case NPS Preditivo - AI Scientist (Fase 01)

Projeto desenvolvido para a Fase 01 da pós-graduação em AI Scientist. O objetivo deste case é construir um modelo preditivo capaz de analisar e prever o Net Promoter Score (NPS), auxiliando na tomada de decisão estratégica e na retenção de clientes.

---

## 📁 Estrutura do Projeto

O repositório está organizado utilizando as melhores práticas para projetos em Ciência de Dados:

* **`/data`**: Diretório contendo os conjuntos de dados.
  * `/raw`: Dados brutos e imutáveis originais.
  * `/processed`: Dados limpos e transformados, prontos para modelagem.
* **`/notebooks`**: Jupyter Notebooks com a Análise Exploratória de Dados (EDA) e experimentações iniciais.
* **`/src`**: Scripts em Python para automação do pipeline.
  * `data_prep.py`: Ingestão, limpeza e transformação dos dados.
  * `train.py`: Treinamento, validação e serialização do modelo.
* **`/models`**: Arquivos do modelo treinado exportados (ex: `.pkl`, `.joblib`).
* **`/docs`**: Documentação de apoio e apresentação final do case.

---

## 🚀 Como Executar

**1. Clone o repositório:**
```bash
git clone [https://github.com/AntoniLima/Fiap_AI_Scientist_Fase_01.git](https://github.com/AntoniLima/Fiap_AI_Scientist_Fase_01.git)

2. Instale as dependências:
Certifique-se de ter o Python instalado e execute:

Bash
pip install -r requirements.txt
3. Execução:

Inicie explorando os notebooks na pasta /notebooks.

Para rodar o pipeline completo de treinamento, execute: python src/train.py

👥 Equipe
Amanda Cristine

Antonio Lima

Joviniano Gil

Luiza Ferreira

Vinicius Moutinho