from modules.automation.application.usecases.cancelled_invoices_usecase import (
    CancelledInvoicesUseCase,
)
from modules.automation.application.usecases.merge_excel_files_usecase import (
    MergeExcelFilesUseCase,
)
from modules.automation.automations.cancelled_tax_invoices.navigation.browser_session import (
    BrowserSession,
)
from modules.automation.automations.cancelled_tax_invoices.navigation.navigate_to_report import (
    NavigateToReport,
)
from modules.automation.automations.cancelled_tax_invoices.orchestrator.get_cancelled_report_orchestrator import (
    GetCancelledReportOrchestrator,
)
from modules.automation.automations.cancelled_tax_invoices.services.download_report_service import (
    DownloadReportService,
)
from modules.automation.automations.merge_excel_files.services.merge_excel_files_service import (
    MergeExcelFilesService,
)
from modules.automation.automations.state.automation_state import AutomationState
from modules.automation.utils.selenium_driver import SeleniumDriver
from shared.application.usecases.branch.create_branch import (
    CreateBranchUseCase,
)
from shared.application.usecases.branch.delete_branch import (
    DeleteBranchUseCase,
)
from shared.application.usecases.branch.find_branch import (
    FindBranchUseCase,
)
from shared.application.usecases.branch.list_all_branches import (
    ListAllBranchesUseCase,
)
from shared.application.usecases.branch.update_branch import (
    UpdateBranchUseCase,
)
from shared.application.usecases.branch_group.add_branch_in_group import AddBranchInGroupUseCase
from shared.application.usecases.branch_group.create_group import (
    CreateBranchGroupUseCase,
)
from shared.application.usecases.branch_group.find_branch_group import FindBranchGroupUseCase
from shared.application.usecases.branch_group.list_groups import (
    ListGroupsUseCase,
)
from shared.application.usecases.company.create_company import (
    CreateCompanyUseCase,
)
from shared.application.usecases.company.delete_company import (
    DeleteCompanyUseCase,
)
from shared.application.usecases.company.find_company import (
    FindCompanyUseCase,
)
from shared.application.usecases.company.list_companies import (
    ListCompaniesUseCase,
)
from shared.application.usecases.company.update_company import (
    UpdateCompanyUseCase,
)
from shared.infrastructure.queries.company_query_service import (
    CompanyQueryService,
)
from shared.infrastructure.queries.group_query_service import (
    GroupQueryService,
)
from shared.infrastructure.repositories.sqlite_branch_groups_repository import (
    BranchGroupRepository,
)
from shared.infrastructure.repositories.sqlite_branch_repository import (
    BranchRepository,
)
from shared.infrastructure.repositories.sqlite_company_repository import (
    CompanyRepository,
)

automation_state = AutomationState()


def get_browser_session(driver: SeleniumDriver):
    return BrowserSession(driver)


def get_navigate_to_report(driver: SeleniumDriver):
    return NavigateToReport(driver)


def get_download_report(driver: SeleniumDriver):
    return DownloadReportService(driver)


def get_get_cancelled_report_orchestrator(driver: SeleniumDriver):
    return GetCancelledReportOrchestrator(
        get_browser_session(driver),
        get_navigate_to_report(driver),
        get_download_report(driver),
    )


def get_merge_excel_files_service():
    return MergeExcelFilesService()


def get_merge_excel_files_usecase():
    return MergeExcelFilesUseCase(get_merge_excel_files_service())


def get_cancelled_invoices_usecase(driver: SeleniumDriver):
    return CancelledInvoicesUseCase(
        get_get_cancelled_report_orchestrator(driver),
    )


# Repositories
def get_company_repository():
    return CompanyRepository()


def get_branch_repository():
    return BranchRepository()


def get_branch_group_repository():
    return BranchGroupRepository()


# Queries
def get_company_query_service():
    return CompanyQueryService()


def get_group_query_service():
    return GroupQueryService()


# Usecases
def get_create_branch_usecase():
    branch_repo = get_branch_repository()
    company_repo = get_company_repository()

    return CreateBranchUseCase(
        branch_repo=branch_repo,
        company_repo=company_repo,
    )


def get_delete_branch_usecase():
    repo = get_branch_repository()

    return DeleteBranchUseCase(repo)


def get_find_branch_usecase():
    repo = get_branch_repository()

    return FindBranchUseCase(repo)


def get_list_all_branches_usecase():
    branch_repo = get_branch_repository()
    company_repo = get_company_repository()

    return ListAllBranchesUseCase(
        branch_repo=branch_repo,
        company_repo=company_repo,
    )


def get_update_branch_usecase():
    repo = get_branch_repository()
    return UpdateBranchUseCase(repo)


def get_add_branch_in_group_usecase():
    branch_repo = get_branch_repository()
    group_repo = get_branch_group_repository()

    return AddBranchInGroupUseCase(branch_repo=branch_repo, group_repo=group_repo)


def get_create_branch_group_usecase():
    repo = get_branch_group_repository()
    return CreateBranchGroupUseCase(repo)


def get_find_branch_group_usecase():
    repo = get_branch_group_repository()
    return FindBranchGroupUseCase(repo)


def get_list_groups_usecase():
    query = get_group_query_service()
    return ListGroupsUseCase(query)


def get_create_company_usecase():
    repo = get_company_repository()
    return CreateCompanyUseCase(repo)


def get_delete_company_usecase():
    repo = get_company_repository()
    return DeleteCompanyUseCase(repo)


def get_find_company_usecase():
    repo = get_company_repository()
    return FindCompanyUseCase(repo)


def get_update_company_usecase():
    repo = get_company_repository()
    return UpdateCompanyUseCase(repo)


def get_list_companies_usecase():
    repo = get_company_repository()
    return ListCompaniesUseCase(repo)
