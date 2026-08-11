from core.di.container import get_download_xmls_usecase
from modules.automation.application.dto.download_xmls_dto import DownloadXmlsDTO

data: DownloadXmlsDTO = DownloadXmlsDTO(
    start_date="01/07/2026",
    end_date="22/07/2026",
    filiais=["06"],
    save_path=r"C:\Users\lu9887091\OneDrive - Nutrien\Área de Trabalho\Nova pasta (6)",
    login="DEFIS_AUX20",
    password="lfT#1020304050",
    tipo_documento=1,
    tipo_operacao=1,
)

usecase = get_download_xmls_usecase()
usecase.execute(data)
