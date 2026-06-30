# Variáveis de ambiente
VENV = venv
PYTHON = $(VENV)/Scripts/python
PIP = $(VENV)/Scripts/pip

.DEFAULT_GOAL := help

help:
	@echo "Comandos disponíveis:"
	@echo "  make setup    - Cria o ambiente virtual e instala as dependências"
	@echo "  make clean    - Remove arquivos de cache e o ambiente virtual"
	@echo "  make run      - Executa o orquestrador do pipeline (main.py)"

setup:
	@echo "Criando o ambiente virtual..."
	python -m venv $(VENV)
	@echo "Atualizando o pip..."
	$(PYTHON) -m pip install --upgrade pip
	@echo "Instalando dependências..."
	$(PIP) install -r requirements.txt
	@echo "Setup concluído! Para ativar, rode: source venv/Scripts/activate"

run:
	@echo "Executando o pipeline completo..."
	$(PYTHON) main.py

clean:
	@echo "Limpando o cache do projeto..."
	rm -rf $(VENV)
	find . -type d -name "__pycache__" -exec rm -r {} +
	@echo "Limpeza concluída!"