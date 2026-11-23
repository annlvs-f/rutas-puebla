"""Carga paradas de ejemplo en Redis Cloud.

Uso (con el entorno virtual activado, desde la carpeta rutas-puebla):
    python seed.py

Es seguro correrlo varias veces: si una parada ya existe, la omite.
Las coordenadas son aproximadas y las rutas son datos de ejemplo
para pruebas, no información oficial del transporte de Puebla.
"""

from app.database import redis_client
from app.models import Parada

PARADAS = [
    Parada(id="pue-001", nombre="Parada Zócalo", colonia="Centro",
           latitud=19.0431, longitud=-98.1937,
           rutas=["Ruta 1", "Ruta 15", "Ruta 72"]),
    Parada(id="pue-002", nombre="Parada BUAP", colonia="Los Volcanes",
           latitud=19.0467, longitud=-98.2065,
           rutas=["Ruta 4", "Ruta 61"]),
    Parada(id="pue-003", nombre="Parada CAPU", colonia="Amalucan",
           latitud=19.0722, longitud=-98.2147,
           rutas=["Ruta 10", "Ruta 22", "Ruta 40"]),
    Parada(id="pue-004", nombre="Parada Paseo Bravo", colonia="Centro",
           latitud=19.0376, longitud=-98.2019,
           rutas=["Ruta 3", "Ruta 15"]),
    Parada(id="pue-005", nombre="Parada Angelópolis", colonia="Lomas de Angelópolis",
           latitud=19.0300, longitud=-98.2335,
           rutas=["Ruta 8", "Ruta 72"]),
    Parada(id="pue-006", nombre="Parada Fuertes de Loreto", colonia="Centro Histórico",
           latitud=19.0586, longitud=-98.1883,
           rutas=["Ruta 1", "Ruta 22"], activa=False),
]


def main():
    creadas = 0
    for parada in PARADAS:
        clave = f"parada:{parada.id}"
        if redis_client.exists(clave):
            print(f"- {clave} ya existe, se omite")
            continue
        redis_client.set(clave, parada.model_dump_json())
        creadas += 1
        print(f"+ {clave} creada ({parada.nombre})")
    print(f"\nListo: {creadas} paradas nuevas, {len(PARADAS) - creadas} omitidas.")


if __name__ == "__main__":
    main()
