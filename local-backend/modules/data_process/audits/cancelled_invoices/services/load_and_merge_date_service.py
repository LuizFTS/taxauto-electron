import os
import shutil
import tempfile
from typing import Any, Dict

import pandas as pd

from shared.utils.dataframe.detect_header_from_lines import detect_header_from_lines


class LoadAndMergeDataService:
    @staticmethod
    def _normalize_number(series: pd.Series) -> pd.Series:
        return series.str.strip().str.lstrip("0").fillna("")

    @staticmethod
    def _normalize_filial(series: pd.Series) -> pd.Series:
        """Garante zero-padding consistente. '6' e '06' viram '06'"""
        return series.str.strip().str.zfill(2).fillna("")

    @staticmethod
    def _detect_excel_header(path: str) -> int:
        """
        Lê as primeiras linhas do Excel sem header para encontrar
        a linha que contém 'Empresa' ou 'Filial' (cabeçalho real dos dados).
        Retorna o índice (0-based) para usar como header=N no read_excel.
        """
        preview = pd.read_excel(path, header=None, nrows=15, dtype=str)
        for idx, row in preview.iterrows():
            row_values = row.fillna("").astype(str).str.strip().str.upper().tolist()
            if "EMPRESA" in row_values or "FILIAL" in row_values:
                return int(idx)
        return 0  # fallback

    def execute(self, fiscal_book_path: str, portal_report_path: str) -> Dict[str, Any]:
        temp_dir = tempfile.gettempdir()
        temp_fiscal_book_path = os.path.join(
            temp_dir, f"temp_val_{os.path.basename(fiscal_book_path)}"
        )
        temp_portal_report_path = os.path.join(
            temp_dir, f"temp_val_{os.path.basename(portal_report_path)}"
        )

        shutil.copy2(fiscal_book_path, temp_fiscal_book_path)
        shutil.copy2(portal_report_path, temp_portal_report_path)

        if fiscal_book_path.endswith(".csv"):
            with open(temp_fiscal_book_path, "r", encoding="cp1252", errors="ignore") as f:
                lines = [line.strip() for line in f.readlines()[:20]]
            header_idx = detect_header_from_lines(lines)
            df_book = pd.read_csv(
                temp_fiscal_book_path,
                dtype=str,
                sep=";",
                skiprows=header_idx,
                encoding="latin-1",
                on_bad_lines="skip",
                engine="python",
                index_col=False,
            )
        else:
            header_row = self._detect_excel_header(temp_fiscal_book_path)
            df_book = pd.read_excel(
                temp_fiscal_book_path, dtype=str, header=header_row, index_col=False
            )

        df_portal = pd.read_excel(temp_portal_report_path, dtype=str)

        df_book.columns = df_book.columns.str.strip()
        df_portal.columns = df_portal.columns.str.strip()

        print("=== COLUNAS BOOK   ===", df_book.columns.tolist())
        print("=== COLUNAS PORTAL ===", df_portal.columns.tolist())
        print("=== BOOK amostra   ===")
        print(
            df_book[["Filial", "Número"]].head(5)
            if "Número" in df_book.columns
            else df_book.head(3)
        )

        # ── Composite key normalizada ─────────────────────────────────────────
        df_book["composite_key"] = (
            self._normalize_filial(df_book["Filial"])
            + "_"
            + self._normalize_number(df_book["Número"])
        )
        df_portal["composite_key"] = (
            self._normalize_filial(df_portal["Filial"])
            + "_"
            + self._normalize_number(df_portal["Número do Doc"])
        )

        print("=== KEYS BOOK   ===", df_book["composite_key"].head(5).tolist())
        print("=== KEYS PORTAL ===", df_portal["composite_key"].head(5).tolist())

        # ── Filtro do livro ───────────────────────────────────────────────────
        # Esse livro indica cancelamento via coluna "Observação" OU "Status Doc"
        # Tentamos as duas, além de verificar se "Esp." indica NFCE cancelada
        termos_regex = "NF CANCELADA|INUTILIZADA|CANCELAD|INUTILIZAD"

        obs_col = next(
            (c for c in df_book.columns if "OBSERVA" in c.upper() or "STATUS" in c.upper()),
            None,
        )

        if obs_col:
            mask = df_book[obs_col].str.upper().str.strip().str.contains(termos_regex, na=False)
            df_book_filtered = df_book[mask]
            print(f"=== BOOK filtrado pela coluna '{obs_col}': {len(df_book_filtered)} linhas ===")
        else:
            # Sem coluna de status: considera TODAS as linhas do livro para cruzamento
            # O use case vai identificar divergências pelo _merge
            df_book_filtered = df_book
            print(
                f"=== BOOK sem coluna de status — usando todas as {len(df_book_filtered)} linhas ==="
            )

        # ── Merge outer ───────────────────────────────────────────────────────
        df_portal_renamed = df_portal.add_prefix("portal_")
        df_portal_renamed = df_portal_renamed.rename(
            columns={"portal_composite_key": "composite_key"}
        )

        merged_df = pd.merge(
            df_book_filtered,
            df_portal_renamed,
            on="composite_key",
            how="outer",
            indicator=True,
        )

        print("=== _merge value_counts ===")
        print(merged_df["_merge"].value_counts())

        try:
            os.remove(temp_fiscal_book_path)
            os.remove(temp_portal_report_path)
        except Exception:
            pass

        return {
            "merged_data": merged_df,
            "book_count": len(df_book_filtered),
            "portal_count": len(df_portal),
        }
