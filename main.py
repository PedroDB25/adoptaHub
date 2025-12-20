import logging
from sections.buscadorMascotas.application.buscadorMascotasUseCase import BuscadorMascotasUseCase
from sections.buscadorProtectoras.application.buscarorProtectorasUseCase import BuscadorProtectorasUseCase
from sections.copiarAPage.application.copiarAPage import CopiarAPage
from shared.helpers.loggingHelper import LogginHelper

BUSCARPROTECTORAS = False
BUSCARMASCOTAS = True
COPIARAPAGE = False


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
    if BUSCARPROTECTORAS:
        logging.debug("Starting buscar protectoras")
        main.bp.execute()
    if BUSCARMASCOTAS:
        logging.debug("Starting buscar mascotas")
        main.bm.execute()
    if COPIARAPAGE:
        logging.debug("Starting copiar a page")
        main.cp.execute()

