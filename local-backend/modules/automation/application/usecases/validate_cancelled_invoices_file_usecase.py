import os
import shutil
import tempfile

import pandas as pd

from modules.automation.application.dto.cancelled_invoices_dto import (
    ValidateFileDTO,
    ValidateFileResponseDTO,
)
from shared.utils.dataframe.detect_header_from_lines import detect_header_from_lines


class ValidateCancelledInvoicesFileUseCase:
    def execute(self, dto: ValidateFileDTO) -> ValidateFileResponseDTO:
        if not os.path.exists(dto.file_path):
            return ValidateFileResponseDTO(
                is_valid=False, record_count=0, message="Arquivo não encontrado."
            )

        # Criamos um caminho temporário único para não haver conflito
        temp_dir = tempfile.gettempdir()
        temp_file_path = os.path.join(temp_dir, f"temp_val_{os.path.basename(dto.file_path)}")

        try:
            # Copia o arquivo original para o diretório temporário
            shutil.copy2(dto.file_path, temp_file_path)

            if dto.file_path.endswith(".xls"):
                df = pd.read_excel(temp_file_path, engine="xlrd")
            elif dto.file_path.endswith(".csv"):
                with open(temp_file_path, "r", encoding="cp1252", errors="ignore") as f:
                    lines = [line.strip() for line in f.readlines()[:20]]

                header_idx = detect_header_from_lines(lines)

                df = pd.read_csv(
                    temp_file_path,
                    sep=";",
                    encoding="cp1252",
                    engine="python",
                    skiprows=header_idx,
                    on_bad_lines="skip",
                    index_col=False,
                )
            else:
                df = pd.read_excel(temp_file_path)

            df.columns = df.columns.astype(str).str.strip()

            # Caso o header tenha vindo como "Unnamed" (comum em XLS mal formatado)
            if any("Unnamed" in str(col) for col in df.columns):
                df.columns = df.iloc[0].astype(str).str.strip()
                df = df[1:].reset_index(drop=True)

            if dto.file_type == "livro_fiscal":
                # if type equals to livro_fiscal, df columns must have these columns:
                required_columns = [
                    "Filial",
                    "Número",
                    "Observação",
                ]

                # 4. Filtrar por Observação (conforme pedido)
                if "Observação" in df.columns:
                    df["Observação"] = df["Observação"].astype(str).str.strip()
                    termos_permitidos = ["NF CANCELADA", "INUTILIZADA"]
                    df = df[df["Observação"].str.upper().isin(termos_permitidos)]

                # check if df has all required columns
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    return ValidateFileResponseDTO(
                        is_valid=False,
                        record_count=0,
                        message=f"Colunas ausentes: {', '.join(missing_columns)}",
                    )

                if df.empty:
                    return ValidateFileResponseDTO(
                        is_valid=False, record_count=0, message="Arquivo vazio"
                    )

                # check if df has any duplicate rows specific in the required columns
                if df.duplicated(subset=required_columns).any():
                    return ValidateFileResponseDTO(
                        is_valid=False, record_count=0, message="Arquivo contém linhas duplicadas"
                    )

                record_count = len(df)
                return ValidateFileResponseDTO(
                    is_valid=True, record_count=record_count, message="Arquivo OK"
                )

            if dto.file_type == "notas_canceladas":
                # if type equals to portal_ged, df columns must have these columns:
                required_columns = [
                    "Filial",
                    "Número do Doc",
                    "Status Doc",
                ]

                # check if df has all required columns
                missing_columns = [col for col in required_columns if col not in df.columns]
                if missing_columns:
                    return ValidateFileResponseDTO(
                        is_valid=False,
                        record_count=0,
                        message=f"Colunas ausentes: {', '.join(missing_columns)}",
                    )

                # check if df has any rows
                if df.empty:
                    return ValidateFileResponseDTO(
                        is_valid=False, record_count=0, message="Arquivo vazio"
                    )

                # check if df has any duplicate rows
                if df.duplicated(subset=required_columns).any():
                    return ValidateFileResponseDTO(
                        is_valid=False, record_count=0, message="Arquivo contém linhas duplicadas"
                    )

                record_count = len(df)
                return ValidateFileResponseDTO(
                    is_valid=True, record_count=record_count, message="Arquivo OK"
                )

        except Exception as e:
            return ValidateFileResponseDTO(
                is_valid=False, record_count=0, message=f"Erro ao ler arquivo: {str(e)}"
            )
        finally:
            # Remove o arquivo temporário
            if os.path.exists(temp_file_path):
                try:
                    os.remove(temp_file_path)
                except Exception:
                    pass
