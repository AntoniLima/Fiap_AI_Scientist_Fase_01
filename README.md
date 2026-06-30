# **📊 Case NPS Preditivo - AI Scientist (Fase 01)**

Projeto desenvolvido para a Fase 01 da pós-graduação em AI Scientist. O objetivo principal deste case é construir soluções preditivas para o Net Promoter Score (NPS), auxiliando na tomada de decisão estratégica e na retenção de clientes.

O escopo do projeto foca no raciocínio analítico e abrange as seguintes etapas fundamentais:

* **Entendimento do Negócio:** Exercício prático de pensamento analítico e tradução de necessidades corporativas, indo além da execução de código.
* **Definição da Variável Target:** Mapeamento e definição clara do alvo matemático para o problema de negócio em questão.
* **Análise Exploratória de Dados (EDA):** Investigação da base de dados com foco total em extrair insights direcionados ao negócio.
* **Modelagem de Regressão:** Construção de um modelo preditivo desenhado para estimar a nota de NPS do cliente em uma escala contínua.
* **Modelagem de Classificação:** Desenvolvimento de um segundo modelo focado em categorizar os clientes em grupos estratégicos (ex: satisfeitos vs. insatisfeitos / promotores vs. detratores).

---

## **💡 Principais Insights de Negócio (EDA)**

Durante a Análise Exploratória ([veja o notebook completo aqui](./notebooks/01_eda_nps_Final.ipynb)), identificamos padrões operacionais críticos que impactam diretamente o NPS antes mesmo da pesquisa ser enviada ao cliente:

* **Ponto de Ruptura Logístico:** Atrasos são fatais. A partir de **2 dias de atraso**, a maioria dos clientes já se torna detratora. Com **3 dias**, a insatisfação é praticamente unânime.
* **Tolerância no Atendimento:** A **2ª reclamação** é o grande divisor de águas. O cliente costuma perdoar a primeira falha se for bem atendido, mas recontatos derrubam o NPS de forma consistente.
* **O Perfil do NPS:** A satisfação não está ligada a um perfil demográfico específico, mas sim à eficiência operacional:
  * *Alto NPS:* Entrega no prazo + Zero reclamações + Recompra rápida.
  * *Baixo NPS:* Atrasos + Reclamações repetidas + Atendimento lento.
* **Ação Preventiva:** Como os fatores de queda de NPS são rastreáveis *antes* do cliente dar a nota, a empresa pode atuar preditivamente (ex: priorizar a logística de um pedido que está prestes a bater 2 dias de atraso).

---

## **🤖 O Pipeline de Machine Learning**

Para transformar esses insights em ação, construímos um pipeline de Machine Learning orquestrado. 
* Evitamos *data leakage* isolando apenas variáveis operacionais.
* Lidamos com o desbalanceamento das classes e utilizamos uma **Random Forest** (com validação cruzada) superando o baseline de Regressão Logística.
* **Produto Final:** O script gera uma classificação de risco e exporta um arquivo otimizado (`risco_clientes_sac.csv`) com níveis de alerta (ALTO, MÉDIO, BAIXO) para que a equipe de atendimento possa agir preventivamente.

---

## **📁 Estrutura do Projeto**

O repositório foi estruturado utilizando boas práticas de Engenharia de Dados e MLOps para facilitar a colaboração:

* **`main.py`**: O orquestrador central. Executa o pipeline de ponta a ponta.
* **`/src`**: Módulos orientados a objetos.
  * `data_prep.py`: Processador de dados (ingestão e feature engineering seguro).
  * `train.py`: Treinador dos modelos, avaliador de métricas e gerador de alertas.
* **`/data`**: Diretório contendo os conjuntos de dados.
  * `/raw`: Dados brutos e imutáveis originais.
  * `/processed`: Dados limpos e transformados, prontos para exportação de alertas.
* **`/notebooks`**: Jupyter Notebooks com a Análise Exploratória de Dados (EDA) e experimentações iniciais.
* **`/models`**: Arquivos do modelo treinado exportados (ex: `.pkl`, `.joblib`).
* **`/docs`**: Documentação de apoio e apresentação final do case.
* **`requirements.txt`**: Lista de dependências e bibliotecas Python necessárias.
* **`Makefile`**: Automação de comandos para configuração do ambiente.

---

## **🚀 Como Executar**

Este projeto utiliza um `Makefile` para padronizar e automatizar a configuração do ambiente virtual, garantindo que toda a equipe execute o código sem conflitos de versão.

**1. Clone o repositório:**
```bash
git clone [https://github.com/AntoniLima/Fiap_AI_Scientist_Fase_01.git](https://github.com/AntoniLima/Fiap_AI_Scientist_Fase_01.git)

cd Fiap_AI_Scientist_Fase_01

```

**2. Configure o ambiente automaticamente:**
No terminal (Git Bash ou Linux/Mac), execute o comando abaixo para criar o ambiente e instalar todas as dependências do `requirements.txt`:

```bash
make setup

```

**3. Ative o ambiente virtual:**
Sempre que for trabalhar no projeto ou abrir os notebooks, ative o ambiente isolado:

* **Windows (Git Bash):** `source venv/Scripts/activate`
* **Linux/Mac:** `source venv/bin/activate`

**4. Execução do Pipeline Completo:**

Para rodar a extração, o treinamento dos modelos e gerar a base final de alertas para o SAC, basta executar o orquestrador:

```bash
python main.py
```

(Ou utilize make run caso tenha mapeado o comando no Makefile).
*💡 **Dica útil:** Para limpar o cache do projeto (`__pycache__`) e formatar o ambiente em caso de falhas, basta rodar `make clean`.*

---

## **📅 Apresentação e Análise de Negócio**
Toda a documentação gerada, incluindo a apresentação executiva e a análise aprofundada de negócio, está disponível nos links abaixo:

👉 [**Acessar Apresentação do Projeto (PDF)**](./docs/Apresentacao/Apresentacao_NPS_Preditivo.pdf)
👉 [![Apresentação Tech Challenge - Grupo 12](https://img.youtube.com/vi/CTXHmgtaeK0/maxresdefault.jpg)](https://www.youtube.com/watch?v=CTXHmgtaeK0)
👉 [**Veja o notebook EDA completo aqui**](./notebooks/01_eda_nps_Final.ipynb)
👉 [**Veja o notebook do modelo aqui**](./notebooks/modelo.ipynb)

---

## 👥 Equipe

* Amanda Cristine
* Antonio Lima
* Joviniano Gil
* Luiza Ferreira
* Vinicius Moutinho