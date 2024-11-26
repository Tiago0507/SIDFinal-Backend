from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import os

load_dotenv()

# PostgreSQL Configuration
POSTGRES_URL = f"postgresql://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_SERVER')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"

try:
    # Crear el engine
    engine = create_engine(POSTGRES_URL)
    
    # Probar la conexión
    with engine.connect() as connection:
        print("Conexión exitosa!")
        
        # Verificar tablas existentes
        result = connection.execute(text("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """))
        
        tables = result.fetchall()
        print("Tablas existentes:", tables)

except Exception as e:
    print(f"Error: {e}")