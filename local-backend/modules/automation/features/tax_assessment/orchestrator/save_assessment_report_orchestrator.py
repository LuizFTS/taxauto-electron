from pathlib import Path

import nazm as a

from modules.automation.features.state.automation_state import AutomationState
from modules.automation.features.tax_assessment.services.save_pdf import SavePDF
from modules.automation.features.tax_assessment.navigation import Navigation 

from modules.automation.infrastructure.erp_session import ERPSession


class SaveAssessmentReportOrchestrator:
    def __init__(
        self,
        session: ERPSession,
        state: AutomationState,
        save_pdf: SavePDF,
        navigator: Navigation
    ):
        self.session = session
        self.state = state

        self.save_pdf = save_pdf
        self.navigator = navigator

    def execute(self, dto):

        print("[ORCHESTRATOR] Starting saving assessment reports automation")

        self.state.check()
        
        self.session.open()
        self.state.check()

        self.navigator.execute("OBFI0460")
        self.state.check()

        first_round = True

        for filial in dto.filiais:
            print(f"[ORCHESTRATOR] Processing filial {filial}")
            self.state.check()

            file_name = f"{str(filial).zfill(2)}_APURACAO_{dto.date.replace('/', '')[2:]}"
            pdf_path = Path(dto.save_path) / f"{file_name}.pdf"

            self.save_pdf.execute(
                filial=filial,
                date=dto.date,
                save_path=str(pdf_path),
                first_round=first_round,
            )
            self.state.check()
            first_round = False

        a.double_press("ctrl", "q")