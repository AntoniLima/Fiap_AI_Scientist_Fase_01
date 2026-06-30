import sys
from pathlib import Path

# Permite que o Python encontre os módulos dentro de src/
sys.path.insert(0, str(Path(__file__).parent / "src"))

from train import OrquestradorNPS

if __name__ == "__main__":
    CAMINHO_RAW = "data/raw/desafio_nps_fase_1.csv"
    OrquestradorNPS(caminho_dados=CAMINHO_RAW).executar_pipeline_completa()
