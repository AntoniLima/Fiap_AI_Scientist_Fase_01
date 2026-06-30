import logging
import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split, cross_val_score, StratifiedKFold
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score

from data_prep import ProcessadorDados

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class TreinadorModelo:
    """
    Treina dois modelos para comparação:
    - Regressão Logística: baseline simples de referência
    - Random Forest: modelo principal (100 árvores de decisão)
    """

    def __init__(self, random_state: int = 42):
        self.lr = LogisticRegression(max_iter=1000, class_weight='balanced', random_state=random_state)
        self.rf = RandomForestClassifier(n_estimators=100, class_weight='balanced', random_state=random_state)
        self.validador = StratifiedKFold(n_splits=5, shuffle=True, random_state=random_state)

    def treinar(self, X_train: pd.DataFrame, y_train: pd.Series) -> None:
        """Treina os dois modelos nos dados de treino."""
        logger.info("Treinando Regressão Logística (baseline)...")
        self.lr.fit(X_train, y_train)

        logger.info("Treinando Random Forest (modelo principal)...")
        self.rf.fit(X_train, y_train)

    def calcular_probabilidades(self, X: pd.DataFrame) -> np.ndarray:
        """Retorna a probabilidade de ser Detrator — usando o Random Forest."""
        return self.rf.predict_proba(X)[:, 1]

    def avaliar_performance(self, X_test: pd.DataFrame, y_test: pd.Series) -> None:
        """Compara os dois modelos com AUC, F1, Precisão e Recall."""
        modelos = {'Reg. Logística': self.lr, 'Random Forest': self.rf}
        resultados = {}

        for nome, modelo in modelos.items():
            y_pred = modelo.predict(X_test)
            y_prob = modelo.predict_proba(X_test)[:, 1]
            resultados[nome] = {
                'auc':       roc_auc_score(y_test, y_prob),
                'f1':        f1_score(y_test, y_pred),
                'precision': precision_score(y_test, y_pred, zero_division=0),
                'recall':    recall_score(y_test, y_pred),
            }

        print(f"\n{'Métrica':20s}  {'Reg. Logística':>16s}  {'Random Forest':>14s}")
        print('-' * 56)
        for chave, label in [('auc', 'AUC-ROC'), ('f1', 'F1-Score'), ('precision', 'Precisão'), ('recall', 'Recall')]:
            print(f"{label:20s}  {resultados['Reg. Logística'][chave]:>16.3f}  {resultados['Random Forest'][chave]:>14.3f}")

        melhor = max(resultados, key=lambda k: resultados[k]['auc'])
        logger.info(f"Melhor modelo: {melhor} (AUC {resultados[melhor]['auc']:.3f})")

    def validar_cruzado(self, X: pd.DataFrame, y: pd.Series) -> None:
        """
        Validação cruzada com 5 folds — confirma que o resultado não dependeu
        de uma divisão específica de treino/teste.
        """
        for nome, modelo in [('Reg. Logística', self.lr), ('Random Forest', self.rf)]:
            scores = cross_val_score(modelo, X, y, cv=self.validador, scoring='roc_auc')
            logger.info(f"CV {nome}: {[round(v, 3) for v in scores]} | Média: {scores.mean():.3f} ± {scores.std():.3f}")

    def importancia_features(self, features: list) -> None:
        """Mostra quais variáveis mais influenciam o risco de Detrator (Random Forest)."""
        importancias = pd.Series(self.rf.feature_importances_, index=features).sort_values(ascending=False)
        logger.info("Importância das features:")
        for feat, valor in importancias.items():
            print(f"  {feat.replace('_', ' '):32s} {valor:.1%}")


class SistemaAlertas:
    """Transforma a probabilidade do modelo em níveis de alerta para o SAC."""

    def __init__(self):
        self.limiar_alto: float = 0.0
        self.limiar_medio: float = 0.0

    def calibrar_limiares(self, probabilidades_treino: np.ndarray) -> None:
        """Define os cortes com base nos percentis P75 e P50 dos dados de treino."""
        self.limiar_alto  = float(np.percentile(probabilidades_treino, 75))
        self.limiar_medio = float(np.percentile(probabilidades_treino, 50))
        logger.info(f"Limiares — ALTO: >= {self.limiar_alto:.3f} | MÉDIO: >= {self.limiar_medio:.3f}")

    def classificar_risco_cliente(self, probabilidades: np.ndarray) -> np.ndarray:
        """Classifica cada cliente como ALTO, MEDIO ou BAIXO risco."""
        condicoes = [probabilidades >= self.limiar_alto, probabilidades >= self.limiar_medio]
        return np.select(condicoes, ['ALTO', 'MEDIO'], default='BAIXO')


class OrquestradorNPS:
    """Conecta todas as etapas: dados → modelos → validação → alertas SAC."""

    def __init__(self, caminho_dados: str):
        self.prep = ProcessadorDados(caminho_dados)
        self.ml   = TreinadorModelo()
        self.sac  = SistemaAlertas()

    def executar_pipeline_completa(self) -> None:
        # 1. Carrega e prepara os dados
        df_bruto = self.prep.carregar_dados()
        X, y = self.prep.separar_features_alvo(df_bruto)

        # 2. Divide treino/teste mantendo a proporção de detratores em ambos
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42, stratify=y
        )

        # 3. Treina e compara os dois modelos
        self.ml.treinar(X_train, y_train)
        self.ml.avaliar_performance(X_test, y_test)

        # 4. Validação cruzada para confirmar estabilidade do modelo
        self.ml.validar_cruzado(X, y)

        # 5. Quais variáveis mais explicam o risco de Detrator?
        self.ml.importancia_features(self.prep.FEATURES)

        # 6. Calibra os limiares de alerta com base nos dados de treino
        probs_treino = self.ml.calcular_probabilidades(X_train)
        self.sac.calibrar_limiares(probs_treino)

        # 7. Classifica os clientes do conjunto de teste
        probs_teste  = self.ml.calcular_probabilidades(X_test)
        segmentos    = self.sac.classificar_risco_cliente(probs_teste)

        # 8. Exporta resultado com gabarito real para validação posterior do SAC
        df_final = X_test.copy()
        df_final['detrator_real']          = y_test.values       # gabarito real
        df_final['probabilidade_detrator'] = probs_teste.round(3)
        df_final['nivel_alerta_sac']       = segmentos

        caminho_saida = "data/processed/risco_clientes_sac.csv"
        df_final.to_csv(caminho_saida, index=False)
        logger.info(f"Pipeline concluída! Resultados em: {caminho_saida}")


if __name__ == "__main__":
    CAMINHO_RAW = "data/raw/desafio_nps_fase_1.csv"
    orquestrador = OrquestradorNPS(caminho_dados=CAMINHO_RAW)
    orquestrador.executar_pipeline_completa()
