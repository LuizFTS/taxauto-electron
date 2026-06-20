from fastapi import APIRouter, status

from core.di.container import get_download_xmls_usecase
from modules.automation.application.dto.download_xmls_dto import DownloadXmlsDTO

router = APIRouter()


@router.post("/download-xmls/run", status_code=status.HTTP_204_NO_CONTENT)
def download_xmls(data: DownloadXmlsDTO):
    usecase = get_download_xmls_usecase()
    usecase.execute(data)
