class BookStateService:

    def is_open(self, session, filial, book_type):

        print(f"[STATE] Checking if book is open | filial={filial}")

        # inspect ERP UI

        return False