import nazm as a
import nazm.capture as c
import time
from time import sleep

class BookStateService:

    def is_open(self, book_type, filial, start_date):

        company = "2" if int(filial) >= 70 else "1"
        start_date = start_date.replace("/", "")

        print(f"[STATE] Checking if book is open | filial={filial}")
        t = c.load_templates()

        a.click(t.binoculos)

        # Navigate to and fill company field
        a.press('tab')
        #sleep(0.2)
        a.double_press('shift', 'tab')
        #sleep(0.2)
        a.type(company)
        #sleep(0.2)
        
        # Fill branch field
        a.press('tab')
        #sleep(0.2)
        a.type(filial)
        
        # Navigate to date field
        a.press('tab', presses=2)
        # Extract month/year (last 6 digits of date)
        month_year = start_date[-6:]
        a.type(month_year)
        
        # Select book type
        a.press('tab')
        if book_type == "entrada":
            a.press('up', presses=2)
        else:
            a.press('up', presses=1)
        
        # Execute search
        a.press('f8')

        
        # Check if closed book icon is visible (wait up to 2 seconds)
        timeout = 5.0 
        check_interval = 0.3
        start_time = time.time()
        
        # Definimos as escalas como apenas a original para ganhar velocidade total
        # Se o ícone não muda de tamanho na tela, 1.0 é tudo que você precisa.
        fast_params = {
            "timeout": 0,          # Faz o nazm checar apenas uma vez por chamada
            "poll_interval": 0     # Remove qualquer espera interna da lib
        }

        state = True # Valor default caso nada seja encontrado
        while time.time() - start_time < timeout:

            # 2. Verifica Closed com parâmetros ultra-rápidos
            if a.exists(t.closedbook, **fast_params):
                print("[STATUS] Livro fechado encontrado.")
                state = False
                break

            # 1. Verifica Pending com parâmetros ultra-rápidos
            if a.exists(t.pendingbook, **fast_params):
                print("[STATUS] Livro pendente encontrado.")
                state = True
                break
                
                
            time.sleep(check_interval)

        return state