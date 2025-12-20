import logging
import json
import requests
from bs4 import BeautifulSoup
from sections.buscadorMascotas.model.mascota import Mascota
from shared.model.Protectora import Protectora


class BuscadorMascotasUseCase:
    def __init__(self):
        logging.debug("BuscadorMascotasUseCase initialized")

    def execute(self):
        logging.debug("BuscadorMascotasUseCase executed")
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



                    mascota = Mascota(number=number,
                            name=div.contents[1].span.text,
                            image=protectora.web + div.a.img.get("src"),
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

                    mascota = Mascota(number=number,
                            name=img.get("alt"),
                            image=img.get("src"),
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
