# Pruebas manuales — Sprint 1 “Rutas Puebla”

Alumna: Angela Paulina Sánchez Zapata
Fecha de pruebas: ____ / ____ / 2026

Las pruebas se hacen desde Swagger (`http://127.0.0.1:8000/docs`) o desde la interfaz web (`http://127.0.0.1:8000/`).
En cada caso, toma una captura de pantalla y pégala en la columna “Evidencia”.

## 0. Conexión

| # | Prueba | Cómo | Resultado esperado | Resultado obtenido | Evidencia |
|---|--------|------|--------------------|--------------------|-----------|
| 0 | PING a Redis | Abrir `/estado` | `{"proyecto":"Rutas Puebla","redis_conectado":true}` | | captura |

## 1. Los cinco endpoints

| # | Endpoint | Entrada | Resultado esperado | Código | Resultado obtenido | Evidencia |
|---|----------|---------|--------------------|--------|--------------------|-----------|
| 1 | POST /paradas | Cuerpo JSON de la sección “Datos de prueba” | `{"mensaje":"Parada creada","id":"..."}` | 201 | | captura |
| 2 | GET /paradas | — | `total` y lista con las paradas guardadas | 200 | | captura |
| 3 | GET /paradas/{id} | ID de la parada creada | JSON completo de esa parada | 200 | | captura |
| 4 | PUT /paradas/{id} | Mismo cuerpo con `"activa": false` | `{"mensaje":"Parada actualizada",...}` | 200 | | captura |
| 5 | DELETE /paradas/{id} | ID de la parada | `{"mensaje":"Parada eliminada","id":"..."}` | 200 | | captura |

## 2. Casos de error

| # | Prueba | Resultado esperado | Código | Resultado obtenido | Evidencia |
|---|--------|--------------------|--------|--------------------|-----------|
| 6 | GET /paradas/no-existe | `"Parada no encontrada"` | 404 | | captura |
| 7 | PUT /paradas/no-existe | `"Parada no encontrada"` | 404 | | captura |
| 8 | DELETE /paradas/no-existe | `"Parada no encontrada"` | 404 | | captura |
| 9 | POST con un `id` que ya existe | `"La parada ya existe"` | 409 | | captura |
| 10 | POST sin `nombre` o con latitud 500 | Error de validación | 422 | | captura |

## 3. Interfaz web

| # | Prueba | Resultado esperado | Resultado obtenido | Evidencia |
|---|--------|--------------------|--------------------|-----------|
| 11 | Registrar una parada con el formulario | Mensaje verde, aparece en lista y mapa | | captura |
| 12 | Botón “Editar” y “Actualizar” | Datos cargados en el formulario; cambios visibles en la lista | | captura |
| 13 | Botón “Ver en mapa” | El mapa se centra en la parada y abre su popup | | captura |
| 14 | Botón “Eliminar” | Pide confirmación; la parada desaparece de lista y mapa | | captura |

## 4. Persistencia en la nube (HU-06)

| # | Prueba | Resultado esperado | Resultado obtenido | Evidencia |
|---|--------|--------------------|--------------------|-----------|
| 15 | Abrir Redis Insight / Browser en Redis Cloud | Aparecen claves `parada:pue-...` con el JSON de cada parada | | captura |
| 16 | Detener y volver a iniciar el servidor | Las paradas siguen ahí (no se guardan en el equipo local) | | captura |

## Datos de prueba

```json
{
  "nombre": "Parada BUAP",
  "colonia": "Los Volcanes",
  "municipio": "Puebla",
  "latitud": 19.0467,
  "longitud": -98.2065,
  "rutas": ["Ruta 4", "Ruta 61"],
  "activa": true
}
```

## Prueba automática (opcional, como respaldo)

Con el servidor corriendo, en otra terminal:

```
python pruebas_crud.py
```

Debe terminar con `11/11 pruebas correctas`.

## Criterios de aceptación

- [ ] Se puede crear una parada y obtener un ID único.
- [ ] Se puede consultar una parada por ID.
- [ ] Se pueden listar todas las paradas almacenadas.
- [ ] Se puede actualizar una parada existente.
- [ ] Se puede eliminar una parada.
- [ ] La API responde con errores claros si la parada no existe.
- [ ] La conexión usa Redis Cloud mediante la variable de entorno `REDIS_URL`.
- [ ] Redis responde correctamente con PING.
