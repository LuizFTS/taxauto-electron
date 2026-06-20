import os
import shutil
from pathlib import Path

import nazm as a
import nazm.capture as c
import pandas as pd

from modules.automation.features.merge_excel_files.merge_excel_files_service import (
    MergeExcelFilesService,
)
from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_reports.services.save_pdf import SavePDF
from modules.automation.features.tax_reports.services.save_spreadsheet import (
    SaveSpreadsheet,
)
from modules.automation.infrastructure.erp_session import ERPSession


class SaveBooksOrchestrator:
    def __init__(
        self,
        session: ERPSession,
        state: AutomationState,
        merge_spreadsheets: MergeExcelFilesService,
        save_pdf: SavePDF,
        save_spreadsheet: SaveSpreadsheet,
    ):
        self.session = session
        self.state = state

        self.save_pdf = save_pdf
        self.save_spreadsheet = save_spreadsheet
        self.merge_spreadsheets = merge_spreadsheets

    def execute(self, dto):

        print("[ORCHESTRATOR] Starting saving books automation")
        t = c.load_templates()

        a.click(t.livro_printer)
        self.state.check()
        a.wait_cursor_normal()

        first_round = True

        if dto.tasks.save_pdf:
            for filial in dto.filiais:
                print(f"[ORCHESTRATOR] Processing filial {filial}")
                self.state.check()

                file_name = f"{str(filial).zfill(2)}_{dto.book_type.upper()}"
                pdf_path = Path(dto.save_path) / f"{file_name}.pdf"

                self.save_pdf.execute(
                    filial=filial,
                    book_type=dto.book_type,
                    start_date=dto.start_date,
                    end_date=dto.end_date,
                    save_path=str(pdf_path),
                    first_round=first_round,
                )
                self.state.check()
                first_round = False

        first_round = True
        if dto.tasks.save_spreadsheet:
            companies = []

            # Check if in the list of filiais has values bellow 70
            has_values_bellow_70 = any(int(filial) < 70 for filial in dto.filiais)
            if has_values_bellow_70:
                companies.append(1)

            # Check if in the list of filiais has values above 70
            has_values_above_70 = any(int(filial) > 70 for filial in dto.filiais)
            if has_values_above_70:
                companies.append(2)

            """
            If it has values above 70 it means that has branches of company 2
            if it has values bellow 70 it means that has branches of company 1

            So for save_spreadsheet service we won't iterate for all branches, but
            for the company instead
            """
            temp_dirs = []

            # remove all folders and files inside root_temp_dir

            base_dir = os.getenv("LOCALAPPDATA")

            if base_dir is None:
                raise Exception("Nenhum diretório de armazenamento encontrado.")
            else:
                temp_dir = os.path.join(base_dir, "TaxAuto", "Temp")
            os.makedirs(temp_dir, exist_ok=True)

            for item in os.listdir(temp_dir):
                item_path = os.path.join(temp_dir, item)
                if os.path.isfile(item_path):
                    os.remove(item_path)
                elif os.path.isdir(item_path):
                    shutil.rmtree(item_path)

            for company in companies:
                file_path = self.save_spreadsheet.execute(
                    company=company,
                    book_type=dto.book_type,
                    start_date=dto.start_date,
                    end_date=dto.end_date,
                    first_round=first_round,
                )

                if file_path:
                    temp_dirs.append(file_path)

                first_round = False
                self.state.check()

            a.double_press("ctrl", "q")
            a.double_press("ctrl", "q")

            # Get the base directory from the first temp_dir

            merged_path = None
            if len(temp_dirs) == 1:
                merged_path = temp_dirs[0]
            else:
                try:
                    print(temp_dir)
                    self.merge_spreadsheets.execute(temp_dirs, str(temp_dir))
                    merged_path = Path(temp_dir) / "CONSOLIDADO.xlsx"
                except Exception as e:
                    print(f"[ERROR] Merge failed: {e}")

            if merged_path:
                """
                Now that all spreadsheets are merged, we need to filter the branches that the user selected
                We need to use pandas to read the merged spreadsheet and filter the branches that the user selected.
                The branches are in the column "Filial" and the values are like "001", "002", etc.
                We need to filter the rows where the "Filial" column is in the list of filiais that the user selected.
                """
                if len(temp_dirs) == 1:
                    df = pd.read_csv(
                        merged_path,
                        sep=";",
                        encoding="cp1252",
                        skiprows=2,
                        on_bad_lines="skip",
                        index_col=False,
                    )
                    print(df)
                    print("=====================")
                    df = pd.read_csv(
                        merged_path,
                        sep=";",
                        encoding="cp1252",
                        skiprows=2,
                        engine="python",
                        on_bad_lines="skip",
                        index_col=False,
                    )

                    print(df)
                    print("=====================")

                    unnamed_cols = [col for col in df.columns if "Unnamed" in str(col)]
                    unnamed_ratio = len(unnamed_cols) / len(df.columns)

                    if unnamed_ratio > 0.5:
                        # Header realmente não foi detectado — promove primeira linha
                        df.columns = df.iloc[0]
                        df = df[1:].reset_index(drop=True)
                    else:
                        # Apenas remove colunas Unnamed extras (trailing semicolons)
                        df = df.drop(columns=unnamed_cols)

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
                else:
                    df = pd.read_excel(merged_path)
                df.columns = [col.strip() for col in df.columns]

                # convert filial column to string(int(filial))
                df["Filial"] = df["Filial"].apply(lambda x: str(int(x)))

                # convert filiais list to string(int(filial))
                dto.filiais = [str(int(filial)) for filial in dto.filiais]

                df_filtered = df[df["Filial"].isin(dto.filiais)]

                df_filtered["Filial"] = df_filtered["Filial"].apply(lambda x: int(x))

                df_filtered = df_filtered.sort_values(by="Filial")

                filtered_merged_path = Path(temp_dir) / "CONSOLIDADO_FILTERED.xlsx"
                df_filtered.to_excel(filtered_merged_path, index=False)

                # Copy of the merged spreadsheet to the save_path
                shutil.copy(
                    filtered_merged_path,
                    Path(dto.save_path)
                    / f"{dto.book_type.upper()}_{dto.start_date.replace('/', '')}_{dto.end_date.replace('/', '')}.xlsx",
                )

                # Remove the temp directory
                shutil.rmtree(temp_dir)
