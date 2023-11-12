import pandas as pd
import re
import datetime
import os
import csv
import sqlite3
from sqlite3 import Error
from prettytable import PrettyTable
import sys

def menu_principal():
    while True:
        print("\n--- Menú Taller Mecánico ---")
        print("1. Notas")
        print("2. Clientes")
        print("3. Servicios")
        print("4. Estadísticas")
        print("5. Salir")
        op=int(input("Por favor escoja una opción: "))
        if op == 1:
            menu_notas()
        elif op == 2:
            menu_clientes()
        elif op == 3:
            menu_servicios()
        elif op==4:
            menu_estadisticas()
        elif op == 5:
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, elija una opción válida.")

def menu_notas():
    while True:
        print("\n--- Menú Taller Mecánico ---")
        print("1. Registrar una nota")
        print("2. Cancelar una nota")
        print("3. Recuperar una nota")
        print("4. Consultas y reportes")
        print("5. Volver al menú principal")
        opcion=int(input("Ingrese una opción: "))
        if opcion == 1:
            insertar_notas()
        elif opcion ==2:            
            cancelar_nota()
        elif opcion == 3:
            recuperar_nota_cancelada()    
        elif opcion == 4:
            menu_consultas_notas()
        elif opcion == 5:
            confirmacion_salida = input("¿Está seguro de que desea salir? (si/no): ")
            if confirmacion_salida.lower() == 'si':
                print("¡Hasta luego!")
                break
        else:
            print("Opción inválida. Por favor, elija una opción válida.")

def insertar_notas():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute(("SELECT clave_cliente, cliente FROM CLIENTES ORDER BY clave_cliente"))
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("Listado de clientes:\n")
                    print("Clave \t Nombre de cliente")
                    for clave, nombre in clientes:
                        print(f"\n{clave} \t {nombre}")
                    break
                else: 
                    print("No se encontraron coincidencias")
                    break
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT id_servicio, nombre_servicio, costo_servicio FROM SERVICIOS ORDER BY id_servicio")
                servicios = mi_cursor.fetchall()

                if servicios:
                    print("\nListado de servicios disponibles:\n")
                    print("Clave \t Nombre de servicio \t\t Costo")
                    for id_servicio, nombre_servicio, costo_servicio in servicios:
                        print(f"\n{id_servicio} \t {nombre_servicio} \t {costo_servicio}")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

        nota={}
        while True:
            try:
                fecha=datetime.datetime.strptime(input("Ingrese la fecha dd/mm/aaaa: "),"%d/%m/%Y").date()
                if fecha<datetime.datetime.today().date():
                    break
                else: 
                   print("Ingrese una fecha válida")  
            except ValueError:
                print("Ingrese una fecha válida")    
        
        while True:
            try:
                with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                    mi_cursor=conn.cursor()
                    while True:
                        cliente_clave_ingreso=int(input("Ingrese la clave del cliente: "))
                        if cliente_clave_ingreso:
                            valores_clie={"clave_cliente":cliente_clave_ingreso}
                            mi_cursor.execute("SELECT clave_cliente FROM CLIENTES WHERE clave_cliente=:clave_cliente", valores_clie)
                            cliente = mi_cursor.fetchone()
                            if cliente:
                                clave_cliente=cliente_clave_ingreso
                                break
                            else:
                                print("El cliente no está registrado")
                        else:
                            print("No se puede dejar vacío")
                    while True:
                        servicio_clave_ingreso=int(input("Ingrese la clave del servicio realizado: "))
                        if servicio_clave_ingreso:
                            clave=(servicio_clave_ingreso,)
                            mi_cursor.execute("SELECT costo_servicio FROM SERVICIOS WHERE id_servicio=?", clave)
                            servicios = mi_cursor.fetchone()
                            if servicios:
                                for costo_servicio in servicios:
                                    clave_servicio=servicio_clave_ingreso
                                    costo_servicio_insertar=costo_servicio
                                    break
                                break
                            else:
                                print("El servicio no existe")
                        else:
                            print("No se puede dejar vacío")  
            except Error as e:
                print (e)
            except Exception:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                conn.close()

            nota["Fecha"] = fecha
            nota["Estatus"] = 1
            nota["Monto_pago"] = costo_servicio
            nota["clave_cliente"] = clave_cliente
            nota["id_servicio"]=clave_servicio

            try:
                while True:
                    with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                        mi_cursor = conn.cursor()
                        mi_cursor.execute("INSERT INTO NOTAS (fecha, estatus, monto_pago, clave_cliente, id_servicio) VALUES\
                                        (:Fecha,:Estatus,:Monto_pago,:clave_cliente,:id_servicio)",nota)
                        print(f"Datos insertados correctamente \nEl folio de la nota es {mi_cursor.lastrowid}")
                        break
            except Error as e:
                    print (e)
            except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                    conn.commit()
                    conn.close()
                    menu_notas()
            

