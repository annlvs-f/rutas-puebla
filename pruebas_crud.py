"""Prueba automática de los 5 endpoints del CRUD (solo librería estándar).

1. Deja corriendo el servidor:  python -m uvicorn app.main:app --reload
2. En otra terminal (con el venv activado):  python pruebas_crud.py

Crea una parada temporal (pue-prueba-001), la consulta, la lista, la
actualiza, la elimina y verifica que ya no exista. Al final no deja datos.
"""

import json
import sys
import urllib.error
import urllib.request

BASE = "http://127.0.0.1:8000"
ID = "pue-prueba-001"

resultados = []


def llamar(metodo, ruta, cuerpo=None):
    datos = json.dumps(cuerpo).encode() if cuerpo is not None else None
    peticion = urllib.request.Request(
        BASE + ruta, data=datos, method=metodo,
        headers={"Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(peticion) as r:
            return r.status, json.loads(r.read() or b"null")
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"null")


def verificar(nombre, condicion, detalle=""):
    estado = "OK " if condicion else "FALLA"
    resultados.append(condicion)
    print(f"[{estado}] {nombre} {detalle}")


def main():
    try:
        codigo, estado = llamar("GET", "/estado")
    except urllib.error.URLError:
        print("No se pudo conectar. ¿Está corriendo uvicorn en el puerto 8000?")
        sys.exit(1)

    verificar("PING a Redis (/estado)", estado.get("redis_conectado") is True)

    # Limpieza por si una corrida anterior quedó a medias
    llamar("DELETE", f"/paradas/{ID}")

    parada = {
        "id": ID,
        "nombre": "Parada de prueba",
        "colonia": "Centro",
        "municipio": "Puebla",
        "latitud": 19.0414,
        "longitud": -98.2063,
        "rutas": ["Ruta 1", "Ruta 15"],
        "activa": True,
    }

    codigo, resp = llamar("POST", "/paradas", parada)
    verificar("POST /paradas (crear)", codigo == 201 and resp.get("id") == ID, f"-> {codigo}")

    codigo, _ = llamar("POST", "/paradas", parada)
    verificar("POST duplicado devuelve 409", codigo == 409, f"-> {codigo}")

    codigo, resp = llamar("GET", f"/paradas/{ID}")
    verificar("GET /paradas/{id} (obtener)", codigo == 200 and resp["nombre"] == "Parada de prueba", f"-> {codigo}")

    codigo, resp = llamar("GET", "/paradas")
    ids = [p["id"] for p in resp.get("paradas", [])]
    verificar("GET /paradas (listar)", codigo == 200 and ID in ids, f"-> {codigo}, total={resp.get('total')}")

    cambios = dict(parada, nombre="Parada de prueba EDITADA", activa=False)
    codigo, resp = llamar("PUT", f"/paradas/{ID}", cambios)
    verificar("PUT /paradas/{id} (actualizar)", codigo == 200, f"-> {codigo}")

    codigo, resp = llamar("GET", f"/paradas/{ID}")
    verificar("La actualización se guardó", resp.get("nombre") == "Parada de prueba EDITADA" and resp.get("activa") is False)

    codigo, _ = llamar("PUT", "/paradas/no-existe", cambios)
    verificar("PUT a ID inexistente devuelve 404", codigo == 404, f"-> {codigo}")

    codigo, _ = llamar("DELETE", f"/paradas/{ID}")
    verificar("DELETE /paradas/{id} (eliminar)", codigo == 200, f"-> {codigo}")

    codigo, resp = llamar("GET", f"/paradas/{ID}")
    verificar("GET tras eliminar devuelve 404", codigo == 404 and "no encontrada" in str(resp.get("detail", "")).lower(), f"-> {codigo}")

    codigo, _ = llamar("DELETE", f"/paradas/{ID}")
    verificar("DELETE repetido devuelve 404", codigo == 404, f"-> {codigo}")

    print(f"\n{sum(resultados)}/{len(resultados)} pruebas correctas")
    sys.exit(0 if all(resultados) else 1)


if __name__ == "__main__":
    main()
