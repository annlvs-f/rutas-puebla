# 🚌 Rutas Puebla — Sprint 1

API REST + interfaz web para administrar paradas de transporte público de la ciudad de Puebla (CRUD).

| Elemento | Definición |
|----------|------------|
| Producto | API REST “Rutas Puebla” |
| Entidad | Parada |
| Base de datos | Redis Cloud (clave-valor / JSON) |
| Lenguaje | Python 3.11+ |
| Framework | FastAPI |
| Cliente Redis | redis-py |
| Frontend | HTML, CSS y JavaScript (Fetch API) + Leaflet / OpenStreetMap |

Alumna: Angela Paulina Sánchez Zapata — Universidad Tecnológica de Puebla.

## Historias de usuario cubiertas

- HU-01: registrar una parada con nombre, colonia, coordenadas y rutas.
- HU-02: consultar una parada por su ID.
- HU-03: listar todas las paradas.
- HU-04: actualizar los datos de una parada.
- HU-05: eliminar una parada obsoleta.
- HU-06: los datos se guardan en Redis Cloud, no en el equipo local.

## Modelo de datos

Cada parada se guarda en Redis con la clave `parada:{id}` (ejemplo: `parada:pue-001`) como documento JSON:

```json
{
  "id": "pue-001",
  "nombre": "Parada Zócalo",
  "colonia": "Centro",
  "municipio": "Puebla",
  "latitud": 19.0431,
  "longitud": -98.1937,
  "rutas": ["Ruta 1", "Ruta 15", "Ruta 72"],
  "activa": true,
  "creado_en": "2026-11-18T23:00:00Z"
}
```

## Endpoints

| Método | Ruta | Acción |
|--------|------|--------|
| POST | /paradas | Crear parada |
| GET | /paradas | Listar paradas |
| GET | /paradas/{id} | Obtener una parada |
| PUT | /paradas/{id} | Actualizar parada |
| DELETE | /paradas/{id} | Eliminar parada |
| GET | /estado | Verifica la conexión con Redis (PING) |

Errores: `404` si la parada no existe, `409` si el ID ya existe al crear, `422` si los datos no son válidos.

## Instalación y ejecución

### 1. Redis Cloud

1. Crea una cuenta en <https://redis.io/cloud/> y una base de datos (el plan gratuito basta).
2. En la base de datos, abre **Connect** y copia el endpoint, el usuario (`default`) y la contraseña.
3. La base empieza vacía: Redis no necesita tablas, las claves se crean al registrar paradas.

### 2. Entorno virtual y dependencias

```bash
cd rutas-puebla
python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1
# Linux / macOS
source venv/bin/activate

pip install -r requirements.txt
```

Si PowerShell bloquea la activación: `Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned`.

### 3. Variable de entorno

Copia `.env.example` como `.env` (en la raíz del proyecto) y escribe tu cadena de conexión:

```
REDIS_URL=redis://default:TU_PASSWORD@TU_HOST:PUERTO
```

- Usa `rediss://` solo si tu base tiene TLS activado; si no, `redis://`.
- Si la contraseña tiene `@`, `#`, `/` o `:`, codifícalos (`%40`, `%23`, `%2F`, `%3A`).
- El `.env` está en `.gitignore`: **nunca lo subas al repositorio**.

### 4. Ejecutar

```bash
python -m uvicorn app.main:app --reload
```

- Interfaz web: <http://127.0.0.1:8000/>
- Swagger: <http://127.0.0.1:8000/docs>
- Estado de Redis: <http://127.0.0.1:8000/estado> → `"redis_conectado": true`

### 5. Datos de ejemplo (opcional)

```bash
python seed.py
```

Carga 6 paradas de ejemplo (IDs `pue-001` a `pue-006`). Se puede correr varias veces sin duplicar. Las coordenadas son aproximadas y las rutas son ficticias, solo para pruebas.

## Pruebas

- **Manuales:** sigue `docs/PRUEBAS_MANUALES.md` (tabla con casos, resultados esperados y espacio para capturas).
- **Automática de respaldo:** con el servidor corriendo, en otra terminal:

```bash
python pruebas_crud.py
```

Debe terminar con `11/11 pruebas correctas`.

## Criterios de aceptación

- [x] Se puede crear una parada y obtener un ID único.
- [x] Se puede consultar una parada por ID.
- [x] Se pueden listar todas las paradas almacenadas.
- [x] Se puede actualizar una parada existente.
- [x] Se puede eliminar una parada.
- [x] La API responde con errores claros si la parada no existe.
- [x] La conexión usa Redis Cloud mediante la variable de entorno `REDIS_URL`.
- [x] Redis responde correctamente con PING.

## Estructura del proyecto

```
rutas-puebla/
├── app/
│   ├── main.py          # App FastAPI, CORS, archivos estáticos
│   ├── database.py      # Conexión a Redis Cloud
│   ├── models.py        # Modelo Parada (Pydantic)
│   └── routes.py        # CRUD de paradas
├── static/
│   ├── index.html       # Interfaz web
│   ├── styles.css
│   └── app.js           # Lógica del CRUD y mapa Leaflet
├── docs/
│   └── PRUEBAS_MANUALES.md
├── seed.py              # Datos de ejemplo
├── pruebas_crud.py      # Prueba automática de los 5 endpoints
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Siguiente sprint (propuesta)

Búsqueda por colonia, filtro por ruta y geolocalización (paradas cercanas) usando las capacidades geoespaciales de Redis.
