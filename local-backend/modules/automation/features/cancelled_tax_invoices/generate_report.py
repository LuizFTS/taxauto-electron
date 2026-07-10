import logging
import os
from time import sleep

import pandas as pd

logger = logging.getLogger(__name__)


class GenerateReport:
    @staticmethod
    def _is_valid_excel(file_path: str):
        if not os.path.exists(file_path):
            return False

        if os.path.getsize(file_path) == 0:
            return False

        try:
            # Tenta ler apenas o cabeçalho para validar se o motor xlrd aceita o arquivo
            pd.read_excel(file_path, engine="xlrd", nrows=0)
            return True
        except Exception:
            # Se der erro (como o b'<!DOCTYP'), retornamos False para ser removido
            return False

    def execute(self, file_path: str, filial: str):
        if not self._is_valid_excel(file_path):
            if os.path.exists(file_path):
                os.remove(file_path)
            logger.error(f"[Filial {filial}] Arquivo inválido ou corrompido: {file_path}")
            return

        df = pd.read_excel(file_path, engine="xlrd")

        # 5. Sua lógica de limpeza para colunas "Unnamed"
        if any("Unnamed" in str(col) for col in df.columns):
            # Garante que não estamos pegando uma linha vazia como header
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)

        df.columns = df.columns.astype(str).str.strip()

        # --- PASSO 2: MESCLAR AS COLUNAS (AQUI ESTÁ O SEGREDO) ---
        # Só depois disso a coluna "Número do Doc" estará completa
        if "Número Inicial" in df.columns and "Número do Doc" in df.columns:
            df["Número do Doc"] = df["Número do Doc"].fillna(df["Número Inicial"])

        if "Status Inutilização" in df.columns and "Status Doc" in df.columns:
            df["Status Doc"] = df["Status Doc"].fillna(df["Status Inutilização"])

        # --- PASSO 3: LIMPEZA DE LINHAS E CONVERSÃO ---
        # Agora sim, se o "Número do Doc" ainda for nulo, a linha é lixo
        df = df.dropna(subset=["Número do Doc"])

        try:
            # Converte para numérico e garante que é inteiro (Int64 aceita nulos se sobrarem)
            df["Número do Doc"] = pd.to_numeric(df["Número do Doc"], errors="coerce").astype(
                "Int64"
            )

        except Exception as e:
            logger.error(f"[Filial {filial}] Erro na conversão: {e}")

        # --- PASSO 4: FINALIZAÇÃO ---
        # Remove as colunas auxiliares que agora são inúteis
        cols_para_remover = ["Número Inicial", "Status Inutilização"]
        df = df.drop(columns=[c for c in cols_para_remover if c in df.columns])

        df["Filial"] = filial
        # Reordenar colunas colocando Filial na frente
        cols = ["Filial"] + [c for c in df.columns if c != "Filial"]
        df = df[cols]

        # Salvar e remover original
        if os.path.exists(file_path):
            sleep(2)
            os.remove(file_path)

        new_path = file_path.replace(".xls", ".xlsx")
        sleep(2)
        df.to_excel(new_path, index=False)
        logger.info(f"[Filial {filial}] Relatório gerado com sucesso!")
