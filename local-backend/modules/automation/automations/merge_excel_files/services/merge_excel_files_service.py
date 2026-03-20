from pathlib import Path
from typing import List

import pandas as pd


class MergeExcelFilesService:
    """
    Service responsible for merging CSV/XLSX files into a single Excel file.
    """

    DEFAULT_PREVIEW_ROWS = 20
    MIN_NON_NULL_THRESHOLD = 2

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
                elif extension in (".xlsx", ".xls"):
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

        header_idx = self._detect_header_from_lines(lines)

        df = pd.read_csv(
            path,
            sep=";",
            encoding="cp1252",
            skiprows=header_idx,
            engine="python",
            on_bad_lines="skip",
            index_col=False,
        )

        if any("Unnamed" in str(col) for col in df.columns):
            # First row is likely the real header
            df.columns = df.iloc[0]
            df = df[1:].reset_index(drop=True)

        return df

    def _load_excel(self, path: Path) -> pd.DataFrame:
        """
        Robust Excel loader with reliable header detection.
        """

        def reader(**kwargs):
            return pd.read_excel(path, header=None, **kwargs)

        preview = reader(nrows=self.DEFAULT_PREVIEW_ROWS)
        header_idx = self._detect_header_from_preview(preview)

        return reader(skiprows=header_idx)

    def _detect_header_from_lines(self, lines: List[str]) -> int:
        """
        Detect header using both delimiter density and semantic content.
        """

        if not lines:
            raise ValueError("File is empty.")

        parsed_lines = [line.split(";") for line in lines]

        scores = []

        for idx, cols in enumerate(parsed_lines):
            # Clean values
            cleaned = [c.strip() for c in cols]

            # Count meaningful cells (not empty)
            non_empty = [c for c in cleaned if c]

            non_empty_count = len(non_empty)

            # Count "text-like" cells (header tends to be text, not numbers)
            text_cells = [c for c in non_empty if not c.replace(",", "").replace(".", "").isdigit()]
            text_ratio = len(text_cells) / non_empty_count if non_empty_count else 0

            # Final score
            score = non_empty_count * text_ratio

            scores.append((idx, score))

        # Pick row with highest score
        best_idx, best_score = max(scores, key=lambda x: x[1])

        if best_score == 0:
            raise ValueError("Could not detect a valid header row.")

        return best_idx

    # =========================
    # Transformation Layer
    # =========================

    def _merge_dataframes(self, dfs: List[pd.DataFrame]) -> pd.DataFrame:
        if not dfs:
            raise ValueError("No data found to merge.")
        # sort=False maintains column order from the first file loaded
        return pd.concat(dfs, ignore_index=True, sort=False)

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
