from pathlib import Path

import pandas as pd


class MergeBooksService:

    def execute(self, paths: list[str], book_type: str):
        df = self.load_and_merge_csvs(paths)
        self.save_merged(paths, df, book_type)

    def load_and_merge_csvs(self, paths: list[str]) -> pd.DataFrame:
        dfs = []

        for path in paths:
            df = pd.read_csv(
                path,
                sep=";",
                encoding="cp1252",
                skiprows=2,  # ajuste conforme seu caso
                engine="python",  # mais tolerante
                on_bad_lines="warn",  # evita crash
                index_col=False,
            )
            dfs.append(df)

        merged_df = pd.concat(dfs, ignore_index=True)
        return merged_df

    def save_merged(self, paths: list[str], df: pd.DataFrame, book_type: str):
        # Get first path
        first_path = Path(paths[0])

        # Remove filename → only directory
        directory = first_path.parent

        # Define merged filename
        output_path = directory / f"CONSOLIDADO_{book_type.upper()}.csv"

        # Save merged file
        df.to_csv(output_path, sep=";", index=False, encoding="cp1252")
