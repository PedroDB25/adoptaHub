import logging
import json
import requests
from bs4 import BeautifulSoup
from shared.model.Protectora import Protectora
import re

class BuscadorProtectorasUseCase:
    def __init__(self):
        pass

    def execute(self):
        porComunidadJSON = self.cargarDatos()
        protectoras = self.abrirPorComunidad(porComunidadJSON)
        self.escribirFichero(protectoras)

    def cargarDatos(self) -> dict:
        logging.debug("cargarDatos() called")
        with open(r"resources\porComunidad.json", encoding="utf-8") as file:
           return json.load(file)


    def abrirPorComunidad(self, porComunidadJSON: dict):
        logging.debug("abrirPorComunidad() called")
        map_protectoras = {}
        id_protectora = 0
        rutaBase = porComunidadJSON["link"]
        for comunidad in porComunidadJSON["links"]:
            list_comunidades = []
            ruta =rutaBase + porComunidadJSON["links"][comunidad]
            llamada = requests.get(ruta, timeout=5)
            soup = BeautifulSoup(llamada.text, 'html.parser')
            nodos = soup.select("section.backgroundcolor-white:first-child div.uk-section-small ul.uk-list li")
            for li in nodos:
                protectora = Protectora()
                protectora.number = id_protectora
                protectora.name = li.select("b")[0].text
                self.ordenar_links(li.select("a"), protectora) # ordenar los links
                protectora.comunidad_autonoma = comunidad
                list_comunidades.append(protectora)
                id_protectora += 1
            # Convertir objeto a diccionario
            dict_list = [model.dict() for model in list_comunidades]
            map_protectoras[comunidad] = dict_list

        return map_protectoras
    
    def ordenar_links(self, links, protectora: Protectora):
        for link in links:
            if re.match(r".+@.+\..+", link.text):
                protectora.mailto = link.text.split("/")[0].strip()
            elif re.match(r"[\d ]+", link.text):
                protectora.phone = link.text
            elif re.match   (r"(http)*s*(://)*(www\.)*[a-zA-Z-]+\.[a-zA-Z]+[.]*", link.text):
                if "facebook" in link.text:
                    protectora.facebook = link.text
                else: 
                    protectora.web = link.text
    
    def escribirFichero(self, map_protectoras):
        logging.debug("escribirFichero() called")
        with open(r"page\resources\js\protectoras.json", "w", encoding="utf-8") as file:
            json.dump(map_protectoras, file, ensure_ascii=False, indent=4)
