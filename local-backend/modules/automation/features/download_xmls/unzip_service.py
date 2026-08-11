import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path
from zipfile import ZipFile


class UnzipService:
    def corrigir_extensao_se_necessario(self, path):
        path = Path(path)

        if not path.exists():
            raise FileNotFoundError(f"Arquivo não encontrado: {path}")

        if zipfile.is_zipfile(path):
            if path.suffix.lower() != ".zip":
                novo_path = path.with_suffix(".zip")
                path.rename(novo_path)
                return novo_path, "zip"
            return path, "zip"

        try:
            ET.parse(path)
            if path.suffix.lower() != ".xml":
                novo_path = path.with_suffix(".xml")
                path.rename(novo_path)
                return novo_path, "xml"
            return path, "xml"
        except ET.ParseError:
            return path, "desconhecido"

    def execute(self, file_path: str):
        path_corrigido, tipo_real = self.corrigir_extensao_se_necessario(file_path)

        zip_file = Path(path_corrigido)

        # file_path without file, just the folder
        extract_dir = file_path.replace(zip_file.name, "")

        if tipo_real == "zip":
            with ZipFile(zip_file, "r") as zip_ref:
                zip_ref.extractall(extract_dir)

        zip_file.unlink()
