from pathlib import Path

import pandas as pd


class MergeExcelFilesService:

    def execute(self, paths: list[str], output_path: str):
        df = self.load_and_merge_csvs(paths)
        self.save_merged(paths, df, output_path)

    def load_and_merge_csvs(self, paths: list[str]) -> pd.DataFrame:
        dfs = []

        # Get extension from path
        extension = Path(paths[0]).suffix

        for path in paths:
            if extension == ".csv":
                df = pd.read_csv(
                    path,
                    sep=";",
                    encoding="cp1252",
                    skiprows=2,  # ajuste conforme seu caso
                    engine="python",  # mais tolerante
                    on_bad_lines="warn",  # evita crash
                    index_col=False,
                )
            elif extension == ".xlsx":
                df = pd.read_excel(
                    path,
                    skiprows=2,  # ajuste conforme seu caso
                    engine="python",  # mais tolerante
                    on_bad_lines="warn",  # evita crash
                    index_col=False,
                )
            dfs.append(df)

        merged_df = pd.concat(dfs, ignore_index=True)
        return merged_df

    def save_merged(self, paths: list[str], df: pd.DataFrame, output_path: str):
        output_path = Path(output_path)
        # Define merged filename
        output_path = output_path / "CONSOLIDADO.xlsx"

        # Save merged file
        df.to_excel(output_path, index=False)
