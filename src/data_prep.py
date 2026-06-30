import logging
import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger(__name__)


class ProcessadorDados:
    """Carrega e prepara os dados de NPS, evitando data leakage."""

    # Apenas variáveis disponíveis após a entrega e antes do NPS ser coletado
    FEATURES = [
        'delivery_delay_days', 'complaints_count', 'customer_service_contacts',
        'resolution_time_days', 'delivery_attempts', 'freight_value',
        'order_value', 'items_quantity', 'discount_value',
        'customer_tenure_months', 'payment_installments'
    ]

    def __init__(self, caminho_arquivo: str):
        self.caminho_arquivo = caminho_arquivo

    def carregar_dados(self) -> pd.DataFrame:
        """Lê o CSV e verifica se há valores nulos."""
        try:
            df = pd.read_csv(self.caminho_arquivo)
            nulos = df.isnull().sum().sum()
            logger.info(f"Dados carregados: {df.shape[0]} linhas × {df.shape[1]} colunas | Nulos: {nulos}")
            return df
        except FileNotFoundError:
            logger.error(f"Arquivo não encontrado: {self.caminho_arquivo}")
            raise

    def separar_features_alvo(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
        """
        Cria o target binário (NPS <= 6 = Detrator) e isola as features operacionais.
        Colunas como nps_score e csat_internal_score são excluídas para evitar leakage.
        """
        try:
            y = (df['nps_score'] <= 6).astype(int)
            X = df[self.FEATURES]

            pct_det = y.mean() * 100
            logger.info(f"Detratores: {y.sum()} ({pct_det:.1f}%) | Não-detratores: {(y == 0).sum()} ({100 - pct_det:.1f}%)")

            # Classes desbalanceadas: class_weight='balanced' compensa isso no modelo
            if pct_det < 30 or pct_det > 70:
                logger.warning("Classes desbalanceadas detectadas — class_weight='balanced' está ativo.")

            return X, y
        except KeyError as e:
            logger.error(f"Coluna ausente no DataFrame: {e}")
            raise
