from pathlib import Path
from zipfile import ZipFile


class UnzipService:
    def execute(self, file_path: str):
        zip_file = Path(file_path)
        if not zip_file.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

        extract_dir = zip_file.with_suffix("")

        extract_dir.mkdir(exist_ok=True)

        with ZipFile(zip_file, "r") as zip_ref:
            zip_ref.extractall(extract_dir)

        zip_file.unlink()
