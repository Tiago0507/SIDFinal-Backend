![ICESI University Logo](https://res.cloudinary.com/dxhi8xsyb/image/upload/v1731991202/ICESI_logo_prin_descriptor_RGB_POSITIVO_0924_bszq4w.png)

# Backend de Aplicación de Arrendamiento de Equipos Tecnológicos

## Miembros
- Juan David Calderón Salamanca
- Santiago Escobar León
- Santiago Valencia García

## Descripción

Este backend es parte de una aplicación web diseñada para una empresa de servicios de tecnología que permite a sus clientes ver los equipos que tienen alquilados y registrar nuevas solicitudes de arrendamiento. El sistema se conecta a una base de datos PostgreSQL donde se almacenan los contratos de arrendamiento, los clientes y los equipos disponibles para arrendar.

### Funcionalidades Principales:

1. **Ver equipos alquilados**: Los clientes pueden visualizar los contratos de arrendamiento vigentes, que incluyen detalles sobre los equipos que tienen en alquiler.
2. **Registrar solicitudes de arrendamiento**: Los clientes pueden consultar los equipos disponibles por categoría, con detalles como foto, descripción, precio y características.
3. **Manejo de productos tecnológicos**: El sistema soporta diversas categorías de productos (portátiles, impresoras, tablets, entre otros) con atributos específicos para cada tipo de equipo.

## Requisitos

Para ejecutar este backend, debes tener un entorno de Python configurado y las siguientes dependencias instaladas:

### Dependencias

- **fastapi==0.115.5**
- **uvicorn==0.32.1**
- **sqlalchemy==2.0.36**
- **psycopg2-binary==2.9.10**
- **motor==3.6.0**
- **python-jose==3.3.0**
- **passlib==1.7.4**
- **python-multipart==0.0.17**
- **python-dotenv==1.0.1**
- **pydantic==2.10.2**
- **bcrypt==4.0.1**
- **email-validator==2.2.0**

---

## Instalación

### 1. Crear un entorno virtual

Para crear y activar un entorno virtual en tu sistema, sigue estos pasos:

1. Abre una terminal o línea de comandos.
2. Navega hasta el directorio del proyecto.
3. Crea un entorno virtual con el siguiente comando:

   ```bash
   python -m venv venv
   ```

4. Activa el entorno virtual:
   - **Windows**:

     ```bash
     .\venv\Scripts\activate
     ```

   - **Linux/macOS**:

     ```bash
     source venv/bin/activate
     ```

### 2. Instalar dependencias

Una vez activado el entorno virtual, instala las dependencias del proyecto con:

```bash
pip install -r requirements.txt
```

El archivo `requirements.txt` debe contener lo siguiente:

```bash
fastapi==0.115.5
uvicorn==0.32.1
sqlalchemy==2.0.36
psycopg2-binary==2.9.10
motor==3.6.0
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.17
python-dotenv==1.0.1
pydantic==2.10.2
bcrypt==4.0.1
email-validator==2.2.0
```

---

## Ejecución del backend

Para iniciar el servidor backend, ejecuta el siguiente comando desde la raíz del proyecto:

```bash
uvicorn app.main:app --reload
```

Esto ejecutará el servidor FastAPI en modo de desarrollo (con recarga automática).

## Estructura del Proyecto

El backend sigue la siguiente estructura de carpetas:

```
.
├── app/
│   ├── __init__.py
│   ├── config/
│   ├── core/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   └── dependencies.py
│   └── main.py
├── doc/
├── requirements.txt
└── README.md
```

- **app/**: Contiene los archivos principales del backend.
  - **config/**: Define las configuraciones de base de datos.
  - **core/**: Define las configuraciones de autenticación.
  - **models/**: Define los modelos de base de datos.
  - **routes/**: Contiene los controladores de las rutas (endpoints).
  - **schemas/**: Define los esquemas de validación de datos (Pydantic).

---

## Desarrollado con 🛠️

<div style="text-align: left">
    <p>
        <a href="https://fastapi.tiangolo.com/" target="_blank"> <img alt="FastAPI" src="https://cdn.svgporn.com/logos/fastapi.svg" height="60" width="60"> </a>
        <a href="https://www.postgresql.org/" target="_blank"> <img alt="PostgreSQL" src="https://cdn.svgporn.com/logos/postgresql.svg" height="60" width="60"> </a>
        <a href="https://www.mongodb.com/" target="_blank"> <img alt="MongoDB" src="https://cdn.svgporn.com/logos/mongodb.svg" height="60" width = "60"></a>
        <a href="https://www.python.org/" target="_blank"> <img alt="Python" src="https://cdn.svgporn.com/logos/python.svg" height="60" width="60"> </a>
    </p>
</div>

---

## Contribuciones

Si deseas contribuir al proyecto, por favor sigue estos pasos:

1. Haz un fork del repositorio.
2. Crea una nueva rama para tu característica (`git checkout -b feature/nueva-funcionalidad`).
3. Realiza tus cambios y haz commit de ellos (`git commit -am 'Agrega nueva funcionalidad'`).
4. Haz push a tu rama (`git push origin feature/nueva-funcionalidad`).
5. Abre un pull request.
