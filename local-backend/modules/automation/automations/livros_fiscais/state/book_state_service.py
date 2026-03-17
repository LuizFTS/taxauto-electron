import time

import nazm as a
import nazm.capture as c


class BookStateService:
    def __init__(self):
        self.t = c.load_templates()

    def is_open(self, book_type, filial, start_date):

        company = "2" if int(filial) >= 70 else "1"
        start_date = start_date.replace("/", "")

        print(f"[STATE] Checking if book is open | filial={filial}")

        a.press("f7")

        # Navigate to and fill company field
        a.press("tab")
        # sleep(0.2)
        a.double_press("shift", "tab")
        # sleep(0.2)
        a.type(company)
        # sleep(0.2)

        # Fill branch field
        a.press("tab")
        # sleep(0.2)
        a.type(filial)

        # Navigate to date field
        a.press("tab", presses=2)
        # Extract month/year (last 6 digits of date)
        month_year = start_date[-6:]
        a.type(month_year)

        # Select book type
        a.press("tab")
        if book_type == "entrada":
            a.press("up", presses=2)
        else:
            a.press("up", presses=1)

        # Execute search
        a.press("f8")
        time.sleep(1)

        # Check if closed book icon is visible (wait up to 2 seconds)
        timeout = 3.0
        start_time = time.time()

        state = True  # Valor default caso nada seja encontrado
        while time.time() - start_time < timeout:
            # 2. CAPTURA ÚNICA (O segredo da velocidade)
            # Use o método de captura mais rápido que você tiver

            # 3. Compara os dois na mesma imagem de memória

            if a.element_exists(self.t.closedbook):
                print("Fechado!")
                return False

            if a.element_exists(self.t.pendingbook):
                print("Pendente!")
                return True

            time.sleep(0.01)

        print("[TIMEOUT] Nenhum estado identificado.")
        return state
