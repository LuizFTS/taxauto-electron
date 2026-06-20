import re
from pathlib import Path
from typing import List

import pandas as pd

from shared.utils.dataframe.detect_header_from_lines import detect_header_from_lines


class MergeExcelFilesService:
    """
    Service responsible for merging CSV/XLSX files into a single Excel file.
    """

    DEFAULT_PREVIEW_ROWS = 20
    MIN_NON_NULL_THRESHOLD = 2

    def _score_columns(self, columns: List[str]) -> float:
        """
        Pontua qualidade de um conjunto de colunas.
        Colunas boas: texto, únicas, não são valores numéricos/datas.
        """
        if not columns:
            return 0.0

        cleaned = [str(c).strip() for c in columns]

        # Penaliza colunas que parecem valores ou índices (ex: "376,09", "0", "nan")
        def is_bad_col(c: str) -> bool:
            if c.lower() in ("nan", "none", ""):
                return True
            if re.match(r"^-?\d+([.,]\d+)?$", c):  # número puro
                return True
            if re.match(r"^\d{2}/\d{2}/\d{4}$", c):  # data
                return True
            return False

        good_cols = [c for c in cleaned if not is_bad_col(c)]
        unique_ratio = len(set(good_cols)) / len(cleaned)
        good_ratio = len(good_cols) / len(cleaned)

        return len(cleaned) * good_ratio * unique_ratio

    def _pick_reference_columns(self, dataframes: List[pd.DataFrame]) -> List[str]:
        """
        Escolhe como referência as colunas do DataFrame com maior score.
        Ignora 'nome_arquivo' no rankeamento mas preserva no final.
        """
        best_df = max(
            dataframes,
            key=lambda df: self._score_columns([c for c in df.columns if c != "nome_arquivo"]),
        )
        # Garante que nome_arquivo sempre vai junto, se existir
        ref = [c for c in best_df.columns if c != "nome_arquivo"]
        if any("nome_arquivo" in df.columns for df in dataframes):
            ref.append("nome_arquivo")
        return ref

    def execute(self, paths: List[str], output_dir: str) -> Path:
        """
        Main entrypoint for the service.
        """
        dataframes = self._load_files(paths)
        merged_df = self._merge_dataframes(dataframes)
        return self._save_output(merged_df, output_dir)

    # =========================
    # Loading Layer
    # =========================

    def _load_files(self, paths: List[str]) -> List[pd.DataFrame]:
        if not paths:
            raise ValueError("No input files provided.")

        dataframes = []
        for path_str in paths:
            path = Path(path_str)
            if not path.exists():
                raise FileNotFoundError(f"File not found: {path}")

            extension = path.suffix.lower()
            try:
                if extension == ".csv":
                    df = self._load_csv(path)
                elif extension in (".xlsx", ".xls", ".xlsm"):
                    df = self._load_excel(path)
                else:
                    raise ValueError(f"Unsupported file type: {extension}")

                dataframes.append(df)
            except Exception as e:
                # Wrap the error to provide context on which file failed
                raise RuntimeError(f"Error processing file {path.name}: {e}") from e

        return dataframes

    def _load_csv(self, path: Path) -> pd.DataFrame:
        """
        Robust CSV loader using raw line inspection for header detection.
        """

        with open(path, "r", encoding="cp1252", errors="ignore") as f:
            lines = [line.strip() for line in f.readlines()[: self.DEFAULT_PREVIEW_ROWS]]

        header_idx = detect_header_from_lines(lines)

        df = pd.read_csv(
            path,
            sep=";",
            encoding="cp1252",
            skiprows=header_idx,
            engine="python",
            index_col=False,
        )

        df = pd.read_csv(
            path,
            sep=";",
            encoding="cp1252",
            skiprows=header_idx,
            engine="python",
            on_bad_lines="skip",
            index_col=False,
        )

        unnamed_cols = [col for col in df.columns if "Unnamed" in str(col)]
        unnamed_ratio = len(unnamed_cols) / len(df.columns)

        if unnamed_ratio > 0.5:
            # Header realmente não foi detectado — promove primeira linha
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)
        else:
            # Apenas remove colunas Unnamed extras (trailing semicolons)
            df = df.drop(columns=unnamed_cols)

        df["nome_arquivo"] = path.name

        if not df.columns.is_unique:
            new_cols = []
            counts = {}
            for col in df.columns:
                col_str = str(col)
                if col_str in counts:
                    counts[col_str] += 1
                    new_cols.append(f"{col_str}_{counts[col_str]}")
                else:
                    counts[col_str] = 0
                    new_cols.append(col_str)
            df.columns = new_cols

        return df

    def _load_excel(self, path: Path) -> pd.DataFrame:
        """
        Robust Excel loader with reliable header detection.
        """
        # 1. Carregamos uma prévia do Excel (sem cabeçalho) para análise
        # Lemos apenas as primeiras linhas definidas no seu preview
        preview_df = pd.read_excel(path, header=None, nrows=self.DEFAULT_PREVIEW_ROWS)

        # 2. Convertemos as linhas do DataFrame em strings separadas por ";"
        # para reutilizar seu detector que espera esse formato.
        lines = []
        for _, row in preview_df.iterrows():
            # Converte cada célula para string, remove espaços e junta com ";"
            line_str = ";".join([str(val).strip() if pd.notna(val) else "" for val in row])
            lines.append(line_str)

        # 3. Agora o seu detector vai funcionar porque as 'lines' são strings formatadas
        header_idx = detect_header_from_lines(lines)

        # 4. Lê o arquivo completo pulando as linhas até o cabeçalho detectado
        df = pd.read_excel(path, skiprows=header_idx)

        # 1. Remove linhas onde a primeira coluna é vazia
        coluna_chave = df.columns[0]
        df = df.dropna(subset=[coluna_chave])

        # 2. Converte o número do documento para inteiro (para tirar o .0 do 44340.0)
        # Só fazemos isso se a coluna for numérica
        try:
            df[coluna_chave] = df[coluna_chave].astype(float).astype(int)
        except Exception:
            pass  # Caso haja algum texto perdido, ele mantém como está

        # 3. Reset do index para a contagem ficar limpa (0, 1, 2, 3...)
        df = df.reset_index(drop=True)

        # 5. Sua lógica de limpeza para colunas "Unnamed"
        if any("Unnamed" in str(col) for col in df.columns):
            # Garante que não estamos pegando uma linha vazia como header
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)

        df["nome_arquivo"] = path.name

        return df

    # =========================
    # Transformation Layer
    # =========================
    def _merge_dataframes(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        if not dfs:
            return pd.DataFrame()

        if len(dfs) == 1:
            return dfs[0].copy()

        reference_columns = self._pick_reference_columns(dfs)

        normalized = []
        for df in dfs:
            # Alinha nomes de colunas (case-insensitive + strip)
            col_map = {}
            for col in df.columns:
                col_normalized = str(col).strip().lower()
                for ref in reference_columns:
                    if col_normalized == str(ref).strip().lower():
                        col_map[col] = ref
                        break
            df = df.rename(columns=col_map)

            # Preenche colunas ausentes e descarta excedentes
            for col in reference_columns:
                if col not in df.columns:
                    df[col] = pd.NA

            normalized.append(df[reference_columns])

        return pd.concat(normalized, ignore_index=True)

    # =========================
    # Output Layer
    # =========================

    def _save_output(self, df: pd.DataFrame, output_dir: str) -> Path:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        final_path = self._generate_unique_filename(output_path, "CONSOLIDADO", ".xlsx")

        df.to_excel(final_path, index=False)
        return final_path

    def _generate_unique_filename(self, directory: Path, base_name: str, extension: str) -> Path:
        """
        Logic:
        1. Try 'CONSOLIDADO.xlsx'
        2. If exists, try 'CONSOLIDADO_1.xlsx'
        3. If exists, try 'CONSOLIDADO_2.xlsx' ...
        """
        # First attempt: no suffix
        candidate = directory / f"{base_name}{extension}"
        if not candidate.exists():
            return candidate

        # Subsequent attempts: add _1, _2, etc.
        counter = 1
        while True:
            candidate = directory / f"{base_name}_{counter}{extension}"
            if not candidate.exists():
                return candidate
            counter += 1
