from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de PostgreSQL
POSTGRES_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

try:
    # Crear el engine
    engine = create_engine(POSTGRES_URL)
    
    # Probar la conexión
    with engine.connect() as connection:
        print("Conexión exitosa!")
        
        # Obtener todas las tablas del esquema público
        result = connection.execute(text("""
            SELECT tablename 
            FROM pg_tables 
            WHERE schemaname = 'public'
        """))
        
        tables = result.fetchall()
        if tables:
            print("Tablas existentes:", [table[0] for table in tables])

            # Eliminar todas las tablas
            for table in tables:
                table_name = table[0]
                print(f"Eliminando tabla: {table_name}")
                connection.execute(text(f"DROP TABLE IF EXISTS {table_name} CASCADE"))
            print("Todas las tablas han sido eliminadas.")
        else:
            print("No hay tablas para eliminar.")

except Exception as e:
    print(f"Error: {e}")