def cancelar_nota():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("""
                    SELECT N.FOLIO, N.FECHA, N.clave_cliente, C.cliente, C.RFC, C.correo, N.id_servicio, S.nombre_servicio, S.costo_servicio, N.monto_pago
                    FROM NOTAS N
                    INNER JOIN CLIENTES C ON N.clave_cliente=C.clave_cliente
                    INNER JOIN SERVICIOS S ON N.id_servicio=S.id_servicio
                    WHERE N.estatus=1
                """)
                notas = mi_cursor.fetchall()

                if notas:
                    print("NOTAS ENCONTRADAS:\n")
                    table = PrettyTable(["Folio", "Fecha", "Clave Cliente", "Cliente", "RFC", "Correo", "ID Servicio", "Nombre Servicio", "Costo Servicio", "Monto Pago Total"])
                    for folio, fecha, clave_c, nombre_c, rfc, correo, id_servicio, n_servicio, c_servicio, monto_p in notas:
                        table.add_row([folio, fecha, clave_c, nombre_c, rfc, correo, id_servicio, n_servicio, c_servicio, monto_p])
                    print(table)

                    print("¿Desea cancelar una nota?")
                    cancelar = input().upper()
                    if cancelar == "SI":
                        cancelar_folio = int(input("Ingrese el folio: "))
                        values = {"folio": cancelar_folio}
                        mi_cursor.execute("UPDATE NOTAS SET estatus=0 WHERE folio=:folio", values)
                        print("Nota cancelada con éxito.")
                    elif cancelar == "NO":
                        print("Volviendo al menú de consultas de notas")
                        menu_notas()
                else:
                    print("No se encontraron coincidencias")
                    menu_notas()
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def recuperar_nota_cancelada():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT FOLIO, FECHA, clave_cliente FROM NOTAS WHERE estatus=0")
                notas = mi_cursor.fetchall()
                
                if notas:
                    print("NOTAS ENCONTRADAS:\n")
                    table = PrettyTable(["Folio", "Fecha", "Clave del cliente"])
                    for folio, fecha, clave_cliente in notas:
                        table.add_row([folio, fecha, clave_cliente])
                    print(table)

                    print("¿Desea recuperar una nota?")
                    respuesta = input().upper()

                    if respuesta == "SI":
                        cancelar_folio = int(input("Ingrese el folio: "))
                        print(f"Los datos de la nota con el folio {cancelar_folio} son:")
                        mi_cursor.execute("""
                            SELECT N.FOLIO, N.FECHA, N.clave_cliente, C.cliente, C.RFC, C.correo, N.id_servicio, S.nombre_servicio, S.costo_servicio, N.monto_pago
                            FROM NOTAS N
                            INNER JOIN CLIENTES C ON N.clave_cliente=C.clave_cliente
                            INNER JOIN SERVICIOS S ON N.id_servicio=S.id_servicio
                            WHERE N.folio=? AND N.estatus=0
                        """, (cancelar_folio,))
                        nota = mi_cursor.fetchone()

                        if nota:
                            print("NOTA:\n")
                            table = PrettyTable(["Folio", "Fecha", "Clave del cliente", "Cliente", "RFC", "Correo", "ID Servicio", "Nombre del servicio", "Costo del servicio", "Monto de pago total"])
                            table.add_row([nota[0], nota[1], nota[2], nota[3], nota[4], nota[5], nota[6], nota[7], nota[8], nota[9]])
                            print(table)

                            res = input("¿Desea confirmar la recuperación? ").upper()

                            if res == "SI":
                                values = {"folio": cancelar_folio}
                                mi_cursor.execute("UPDATE NOTAS SET estatus=1 WHERE folio=:folio", values)
                                print("Nota recuperada exitosamente")
                            else:
                                print("La nota no fue recuperada\nVolviendo al menú de consultas de notas")
                                menu_notas()
                        else:
                            print("No se encontró ninguna nota con el folio ingresado.")
                            menu_notas()
                    elif respuesta == "NO":
                        print("La nota no fue recuperada\nVolviendo al menú de consultas de notas")
                        menu_notas()
                    else:
                        print("Opción no válida. Por favor, ingrese 'SI' o 'NO'.")
                else:
                    print("No se encontraron coincidencias")
                    menu_notas()
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def menu_consultas_notas():
            print("\n--- Submenú Consultas y Reportes ---")
            print("1. Consulta por período")
            print("2. Consulta por folio")
            print("3. Consulta por cliente")
            print("4. Regresa al menú principal")
            subopcion = input("Seleccione una opción: ")
            if subopcion == "1":
                consultar_por_periodo()
            elif subopcion == "2":
                consultar_por_folio()
            elif subopcion == "3":
                pass
               ## consultar_por_rfc()
            elif subopcion=="4":
                menu_principal()
            else:
                print("Opción inválida. Por favor, elija una opción válida.")

