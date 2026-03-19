from fastapi import APIRouter, status

from core.di.container import get_merge_excel_files_usecase
from modules.automation.application.dto.merge_excel_files_dto import MergeExcelFilesDTO

router = APIRouter()


@router.post("/merge-excel-files/run", status_code=status.HTTP_204_NO_CONTENT)
def merge_excel_files(data: MergeExcelFilesDTO):
    usecase = get_merge_excel_files_usecase()
    usecase.execute(data)
