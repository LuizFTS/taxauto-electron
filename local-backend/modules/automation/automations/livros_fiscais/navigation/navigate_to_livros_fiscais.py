import nazm as a


class NavigateToLivrosFiscais:

    def execute(self):
        print("[NAVIGATION] Navigating to Livros Fiscais screen")
        # open ERP
        # login
        # navigate menu
        # open livros fiscais screen
        a.press('f9')
        a.type('OBFI0200', 0.001)
        a.press('enter')

        