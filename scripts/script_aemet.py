import os
import json
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv
import requests

load_dotenv()
API_KEY_AEMET = os.getenv("API_KEY_AEMET")

CARPETA_DESTINO = Path(
    r"C:\Users\Jorge Esteban Garcia\Desktop\BIG DATA\bigdata-p4-urbano\data\raw"
)


def acceso_api():
    url = "https://opendata.aemet.es/opendata/api/observacion/convencional/datos/estacion/8416/"
    headers = {"api_key": API_KEY_AEMET}
    response = requests.get(url, headers=headers)
    return response.json()


def obtener_datos(enlace):
    response = requests.get(enlace)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al obtener los datos: {response.status_code}")
        return None


def guardar_json(datos, carpeta=CARPETA_DESTINO):
    carpeta.mkdir(parents=True, exist_ok=True)
    fecha = datetime.now().strftime("%Y-%m-%d")
    ruta = carpeta / f"aemet_valencia_{fecha}.json"
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, ensure_ascii=False, indent=2)
    print(f"Guardado en: {ruta}")
    return ruta


if __name__ == "__main__":
    enlaces = acceso_api()
    enlace_datos = enlaces.get("datos")

    if not enlace_datos:
        print(f"La API no devolvió enlace de datos: {enlaces}")
    else:
        datos = obtener_datos(enlace_datos)
        if datos is not None:
            guardar_json(datos)