def consultar_por_periodo():
    try:
        fecha_inicial_str = input("Ingrese la fecha inicial dd/mm/aaaa (deje en blanco para usar 01/01/2000): ")
        if fecha_inicial_str.strip() == '':
            f_i = '1/1/2000'
            fecha_inicial = datetime.datetime.strptime(f_i, "%d/%m/%Y").date()
        else:
            fecha_inicial = datetime.datetime.strptime(fecha_inicial_str, "%d/%m/%Y").date()

        fecha_final_str = input("Ingrese la fecha final dd/mm/aaaa (deje en blanco para usar la fecha actual): ")
        if fecha_final_str.strip() == "":
            fecha_final = datetime.datetime.today().date()
        else:
            fecha_final = datetime.datetime.strptime(fecha_final_str, "%d/%m/%Y").date()

        if fecha_final < fecha_inicial:
            print("La fecha final debe ser igual o posterior a la fecha inicial.")
            return
    except ValueError:
        print("Fecha ingresada inválida.")
        return

    fechas = (fecha_inicial, fecha_final)

    try:
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT NOTAS.FOLIO, NOTAS.FECHA, NOTAS.clave_cliente, CLIENTES.cliente, CLIENTES.RFC, CLIENTES.correo,
                    NOTAS.monto_pago, SERVICIOS.nombre_servicio, SERVICIOS.costo_servicio
                FROM NOTAS
                INNER JOIN CLIENTES ON NOTAS.clave_cliente = CLIENTES.clave_cliente
                INNER JOIN SERVICIOS ON NOTAS.id_servicio = SERVICIOS.id_servicio
                WHERE NOTAS.estatus = 1 AND NOTAS.fecha BETWEEN ? AND ?
            """, fechas)

            notas = mi_cursor.fetchall()

            if notas:
                print("NOTAS ENCONTRADAS:\n")
                table = PrettyTable(["Folio", "Fecha", "Clave del cliente", "Cliente", "RFC", "Correo",
                                     "Monto de pago", "Servicio", "Costo del servicio"])
                for folio, fecha, clave_c, nombre_c, rfc, correo, monto_p, servicio, costo_servicio in notas:
                    table.add_row([folio, fecha, clave_c, nombre_c, rfc, correo, monto_p, servicio, costo_servicio])
                print(table)

                print("¿Desea preservar los datos en un archivo?")
                print("1. Exportar a Excel")
                print("2. Exportar a CSV")
                print("3. Regresar al menú de consultas")
                opcion = int(input("Elija la opción: "))

                if opcion == 1:
                    exportar_a_excel(notas)
                elif opcion == 2:
                    exportar_a_csv(notas)
                elif opcion == 3:
                    menu_consultas_notas()
            else:
                print("No se encontraron coincidencias")
                menu_reportes_servicios()

    except Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")
    finally:
        conn.close()

def consultar_por_folio():
    try:
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("""
                SELECT N.FOLIO, N.FECHA, C.cliente
                FROM NOTAS N
                INNER JOIN CLIENTES C ON N.clave_cliente = C.clave_cliente
                WHERE N.estatus = 1
            """)
            notas = mi_cursor.fetchall()

            if notas:
                print("NOTAS ENCONTRADAS:\n")
                table = PrettyTable(["Folio", "Fecha", "Cliente"])
                for folio, fecha, cliente in notas:
                    table.add_row([folio, fecha, cliente])
                print(table)

                folio_elegido = int(input("Ingrese el folio de la nota que desea consultar (o ingrese 0 para volver): "))

                if folio_elegido != 0:
                    valores = {"folio": folio_elegido}
                    mi_cursor.execute("""
                        SELECT NOTAS.FOLIO, NOTAS.FECHA, NOTAS.clave_cliente, CLIENTES.cliente, CLIENTES.RFC,
                            CLIENTES.correo, NOTAS.monto_pago, SERVICIOS.nombre_servicio, SERVICIOS.costo_servicio
                        FROM NOTAS
                        INNER JOIN CLIENTES ON NOTAS.clave_cliente = CLIENTES.clave_cliente
                        INNER JOIN SERVICIOS ON NOTAS.id_servicio = SERVICIOS.id_servicio
                        WHERE NOTAS.folio = :folio AND NOTAS.estatus = 1
                    """, valores)

                    nota = mi_cursor.fetchall()

                    if nota:
                        print("DETALLE DE LA NOTA:\n")
                        detalle_table = PrettyTable([
                            "Folio", "Fecha", "Clave del cliente", "Nombre del cliente", "RFC", "Correo",
                            "Monto de pago", "Nombre del servicio", "Costo del servicio"
                        ])
                        for folio, fecha, clave_c, nombre_c, rfc, correo, monto_p, servicio, costo_servicio in nota:
                            detalle_table.add_row([folio, fecha, clave_c, nombre_c, rfc, correo, monto_p, servicio, costo_servicio])
                        print(detalle_table)
                    else:
                        print("No se encontró ninguna nota con el folio ingresado.")
            else:
                print("No se encontraron notas registradas.")
    except Error as e:
        print(e)
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")
    finally:
        menu_consultas_notas()


def menu_clientes():
    while True:
        print("\n\t--- Menú Clientes ---")
        print("1. Agregar un cliente")
        print("2. Suspender un cliente")
        print("3. Recuperar un cliente")
        print("4. Consultas y reportes de clientes")
        print("5. Volver al menú anterior")
        eleccion=int(input("Elija una opción: "))
        if eleccion==1:
            agregar_cliente()
        elif eleccion==2:
            suspende_cliente()
        elif eleccion==3:
            recuperar_cliente()
        elif eleccion==4:
           menu_consultas_clientes()
        elif eleccion==5:
            menu_principal()
        else:
            print("Opción inválida")


def agregar_cliente():
    print("Agregar Cliente: \n")
    while True:
        rfc = input("Por favor, ingrese su RFC: ")
        validar_rfc(rfc)
        if validar_rfc(rfc):
            break
        else:
            print(f"RFC {rfc} no válido. Ingrese un RFC válido.")

    while True:  
        nombre = input("Ingresa el nombre completo del cliente: ")
        if nombre.strip()=="":
            print("No se puede dejar el campo vacío")
        else: 
            break

    while True:    
        correo = input("Ingresa un correo electrónico: ")
        if (correo.strip()==""):
            print("El correo no puede ser omitido")
        elif (validar_correo(correo)):
            break 
    estatus=1
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                valores=(rfc, nombre, correo, estatus)
                mi_cursor.execute("INSERT INTO CLIENTES (RFC, cliente, correo, estatus) VALUES(?,?,?,?)",valores)
                print("Datos insertados correctamente")          
                break      
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el error: {sys.exc_info()}")
        finally:
            conn.close()

def ejecutar_query(conn, query, valores=None):
    try:
        with conn:
            cursor = conn.cursor()
            if valores:
                cursor.execute(query, valores)
            else:
                cursor.execute(query)
            return cursor.fetchall()
    except Error as e:
        print(e)
        return None

def suspende_cliente():
    try: 
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            cursor = conn.cursor()
            clientes = ejecutar_query(conn, "SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES WHERE estatus=1")

            if clientes:
                print("CLIENTES ENCONTRADOS:\n")
                
                # Crear y mostrar la tabla
                tabla = PrettyTable(["Clave", "Cliente", "RFC", "Correo"])
                for cliente_info in clientes:
                    tabla.add_row(cliente_info)
                print(tabla)

                while True:
                    clave_c = input("\nIngrese la clave del cliente que desea cancelar (0 para cancelar): ")
                    if clave_c.isdigit():
                        clave_c = int(clave_c)
                        if clave_c == 0:
                            print("Volviendo al menú de consultas")
                            break
                        else:
                            valores = {"clave_cliente": clave_c}
                            cliente_info = ejecutar_query(conn, "SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES WHERE clave_cliente=:clave_cliente AND estatus=1", valores)

                            if cliente_info and len(cliente_info) == 1:
                                print("INFORMACION DEL CLIENTE:\n")
                                
                                # Crear y mostrar la tabla
                                tabla_info = PrettyTable(["Clave", "Cliente", "RFC", "Correo"])
                                tabla_info.add_row(cliente_info[0])
                                print(tabla_info)

                                res = input("¿Desea cancelar la nota? SI/NO ").upper()
                                if res == 'SI':
                                    ejecutar_query(conn, "UPDATE CLIENTES SET estatus=0 WHERE clave_cliente=:clave_cliente", valores)
                                    print("Cliente suspendido con éxito")
                                else:
                                    print("Regresando al menú")
                                    break
                            else:
                                print("Ingrese una clave válida")
                    else:
                        print("Ingrese una clave válida")

            else:
                print("\nNo se encontraron coincidencias\nVolviendo al menú de consultas")
    except Error as e:
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

def recuperar_cliente():
    try:
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            cursor = conn.cursor()
            clientes = ejecutar_query(conn, "SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES WHERE estatus=0")

            if clientes:
                print("CLIENTES ENCONTRADOS:\n")
                tabla = PrettyTable(["Clave", "Cliente", "RFC", "Correo"])
                for clave, cliente, rfc, correo in clientes:
                    tabla.add_row([clave, cliente, rfc, correo])
                print(tabla)

                while True:
                    clave_c = input("\nIngrese la clave del cliente que desea recuperar (0 para cancelar): ")
                    if clave_c.isdigit():
                        clave_c = int(clave_c)
                        if clave_c == 0:
                            print("Volviendo al menú de consultas")
                            break
                        else:
                            valores = {"clave_cliente": clave_c}
                            cliente = ejecutar_query(conn, "SELECT cliente, RFC, correo FROM CLIENTES WHERE clave_cliente=:clave_cliente AND estatus=0", valores)

                            if cliente:
                                print("INFORMACION DEL CLIENTE:\n")
                                tabla_info = PrettyTable(["Cliente", "RFC", "Correo"])
                                nombre, rfc, correo = cliente[0]
                                tabla_info.add_row([nombre, rfc, correo])
                                print(tabla_info)

                                res = input("¿Desea recuperar el cliente? SI/NO ").upper()
                                if res == 'SI':
                                    ejecutar_query(conn, "UPDATE CLIENTES SET estatus=1 WHERE clave_cliente=:clave_cliente", valores)
                                    print("Cliente recuperado con éxito")
                                else:
                                    print("Regresando al menú")
                                    break
                            else:
                                print("Ingrese una clave válida")
                    else:
                        print("Ingrese una clave válida")

            else:
                print("\nNo se encontraron coincidencias\nVolviendo al menú de consultas")

    except Error as e:
        print(e)
    except Exception as e:
        print(f"Se produjo el siguiente error: {e}")
            
def menu_consultas_clientes():
    while True:
        print("\n\t--- Menú Consultas y Reportes ---")
        print("Listado de clientes registrados ")
        print("1. Ordenado por clave")
        print("2. Ordenado por nombre")
        print("3. Volver al menú anterior")
        opcion=int(input("Elija una opcion: "))
        if opcion==1:
            ordenar_por_clave_clientes()
        elif opcion==2:
            ordenar_por_nombre_clientes()
        elif opcion==3:
            menu_clientes()
        elif opcion==3:
            break
        else:
            ("Opción inválida")

def ordenar_por_clave_clientes():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES ORDER BY clave_cliente")
                clientes = mi_cursor.fetchall()
                
                if clientes:
                    print("Listado de clientes ordenados por clave:\n")
                    
                    # Crear y mostrar la tabla
                    tabla = PrettyTable(["Clave", "Cliente", "RFC", "Correo"])
                    for clave, nombre, rfc, correo in clientes:
                        tabla.add_row([clave, nombre, rfc, correo])
                    print(tabla)
                    
                    print("\n¿Desea exportar el resultado o desea volver al menú?")
                    opcion = int(input("1. Exportar \n2. Volver al menú de consultas\n"))
                    
                    if opcion == 1:
                        op_Ex = int(input("\n1. Exportar a Excel \n2. Exportar a CSV \n"))
                        if op_Ex == 1:
                            pass  # Agrega lógica para exportar a Excel
                        elif op_Ex == 2:
                            pass  # Agrega lógica para exportar a CSV
                        break
                    elif opcion == 2:
                        menu_clientes()
                        break
                else: 
                    print("No se encontraron coincidencias")
                    menu_clientes()
                    break
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def ordenar_por_nombre_clientes():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES ORDER BY cliente")
                clientes = mi_cursor.fetchall()
                
                if clientes:
                    # Ordenar la lista por el nombre del cliente
                    clientes = sorted(clientes, key=lambda x: x[1])
                    
                    print("Listado de clientes ordenados por nombre:\n")
                    
                    # Crear y mostrar la tabla
                    tabla = PrettyTable(["Nombre", "Clave", "RFC", "Correo"])
                    for clave, cliente, rfc, correo in clientes:
                        tabla.add_row([cliente, clave, rfc, correo])
                    print(tabla)
                    
                    print("\n¿Desea exportar el resultado o desea volver al menú?")
                    opcion = int(input("1. Exportar \n2. Volver al menú de consultas\n"))

                    if opcion == 1:
                        op_Ex = int(input("\n1. Exportar a Excel \n2. Exportar a CSV \n"))
                        if op_Ex == 1:
                            exportar_a_excel(clientes)
                        elif op_Ex == 2:
                            exportar_a_csv(clientes)
                        break
                    elif opcion == 2:
                        menu_clientes()
                        break
                else: 
                    print("No se encontraron coincidencias")
                    menu_clientes()
                    break
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def menu_servicios():
    while True:
        print("\n--- Menú de Servicios ---")
        print("1. Agregar un servicio")
        print("2. Consultas y reportes de servicios")
        print("3. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_servicios()
        elif opcion == "2":
            menu_reportes_servicios()
        elif opcion == "3":
            menu_principal()
        else:
            print("Opción inválida. Por favor, elija una opción válida.")
def buscar_por_clave_servicio():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute(("SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS"))
                servicios = mi_cursor.fetchall()
                if servicios:
                    print("Listado de servicios:\n")
                    print("Clave \t Nombre de servicio")
                    for id_servicio, nombre_servicio in servicios:
                        print(f"\n{id_servicio} \t {nombre_servicio}")
                else: 
                    print("No se encontraron coincidencias")
                    menu_reportes_servicios()
        
                clave_elegida = int(input("\nElija una clave de servicio: "))
                valores={"id_servicio": clave_elegida}
                mi_cursor.execute("SELECT * FROM SERVICIOS WHERE id_servicio = :id_servicio?", valores)
                registro=mi_cursor.fetchall()

                if registro:
                    print("\nDetalle del servicio:\n")
                    for id_servicio, nombre_servicio, costo_servicio in registro:
                        print(f"\n Clave del servicio: {id_servicio}")
                        print(f"\n Nombre del servicio: {nombre_servicio}")
                        print(f"\n COsto del servicio: {costo_servicio}")
                else:
                    print("No se encontró ningún servicio con la clave ingresada.")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def buscar_por_nombre_servicio():
    nombre_servicio_buscar = input("Ingrese el nombre del servicio a buscar: ")
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT * FROM SERVICIOS WHERE UPPER(NOMBRE_SERVICIO) = UPPER(?)",nombre_servicio_buscar)
                servicios_encontrados = mi_cursor.fetchall()

                if servicios_encontrados:
                    print("\nDetalle del servicio/es encontrado/s:\n")
                    for id_servicio, nombre_servicio, costo_servicio in servicios_encontrados:
                        print(f"Clave: {id_servicio}")
                        print(f"Nombre de servicio: {nombre_servicio}")
                        print(f"Costo: {costo_servicio}\n")
                else:
                    print(f"No se encontró ningún servicio con el nombre '{nombre_servicio_buscar}'.")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def generar_reporte_servicios_por_clave():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT * FROM SERVICIOS ORDER BY id_servicio")
                servicios = mi_cursor.fetchall()

                if servicios:
                    print("\nReporte de servicios ordenados por clave:\n")
                    print("Clave \t Nombre de servicio \t Costo")
                    for id_servicio, nombre_servicio, costo_servicio in servicios:
                        print(f"\n{id_servicio} \t {nombre_servicio} \t {costo_servicio}")

                    while True:
                        print("1. Exportar a CSV  \n2. Exportar a Excel  \n3. Regresar al menú de reportes")
                        opcion = input("\nElija una opción: ")
                        if opcion == '1':
                            exportar_a_csv(servicios, "ReporteServiciosPorClave")
                            break
                        elif opcion == '2':
                            exportar_a_excel(servicios, "ReporteServiciosPorClave")
                            break
                        elif opcion == '3':
                            menu_reportes_servicios()
                            break
                        else:
                            print("Opción no válida. Intente nuevamente.")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()


def menu_estadisticas():
    print("\n--- Menú de estadisticos ---")
    print("1. Servicios más prestados")
    print("2. Clientes con más notas")
    print("3. Promedio de monto de las notas por periodo")
    print("4. Volver al menú")
    op=int(input("Ingrese la opcion que desee realizar: "))
    if op==1:
        servicio_mas_prestado()
    elif op==2:
        clientes_mas_notas()
    elif op==3:
        promedio_montos_notas()
    elif op==4:
        menu_principal()
    else:
        print("Opcion no válida")

def servicio_mas_prestado():    
    try:
        cant_Servicios=int(input("\nIngrese la cantidad de servicios más prestados que desea ver "))
        if cant_Servicios==0:
            print("Ingrese un número válido")
        fecha_inicial_str = input("Ingrese la fecha inicial dd/mm/aaaa: ")
        fecha_inicial = datetime.datetime.strptime(fecha_inicial_str, "%d/%m/%Y").date()
        fecha_final_str = input("Ingrese la fecha final dd/mm/aaaa: ")
        fecha_final = datetime.datetime.strptime(fecha_final_str, "%d/%m/%Y").date()
        if fecha_final < fecha_inicial:
            print("La fecha final debe ser igual o posterior a la fecha inicial.")
            return        
    except ValueError:
        print("Fecha ingresada inválida.")
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("""
                    SELECT SERVICIOS.nombre_servicio, COUNT(NOTAS.id_servicio) as cantidad 
                    FROM NOTAS 
                    JOIN SERVICIOS ON NOTAS.id_servicio = SERVICIOS.id_servicio 
                    WHERE NOTAS.fecha BETWEEN ? AND ? 
                    GROUP BY SERVICIOS.nombre_servicio 
                    ORDER BY cantidad DESC LIMIT ?
                    """, (fecha_inicial, fecha_final, cant_Servicios))
                registros = mi_cursor.fetchall()
                if registros:
                    print(f"Listado los {cant_Servicios} más prestados entre las fechas:\n")
                    print("Nombre \tCantidad")
                    for nombre, cantidad in registros:
                        print(f"\n{nombre} \t {cantidad}")
                    print("\n¿Desea exportar el resultado o desea volver al menú?")
                    opcion=int(input("1. Exportar \n2. Volver al menú de consultas"))
                    if opcion==1:
                        op_Ex=(input("\n1. Exportar a excel \2. Exportar a cvs \n"))
                        if op_Ex==1:
                            pass
                        elif op_Ex==2:
                            pass
                        break
                    elif opcion==2:
                            menu_estadisticas()    
                    break       
                else: 
                    print("No se encontraron coincidencias")
                    menu_estadisticas()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            menu_estadisticas()

    

def clientes_mas_notas():  
    try:
        cant_clientes=int(input("\nIngrese la cantidad clientes con más notas que desea ver "))
        if cant_clientes==0:
            print("Ingrese un número válido")
        fecha_inicial_str = input("Ingrese la fecha inicial dd/mm/aaaa: ")
        fecha_inicial = datetime.datetime.strptime(fecha_inicial_str, "%d/%m/%Y").date()
        fecha_final_str = input("Ingrese la fecha final dd/mm/aaaa: ")
        fecha_final = datetime.datetime.strptime(fecha_final_str, "%d/%m/%Y").date()
        if fecha_final < fecha_inicial:
            print("La fecha final debe ser igual o posterior a la fecha inicial.")
            return        
    except ValueError:
        print("Fecha ingresada inválida.")
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("""
                    SELECT CLIENTES.cliente, COUNT(NOTAS.clave_cliente) as cantidad 
                    FROM NOTAS 
                    JOIN CLIENTES ON NOTAS.clave_cliente = CLIENTES.clave_cliente 
                    WHERE NOTAS.fecha BETWEEN ? AND ? 
                    GROUP BY CLIENTES.cliente 
                    ORDER BY cantidad DESC LIMIT ?
                    """, (fecha_inicial, fecha_final, cant_clientes))
                registros = mi_cursor.fetchall()
                if registros:
                    print(f"Listado los {cant_clientes} clientes con más notas entre las fechas:\n")
                    print("Nombre \tCantidad")
                    for nombre, cantidad in registros:
                        print(f"\n{nombre} \t {cantidad}")
                    print("\n¿Desea exportar el resultado o desea volver al menú?")
                    opcion=int(input("1. Exportar \n2. Volver al menú de consultas"))
                    if opcion==1:
                        op_Ex=(input("\n1. Exportar a execel \2. Exportar a cvs \n"))
                        if op_Ex==1:
                            pass
                        elif op_Ex==2:
                            pass
                        break
                    elif opcion==2:
                            menu_estadisticas()    
                    break       
                else: 
                    print("No se encontraron coincidencias")
                    menu_estadisticas()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            menu_estadisticas()

def promedio_montos_notas():
    try:
        fecha_inicial_str = input("Ingrese la fecha inicial dd/mm/aaaa: ")
        fecha_inicial = datetime.datetime.strptime(fecha_inicial_str, "%d/%m/%Y").date()
        fecha_final_str = input("Ingrese la fecha final dd/mm/aaaa: ")
        fecha_final = datetime.datetime.strptime(fecha_final_str, "%d/%m/%Y").date()
        if fecha_final < fecha_inicial:
            print("La fecha final debe ser igual o posterior a la fecha inicial.")
            return        
    except ValueError:
        print("Fecha ingresada inválida.")
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("""SELECT AVG(monto_pago) as promedio 
                        FROM NOTAS 
                        WHERE fecha BETWEEN ? AND ?
                        """, (fecha_inicial, fecha_final))
                registros = mi_cursor.fetchone()
                if registros:
                    print(f"Promedio de pago de las notas en el periodo :\n")
                    print("Promedio")
                    for Promedio in registros:
                        print(f"\n{Promedio}")
                    break       
                else: 
                    print("No se encontraron coincidencias")
                    menu_estadisticas()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            menu_estadisticas()



def exportar_a_excel(datos, nombre_archivo):
    df = pd.DataFrame(datos)
    df.to_excel(nombre_archivo, index=False)

def validar_rfc(rfc):
    patron = r'^[A-Z&Ñ]{3,4}\d{6}[A-V1-9][0-9A-Z]([0-9A])?$'
    return bool(re.fullmatch(patron, rfc))


def validar_correo(correoelectronico):
    Filtro = r'^[\w\.]+@[\w\.]+$'    
    if re.match(Filtro, correoelectronico):
        print("El correo electrónico es válido.")
        return True 
    else:
        print("ERROR. El dato ingresado no es valido. Vuelva a intentarlo")
        return False

def exportar_a_csv(datos, nombre_archivo):
    try:
        df = pd.DataFrame(datos, columns=['Clave', 'Nombre de servicio', 'Costo', 'Estatus'])
        timestamp = datetime.now().strftime("%m_%d_%Y")
        nombre_archivo += f"_{timestamp}.csv"
        df.to_csv(nombre_archivo, index=False)
        print(f"Datos exportados a {nombre_archivo}")
    except Exception as e:
        print(f"Error al exportar a CSV: {e}")

def exportar_a_excel(datos, nombre_archivo):
    try:
        df = pd.DataFrame(datos, columns=['Clave', 'Nombre de servicio', 'Costo', 'Estatus'])
        timestamp = datetime.now().strftime("%m_%d_%Y")
        nombre_archivo += f"_{timestamp}.xlsx"

        with pd.ExcelWriter(nombre_archivo, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False)

        print(f"Datos exportados a {nombre_archivo}")
        return True
    except Exception as e:
        print(f"Error al exportar a Excel: {e}")

def listado_servicios():
    while True:
        print("\n--- Menú de listado de Servicios ---")
        print("1. Listado de servicios ordenados por clave")
        print("2. Listado de servicios ordenados por nombre") 
        print("3. Volver al menu anterior") 
        listado_opcion=int(input("Seleccione una opción: "))  
        if listado_opcion==1:
            generar_reporte_servicios_por_clave()
        elif listado_opcion==2:
            generar_reporte_servicios_por_nombre()
        elif listado_opcion==3:
            return
        else:
            print("La opcion no es valida.")

def agregar_servicios():
    conn = None
    while True:
        try:
            nombre_servicio = input("Ingrese el nombre del servicio (no puede quedar vacío): ")
            if not nombre_servicio.strip():
                print("El nombre del servicio no puede estar vacío. Intente nuevamente.")
                continue
            
            while True:
                try:
                    costo_servicio = float(input("Ingrese el costo del servicio (debe ser superior a 0.00): "))
                    if costo_servicio <= 0.00:
                        print("El costo del servicio debe ser superior a 0.00. Intente nuevamente.")
                    else:
                        break  
                except ValueError:
                    print("Error: Ingrese un valor numérico válido para el costo.")
            estatus=1
            conn = sqlite3.connect('BD_TALLER_MECANICO.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO SERVICIOS (NOMBRE_SERVICIO, COSTO_SERVICIO, estatus) VALUES (?, ?, ?)", (nombre_servicio, costo_servicio, estatus))
            conn.commit()
            print("Servicio agregado con éxito.")
            return
        except ValueError:
            print("Error: Ingrese un valor numérico válido para el costo.")
        except Error as e:
            print(e)
        except:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            if conn:
               conn.close()

def suspender_servicio():
    servicio = buscar_por_clave_servicio()
    if servicio:
        confirmacion = input("¿Desea suspender este servicio? (s/n): ").lower()
        if confirmacion == 's':
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("UPDATE SERVICIOS SET estatus = 0 WHERE ID_SERVICIO = ?", (servicio[0],))
                conn.commit()
                print("Servicio suspendido exitosamente.")
        else:
            print("Operación cancelada.")

def recuperar_servicio():
    servicio = buscar_por_clave_servicio(activos=False)
    if servicio:
        confirmacion = input("¿Desea recuperar este servicio? (s/n): ").lower()
        if confirmacion == 's':
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor = conn.cursor()
                mi_cursor.execute("UPDATE SERVICIOS SET estatus = 1 WHERE ID_SERVICIO = ?", (servicio[0],))
                conn.commit()
                print("Servicio recuperado exitosamente.")
        else:
            print("Operación cancelada.")

def buscar_por_clave_servicio(activos=True):
    try:
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            mi_cursor = conn.cursor()

            if activos:
                mi_cursor.execute("SELECT ID_SERVICIO, NOMBRE_SERVICIO, COSTO_SERVICIO FROM SERVICIOS WHERE estatus = 1")
            else:
                mi_cursor.execute("SELECT ID_SERVICIO, NOMBRE_SERVICIO, COSTO_SERVICIO FROM SERVICIOS WHERE estatus = 0")
            servicios = mi_cursor.fetchall()

            if servicios:
                tabla_servicios = PrettyTable(["Clave", "Nombre de Servicio", "Costo"])
                for servicio in servicios:
                    tabla_servicios.add_row([servicio[0], servicio[1], servicio[2]])
                print(tabla_servicios)

                if not activos:
                    print("\n(Servicios suspendidos)")

                while True:
                    try:
                        clave_elegida = int(input("\nElija una clave de servicio (o ingrese 0 para volver): "))

                        if clave_elegida == 0:
                            return None  # Usuario eligió volver al menú anterior

                        mi_cursor.execute("SELECT * FROM SERVICIOS WHERE ID_SERVICIO = ?", (clave_elegida,))
                        servicio_elegido = mi_cursor.fetchone()

                        if servicio_elegido:
                            print("\n Detalle del servicio:")
                            print(f" Clave del servicio: {servicio_elegido[0]}")
                            print(f" Nombre del servicio: {servicio_elegido[1]}")
                            print(f" Costo del servicio: {servicio_elegido[2]}")

                            return servicio_elegido
                        else:
                            print("No se encontró ningún servicio con la clave ingresada.")
                    except ValueError:
                        print("Error: Ingrese un valor numérico válido para la clave.")
            else:
                print("No hay servicios registrados.")

    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")

def buscar_por_nombre_servicio(activos=True):
    nombre_servicio_buscar = input("Ingrese el nombre del servicio a buscar: ")
    try:
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            mi_cursor = conn.cursor()

            filtro_estatus = "estatus = 1" if activos else "estatus = 0"
            mi_cursor.execute(
                f"SELECT * FROM SERVICIOS WHERE UPPER(NOMBRE_SERVICIO) = UPPER(?) AND {filtro_estatus}",
                (nombre_servicio_buscar,),
            )

            servicios_encontrados = mi_cursor.fetchall()
            if servicios_encontrados:
                print("Listado de servicios encontrados:\n")
                table = PrettyTable(["Nombre de Servicio", "Clave"])
                for servicio in servicios_encontrados:
                    table.add_row([servicio[1], servicio[0]])
                print(table)
            else:
                print(f"No se encontró ningún servicio con el nombre '{nombre_servicio_buscar}'.")
    except Error as e:
        print(f"Error al conectarse a la base de datos: {e}")
    except Exception as ex:
        print(f"Se produjo el siguiente error: {ex}")

def generar_reporte_servicios_por_clave():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT * FROM SERVICIOS ORDER BY id_servicio")
                servicios = mi_cursor.fetchall()

                if servicios:
                    print("\nReporte de servicios ordenados por clave:\n")
                    table = PrettyTable(["Clave", "Nombre de servicio", "Costo"])
                    for servicio in servicios:
                        table.add_row([servicio[0], servicio[1], servicio[2]])
                    print(table)

                    while True:
                        print("1. Exportar a CSV  \n2. Exportar a Excel  \n3. Regresar al menú de reportes")
                        opcion = input("\nElija una opción: ")
                        if opcion == '1':
                            exportar_a_csv(servicios, "ReporteServiciosPorClave")
                            break
                        elif opcion == '2':
                            exportar_a_excel(servicios, "ReporteServiciosPorClave")
                            break
                        elif opcion == '3':
                            return
                        else:
                            print("Opción no válida. Intente nuevamente.")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def generar_reporte_servicios_por_nombre():
    while True:
        try:
            conn = sqlite3.connect('BD_TALLER_MECANICO.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM SERVICIOS ORDER BY nombre_servicio")
            servicios = cursor.fetchall()

            if servicios:
                print("\nReporte de servicios ordenados por Nombre:\n")
                table = PrettyTable(["Nombre de servicio", "Clave", "Costo"])

                for servicio in servicios:
                        table.add_row([servicio[1], servicio[0], servicio[2]])
                print(table)

                while True:
                    print("1. Exportar a CSV  \n2. Exportar a Excel  \n3. Regresar al menú de reportes")
                    opcion = input("\nElija una opción: ")
                    if opcion == '1':
                        exportar_a_csv(servicios, "ReporteServiciosPorClave")
                        break
                    elif opcion == '2':
                        exportar_a_excel(servicios, "ReporteServiciosPorClave")
                        break
                    elif opcion == '3':
                        return
                    else:
                        print("Opción no válida. Intente nuevamente.")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def menu_reportes_servicios():
    while True:
        print("\n--- Menú de Consultas y Reportes de Servicios ---")
        print("1. Consultas por clave de servicio")
        print("2. Consultas por nombre de servicio")
        print("3. Listado de servicios")
        print("4. Volver al menú de servicios")
        opcion = int(input("Seleccione una opción: "))

        if opcion == 1:
            buscar_por_clave_servicio()
        elif opcion == 2:
            buscar_por_nombre_servicio()
        elif opcion == 3:
            listado_servicios()
        elif opcion == 4:
            return
        else:
            print("Opción inválida. Por favor, elija una opción válida.")

def menu_servicios():
    while True:
        print("\n--- Menú de Servicios ---")
        print("1. Agregar un servicio")
        print("2. Suspender un servicio")
        print("3. Recuperar un servicio")
        print("4. Consultas y reportes de servicios")
        print("5. Volver al menú principal")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            agregar_servicios()
        elif opcion == "2":
            suspender_servicio()
        elif opcion == "3":
            recuperar_servicio()
        elif opcion == "4":
            menu_reportes_servicios()
        elif opcion == "5":
            return
        else:
            print("Opción inválida. Por favor, elija una opción válida.")

        
def crear_tablas():
    try:
        with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
            mi_cursor = conn.cursor()
            mi_cursor.execute("PRAGMA foreign_keys = 1")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
                CLIENTES (clave_cliente INTEGER NOT NULL PRIMARY KEY, cliente TEXT NOT NULL, RFC TEXT NOT NULL, correo TEXT, estatus INTEGER NOT NULL);")            
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
                SERVICIOS (id_servicio INTEGER NOT NULL PRIMARY KEY, nombre_servicio TEXT NOT NULL, costo_servicio INTEGER NOT NULL, estatus INTEGER NOT NULL DEFAULT 1);")
            mi_cursor.execute("CREATE TABLE IF NOT EXISTS \
                NOTAS (folio INTEGER NOT NULL PRIMARY KEY, fecha TIMESTAMP, estatus INTEGER NOT NULL  DEFAULT 1, monto_pago INTEGER NOT NULL, clave_cliente INTEGER NOT NULL,\
                              id_servicio INTEGER NOT NULL, FOREIGN KEY (clave_cliente) REFERENCES CLIENTES(clave_cliente), FOREIGN KEY (id_servicio) REFERENCES SERVICIOS(id_servicio));")
            conn.commit()
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    conn.close()

crear_tablas()
menu_principal()


