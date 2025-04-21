import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión
SERVER = os.getenv("SERVER")
DATABASE = os.getenv("BD")
USERNAME = os.getenv("USUARIO")
PASSWORD = os.getenv("PASSWORD")

if not all([SERVER, DATABASE, USERNAME, PASSWORD]):
    raise ValueError("Faltan variables de entorno necesarias para la conexión a la base de datos.")

# Crear motor de conexión
engine = create_engine(
    f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}?driver=ODBC+Driver+18+for+SQL+Server&TrustServerCertificate=yes"
)


def execute_stored_procedure(proc_name, params=None):
    try:
        with engine.connect().execution_options(autocommit=True) as conn:
            cursor = conn.connection.cursor()
            
            # Construir la consulta con parámetros, si los hay
            if params:
                placeholders = ", ".join(["?" for _ in params])
                query = f"EXEC {proc_name} {placeholders}"
                cursor.execute(query, tuple(params.values()))
            else:
                query = f"EXEC {proc_name}"
                cursor.execute(query)
            
            # Avanzar hasta encontrar un conjunto de resultados con descripción
            while cursor.description is None:
                if not cursor.nextset():
                    break
            
            # Obtener la descripción y las filas sin transformarlas
            description = cursor.description
            rows = cursor.fetchall()
            #convertir tupla a lista
            rows = [list(row) for row in rows]
            #convertir lista a dataframe
            rows = pd.DataFrame(rows, columns=[col[0] for col in description])

            return rows

    except Exception as e:
        print("Error al ejecutar el procedimiento almacenado:", e)
        return None



if __name__ == "__main__":
    print(execute_stored_procedure("[dbo].[SP_REPORTE_SALUD_SEGURA_POWERBI_DETALLE_NEW]"))











