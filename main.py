import logging
from sections.buscadorMascotas.application.buscadorMascotasUseCase import BuscadorMascotasUseCase
from sections.buscadorProtectoras.application.buscarorProtectorasUseCase import BuscadorProtectorasUseCase
from sections.copiarAPage.application.copiarAPage import CopiarAPage
from shared.helpers.loggingHelper import LogginHelper

BUSCARPROTECTORAS = 0
BUSCARMASCOTAS = 1
COPIARAPAGE = 0


class main:
    def __init__(self):
        LogginHelper()
        logging.debug("main initialized")
        self.bp = BuscadorProtectorasUseCase()
        self.bm = BuscadorMascotasUseCase()
        self.cp = CopiarAPage()
        pass



if __name__ == "__main__":
    main = main()
    if BUSCARPROTECTORAS == 1:
        main.bp.execute()
    if BUSCARMASCOTAS == 1:
        main.bm.execute()
    if COPIARAPAGE == 1:
        main.cp.execute()

