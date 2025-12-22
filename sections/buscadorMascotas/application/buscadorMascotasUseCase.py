import logging
import json
import requests
import os
from pathlib import Path
import shutil
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from sections.buscadorMascotas.model.mascota import Mascota
from shared.model.Protectora import Protectora


class BuscadorMascotasUseCase:
    def __init__(self):
        logging.debug("BuscadorMascotasUseCase initialized")

    def execute(self):
        logging.debug("BuscadorMascotasUseCase executed")
        self.limpiarCarpetaImagenes()  # Limpiar la carpeta de imágenes al iniciar
        protectorasComunidadJSON = self.cargarDatos()
        mascotas = self.leerProtectoras(protectorasComunidadJSON)
        self.generarJsonMascotas(mascotas)

    # cargar en memoria las protectoras
    def cargarDatos(self) -> dict:
        logging.debug("cargarDatos() called")
        with open(r"resources/protectoras.json", encoding="utf-8") as file:
            return json.load(file)

    # leer cada protectora
    def leerProtectoras(self, protectorasComunidadJSON):
        logging.debug("leerProtectoras() called")
        mascotas = {}
        for comunidad in protectorasComunidadJSON:
            for protectora in protectorasComunidadJSON[comunidad]:
                # Protectora

                protectoraClase: Protectora = Protectora.from_dict(protectora)
                if (protectoraClase.web) and protectoraClase.paginas:
                    mascotas[protectoraClase.name] = self.obtenerMascotas(protectoraClase)

        return mascotas

    def obtenerMascotas(self, protectora: Protectora):
        number = 0
        ListaDeMascotas = []
        if protectora.number == 14:
            for pagina in protectora.paginas:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                llamada = requests.get(
                    protectora.web + pagina, timeout=5, headers=headers)
                soup = BeautifulSoup(llamada.text, 'html.parser')
                nodos = soup.select(".uk-tile")
                for div in nodos:
                    #sex y age
                    if len(div.contents[1].contents) == 8 :
                        raza = div.contents[1].contents[2]
                        sex = div.contents[1].contents[4]
                        age = div.contents[1].contents[6]
                    elif len(div.contents[1].contents) == 7:
                        raza = None
                        sex = div.contents[1].contents[3]
                        age = div.contents[1].contents[5]
                    elif len(div.contents[1].contents) == 6:
                        raza = None
                        sex = None
                        age = div.contents[1].contents[4]

                    # Descargar la imagen y obtener la ruta local
                    ruta_imagen_local = self.guardarImagenLocal(
                        protectora.web + div.a.img.get("src"), protectora.name)

                    

                    mascota = Mascota(number=number,
                            name=div.contents[1].span.text,
                            image=ruta_imagen_local,
                            raza = raza,
                            sex=sex,
                            age= age,
                            comunidadAutonoma=protectora.comunidad_autonoma,
                            protectora=protectora.name,
                            link = protectora.web + div.a.get("href"))
                    number += 1
                    ListaDeMascotas.append(mascota)
        
        if protectora.number == 15:
            return  # Tienen Facebook

        if protectora.number == 16:
            for pagina in protectora.paginas:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
                llamada = requests.get(
                    protectora.web + pagina, timeout=5, headers=headers)
                soup = BeautifulSoup(llamada.text, 'html.parser')
                nodos = soup.select("td a img")

                for img in nodos:
                    # Descargar la imagen y obtener la ruta local
                    ruta_imagen_local = self.guardarImagenLocal(
                        img.get("src"), protectora.name)

                    mascota = Mascota(number=number,
                            name=img.get("alt"),
                            image=ruta_imagen_local,
                            comunidadAutonoma=protectora.comunidad_autonoma,
                            protectora=protectora.name,
                            link = img.get("src"))
                    number += 1
                    ListaDeMascotas.append(mascota)

            


        
        dict_list = [model.dict() for model in ListaDeMascotas]
        return dict_list
    
    def generarJsonMascotas(self, mapMascotas):
        logging.debug("escribirFichero() called")
        with open(r"resources/mascotas.json", "w", encoding="utf-8") as file:
            json.dump(mapMascotas, file, ensure_ascii=False, indent=4)
    
    def guardarImagenLocal(self, url_imagen: str, protectora_nombre: str) -> str:
        """
        Descarga la imagen desde la URL y la guarda en una carpeta local dentro de 'resources/images'.
        Retorna la ruta local de la imagen.
        """
        try:
            # Crear la carpeta para las imágenes si no existe
            carpeta_imagenes = Path(f"resources/images/{protectora_nombre}")
            carpeta_imagenes.mkdir(parents=True, exist_ok=True)

            # Obtener el nombre del archivo desde la URL
            nombre_archivo = os.path.basename(urlparse(url_imagen).path)
            ruta_local = carpeta_imagenes / nombre_archivo

            # Descargar la imagen y guardarla localmente
            headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
                }
            response = requests.get(url_imagen, stream=True, timeout=10, headers=headers)
            if response.status_code == 200:
                with open(ruta_local, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)
                return str(ruta_local)
            else:
                logging.warning(f"No se pudo descargar la imagen: {url_imagen}")
                return None
        except Exception as e:
            logging.error(f"Error al guardar la imagen {url_imagen}: {e}")
            return None
        
    def limpiarCarpetaImagenes(self):
            """
            Elimina la carpeta 'resources/images' y todo su contenido si existe.
            """
            carpeta_imagenes = Path("resources/images")
            if carpeta_imagenes.exists() and carpeta_imagenes.is_dir():
                try:
                    shutil.rmtree(carpeta_imagenes)  # Eliminar la carpeta y su contenido
                    logging.info("Carpeta 'resources/images' eliminada correctamente.")
                except Exception as e:
                    logging.error(f"Error al eliminar la carpeta 'resources/images': {e}")
