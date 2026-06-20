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

# Repositories
_company_repo = CompanyRepository()
_branch_repo = BranchRepository()
_branch_group_repo = BranchGroupRepository()

# Queries
_company_query_service = CompanyQueryService()
_group_query_service = GroupQueryService()


# Usecases
def get_create_branch_usecase():
    return CreateBranchUseCase(
        branch_repo=_branch_repo,
        company_repo=_company_repo,
    )


def get_delete_branch_usecase():

    return DeleteBranchUseCase(_branch_repo)


def get_find_branch_usecase():

    return FindBranchUseCase(_branch_repo)


def get_list_all_branches_usecase():

    return ListAllBranchesUseCase(
        branch_repo=_branch_repo,
        company_repo=_company_repo,
    )


def get_update_branch_usecase():
    return UpdateBranchUseCase(_branch_repo)


def get_add_branch_in_group_usecase():

    return AddBranchInGroupUseCase(branch_repo=_branch_repo, group_repo=_branch_group_repo)


def get_create_branch_group_usecase():
    return CreateBranchGroupUseCase(_branch_group_repo)


def get_find_branch_group_usecase():
    return FindBranchGroupUseCase(_branch_group_repo)


def get_list_groups_usecase():
    return ListGroupsUseCase(_group_query_service)


def get_create_company_usecase():
    return CreateCompanyUseCase(_company_repo)


def get_delete_company_usecase():
    return DeleteCompanyUseCase(_company_repo)


def get_find_company_usecase():
    return FindCompanyUseCase(_company_repo)


def get_update_company_usecase():
    return UpdateCompanyUseCase(_company_repo)


def get_list_companies_usecase():
    return ListCompaniesUseCase(_company_repo)
