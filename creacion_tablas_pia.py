import sys
import sqlite3 
from sqlite3 import Error

#crear tablas
try:
    with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
        mi_cursor=conn.cursor()
        mi_cursor.execute("PRAGMA foreign_keys = 1")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            CLIENTES (clave_cliente INTEGER NOT NULL PRIMARY KEY, cliente TEXT NOT NULL, RFC TEXT NOT NULL,  correo TEXT);")
        print("Tabla clientes creada")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            SERVICIOS (id_servicio INTEGER NOT NULL PRIMARY KEY, nombre_servicio TEXT NOT NULL, costo_servicio INTEGER NOT NULL);")
        print("Tabla servicios creada")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            NOTAS (folio INTEGER NOT NULL PRIMARY KEY, fecha TIMESTAMP, estatus TEXT NOT NULL, monto_promedio INTEGER NOT NULL, monto_pago INTEGER NOT NULL, clave_cliente INT NOT NULL, FOREIGN KEY (clave_cliente) REFERENCES CLIENTES(clave_cliente));")
        print("Tabla creada")
        mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
            SERVICIOS_NOTAS (folio INTEGER NOT NULL PRIMARY KEY, id_servicio INTEGER NOT NULL,  FOREIGN KEY (folio) REFERENCES NOTAS(folio),  FOREIGN KEY (id_servicio) REFERENCES SERVICIOS(id_servicio))")
        print("Tabla creada")

except Error as e:
    print(e)
except Exception:
    print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
conn.commit()
conn.close()