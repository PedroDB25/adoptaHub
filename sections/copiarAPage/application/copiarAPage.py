import os
import shutil

class CopiarAPage:
    def __init__(self):
        self.rutaMascotas = None
        self.rutaPretectoras = None
        

    def execute(self):
        #buscar fichero de mascotas y protectoras de la carpeta "resources"
        self.buscarFicheros()

        #copiar a carpeta resources "page\resources\js"
        self.copiarFicheros()

    def buscarFicheros(self):
        #buscar fichero de mascotas y protectoras de la carpeta "resources"
        if "mascotas.json" in os.listdir("resources"):
            self.rutaMascotas = r"resources\mascotas.json"
        if "protectoras.json" in os.listdir("resources"):
            self.rutaPretectoras = r"resources\protectoras.json"

    
    def copiarFicheros(self):
        """
        This method is used to copy files from one location to another.
        It moves the 'mascotas' file from 'resources' to 'page/resources/js'.
        """

        shutil.copy(self.rutaMascotas, 'page/resources/js') if self.rutaMascotas else ""
        shutil.copy(self.rutaPretectoras, 'page/resources/js') if self.rutaPretectoras else ""

a = CopiarAPage()
a.execute()