from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from modules.automation.automations.state.automation_state import AutomationStoppedException


def register_exception_handlers(app: FastAPI) -> None:
    """
    Registers global exception handlers for application errors.
    """

    @app.exception_handler(ValueError)
    async def value_error_handler(request: Request, exc: ValueError):
        """
        Handles validation or business rule errors raised in use cases.
        """
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(LookupError)
    async def lookup_error_handler(request: Request, exc: LookupError):
        """
        Handles entity-not-found situations.
        """
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(AutomationStoppedException)
    async def automation_interrupt_handler(request: Request, exc: AutomationStoppedException):
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Automacao interrompida pelo usuário", "code": "AUTOMATION_STOPPED"},
        )

    @app.exception_handler(Exception)
    async def generic_exception_handler(request: Request, exc: Exception):
        """
        Fallback handler for unexpected errors.
        Prevents leaking internal stack traces to the client.
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"detail": "Internal server error"},
        )
