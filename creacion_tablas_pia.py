import sys
import sqlite3 
from sqlite3 import Error

#crear tablas
try:
    with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
        mi_cursor=conn.cursor()
        mi_cursor.execute("PRAGMA foreign_keys = 1")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            CLIENTES (RFC TEXT NOT NULL PRIMARY KEY, cliente TEXT NOT NULL, correo TEXT);")
        print("Tabla clientes creada")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            SERVICIOS (id_servicio INTEGER NOT NULL PRIMARY KEY, nombre_servicio TEXT NOT NULL, costo_servicio INTEGER NOT NULL);")
        print("Tabla servicios creada")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            NOTAS (FOLIO INTEGER NOT NULL PRIMARY KEY, fecha TIMESTAMP, estatus TEXT NOT NULL, monto_promedio INTEGER NOT NULL, monto_pago INTEGER NOT NULL, RFC TEXT NOT NULL, FOREIGN KEY (RFC) REFERENCES CLIENTES(RFC));")
        print("Tabla creada")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            SERVICIOS_NOTAS (folio INTEGER NOT NULL PRIMARY KEY, ID_SERVICIO INTEGER NOT NULL,  FOREIGN KEY (folio) REFERENCES NOTAS(folio),  FOREIGN KEY (ID_SERVICIO) REFERENCES SERVICIOS(ID_SERVICIO))")
        print("Tabla creada")

except Error as e:
    print(e)
except Exception:
    print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
conn.commit()
conn.close()

#funcion para crear tablas (aun no implementada)
def crear_tablas():
    try:
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            mi_cursor=conn.cursor()
            mi_cursor.execute("PRAGMA foreign_keys = 1")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
                CLIENTES (RFC TEXT NOT NULL PRIMARY KEY, cliente TEXT NOT NULL, correo TEXT);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
                SERVICIOS (id_servicio INTEGER NOT NULL PRIMARY KEY, nombre_servicio TEXT NOT NULL, costo_servicio INTEGER NOT NULL);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
                NOTAS (FOLIO INTEGER NOT NULL PRIMARY KEY, fecha TIMESTAMP, estatus TEXT NOT NULL, monto_promedio INTEGER NOT NULL, monto_pago INTEGER NOT NULL, RFC TEXT NOT NULL, FOREIGN KEY (RFC) REFERENCES CLIENTES(RFC));")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
                SERVICIOS_NOTAS (folio INTEGER NOT NULL PRIMARY KEY, ID_SERVICIO INTEGER NOT NULL,  FOREIGN KEY (folio) REFERENCES NOTAS(folio),  FOREIGN KEY (ID_SERVICIO) REFERENCES SERVICIOS(id_servicio))")
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    conn.commit()
    conn.close()
