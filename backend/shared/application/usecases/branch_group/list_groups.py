import logging
from typing import Any

from shared.infrastructure.queries.group_query_service import GroupQueryService

logger = logging.getLogger(__name__)


class ListGroupsUseCase:
    """
    Use case responsible for retrieving all branch groups along with
    their associated branches using a query service.
    """

    def __init__(self, query: GroupQueryService):
        # Defensive validation to avoid runtime errors if dependency injection fails
        if query is None:
            raise ValueError("GroupQueryService cannot be None")

        self.query = query

    async def execute(self) -> Any:
        """
        Retrieves all groups with their associated branches.

        Returns:
            Any: Structure returned by the query service containing groups
                 and their branches.

        Raises:
            RuntimeError: If the query service returns an invalid result.
        """

        result = await self.query.list_groups_with_branches()

        # Defensive validation: ensure the query service does not return None
        # which could propagate unexpected errors to the caller.
        if result is None:
            raise RuntimeError("Query service returned no data for groups")

        logger.info("Grupos de filiais listados")

        return result
