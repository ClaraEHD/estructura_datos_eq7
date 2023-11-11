import datetime
import pandas as PD
import re
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
                mi_cursor.execute("SELECT * FROM SERVICIOS ORDER BY id_servicio")
                servicios = mi_cursor.fetchall()

                if servicios:
                    print("\nListado de servicios disponibles:\n")
                    print("Clave \t Nombre de servicio \t Costo")
                    for id_servicio, nombre_servicio, costo_servicio in servicios:
                        print(f"\n{id_servicio} \t {nombre_servicio} \t {costo_servicio}")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()


        notas=list()
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
                            valores_ser={"id_servicio":servicio_clave_ingreso}
                            mi_cursor.execute("SELECT costo_servicio FROM SERVICIOS WHERE id_servicio=:id_servicio", valores_ser)
                            servicios = mi_cursor.fetchone()
                            if servicios:
                                clave_servicio=servicio_clave_ingreso
                                costo_servicio_insertar=servicios
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
            nota["Monto_pago"] = costo_servicio_insertar
            nota["clave_cliente"] = clave_cliente
            nota["id_servicio"]=clave_servicio
            notas.append(nota)

            try:
                while True:
                    with sqlite3.connect("PrimerIntentoDemo.db") as conn:
                        mi_cursor = conn.cursor()
                        mi_cursor.execute("INSERT INTO NOTAS (fecha, estatus, monto_pago, clave_cliente, id_servicio)\
                                        (:Fecha,:Estatus,:Monto_pago,:clave_cliente,:id_servicio')",notas)
                        print(f"Datos insertados correctamente \nEl folio de la nota es {mi_cursor.lastrowid}")
            except Error as e:
                    print (e)
            except:
                    print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            finally:
                    conn.close()

def cancelar_nota():
    while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT N.FOLIO, N.FECHA, N.clave_cliente, C.cliente, C.RFC, C.correo, N.id_servicio, S.nombre_servicio, S.costo_servicio, N.monto_pago\
                                   FROM NOTAS N INNER JOIN CLIENTES C ON N.clave_cliente=C.clave_cliente INNER JOIN SERVICIOS S ON \
                                    N.id_servicio=S.id_servicio WHERE N.estatus=1")
                notas = mi_cursor.fetchall()
                if notas:
                    print("NOTAS ENCONTRADAS:\n")
                    print("Folio \t Fecha \t Clave del cliente \t Cliente \t RFC\
                          \tCorreo \tid_servicio \tNombre del servicio\
                          \tCosto del servicio \tMonto de pago total")
                    for Folio, Fecha, Clave_c, Nombre_c, rfc, Correo, id_servicio,n_servicio ,c_servicio , monto_p in notas:
                        print(f"\n{Folio} \t{Fecha} \t{Clave_c} \t{Nombre_c} \t{rfc} \t{Correo} \t{id_servicio} \t{n_servicio} \t{c_servicio}\t {monto_p}")
                
                    print("¿Desea cancelar una nota?")
                    cancelar=input()
                    if cancelar.upper=="SI":
                        cancelar_folio=int(input("Ingrese el folio: "))
                        values={"folio":cancelar_folio}
                        mi_cursor.execute("UPDATE NOTAS SET estatus=0 WHERE folio=:folio", values)
                    elif cancelar.upper=="NO":
                        print("Volviendo al menu de consultas de notas")
                        menu_notas()
                else: 
                    print("No se encontraron coincidencias")
                    menu_notas()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def recuperar_nota_cancelada():
    while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT FOLIO, FECHA, clave_cliente\
                                   FROM NOTAS WHERE estatus=0")
                notas = mi_cursor.fetchall()
                if notas:
                    print("NOTAS ENCONTRADAS:\n")
                    print("Folio \t Fecha \t Clave del cliente")
                    for Folio, Fecha, Clave_c, in notas:
                        print(f"\n{Folio} \t{Fecha} \t{Clave_c}")
                
                    print("¿Desea recuperar una nota?")
                    cancelar=input()
                    if cancelar.upper=="SI":
                        cancelar_folio=int(input("Ingrese el folio: "))
                        print(f"Los datos de la nota con el folio {cancelar_folio} son:")
                        mi_cursor.execute("SELECT N.FOLIO, N.FECHA, N.clave_cliente, C.cliente, C.RFC, C.correo, N.id_servicio, S.nombre_servicio, S.costo_servicio, N.monto_pago\
                                   FROM NOTAS N INNER JOIN CLIENTES C ON N.clave_cliente=C.clave_cliente INNER JOIN SERVICIOS S ON \
                                    N.id_servicio=S.id_servicio WHERE N.estatus=1")
                        notas = mi_cursor.fetchall()
                        if notas:
                            print("NOTA:\n")
                            print("Folio \t Fecha \t Clave del cliente \t Cliente \t RFC\
                                \tCorreo \tid_servicio \tNombre del servicio\
                                \tCosto del servicio \tMonto de pago total")
                            for Folio, Fecha, Clave_c, Nombre_c, rfc, Correo, id_servicio,n_servicio ,c_servicio , monto_p in notas:
                                print(f"\n{Folio} \t{Fecha} \t{Clave_c} \t{Nombre_c} \t{rfc} \t{Correo} \t{id_servicio} \t{n_servicio} \t{c_servicio}\t {monto_p}")
                        res=input("¿Desea confirmar la cancelación?")
                        if res.upper==("SI"):
                            values={"folio":cancelar_folio}
                            mi_cursor.execute("UPDATE NOTAS SET estatus=0 WHERE folio=:folio", values)
                            print("Nota recuperada exitosamente")
                        elif cancelar.upper=="NO":
                            print("La nota no fue recuperada \nVolviendo al menu de consultas de notas")
                            menu_notas()
                    elif cancelar.upper=="NO":
                        print("La nota no fue recuperada \nVolviendo al menu de consultas de notas")
                        menu_notas()
                else: 
                    print("No se encontraron coincidencias")
                    menu_notas()
        except Error as e:
            print (e)
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
#pendiente consultar por periodo
def consultar_por_periodo(): 

    try:
        fecha_inicial_str = input("Ingrese la fecha inicial dd/mm/aaaa (deje en blanco para usar 01/01/2000): ")
        if fecha_inicial_str.strip() == '':
            f_i=('1/1/2000')
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
    while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                #ESTRAER FECHAS CON UN SELECT, CONVERTIRLAS Y DESPUES COMPARALAS, GUARDAR ID
                mi_cursor.execute("SELECT NOTAS.FOLIO, NOTAS.FECHA, NOTAS.clave_cliente, FROM CLIENTES.cliente, CLIENTES.RFC\
                                   CLIENTES.correo, NOTAS.monto_pago, SERVICIOS.nombre_servicio, SERVICIOS.costo_servicio\
                                   FROM NOTAS INNER JOIN CLIENTES ON NOTAS.clave_cliente=CLIENTES.clave_cliente INNER JOIN SERVICIOS ON \
                                    NOTAS.id_servicio=SERVICIOS.id_servicio WHERE NOTAS.estatus=False")#PENDIENTE LO DE LAS FECHAS 
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("NOTAS ENCONTRADAS:\n")
                    print("Folio \t Fecha")
                    for Folio, Fecha,Clave_c, Nombre_c, RFC, Correo, monto_p, Servicio, costo_Servicio  in clientes:
                        print(f"\n{Folio} \t {Fecha}\t {Clave_c}\t {Nombre_c}\t {RFC}\t {Correo}\t {monto_p}\t {Servicio}\t {costo_Servicio}")
                else: 
                    print("No se encontraron coincidencias")
                    menu_reportes_servicios()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
        print("Desea preservar los datos en un archivo")
        print("1. Exportar a excel")
        print("2. Exportar a csv")
        print("3. Regresar al menu de consltas")
        opcion=int(input("Elija la opcion: "))
        if opcion==1:
            exportar_a_excel()
        elif opcion==2:
            exportar_a_csv()
        elif opcion==3:
            menu_consultas_notas()
#------------------------------
def consultar_por_folio():
    while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT N.FOLIO, N.FECHA, C.cliente\
                                   FROM NOTAS N INNER JOIN CLIENTES C ON N.clave_cliente=C.clave_cliente WHERE N.estatus=1")
                notas = mi_cursor.fetchall()
                if notas:
                    print("NOTAS ENCONTRADAS:\n")
                    print("Folio \t Fecha \t Cliente")
                    for Folio, Fecha, clietnte, in notas:
                        print(f"\n{Folio} \t{Fecha} \t{clietnte}")
                    folio =int(input("Ingrese el folio de la nota que deasea consultar: "))
                    if folio==Folio:
                        valores={"folio":folio}
                        mi_cursor.execute("SELECT NOTAS.FOLIO, NOTAS.FECHA, NOTAS.clave_cliente, FROM CLIENTES.cliente, CLIENTES.RFC\
                                        CLIENTES.correo, NOTAS.monto_pago, SERVICIOS.nombre_servicio, SERVICIOS.costo_servicio\
                                        FROM NOTAS INNER JOIN CLIENTES ON NOTAS.clave_cliente=CLIENTES.clave_cliente INNER JOIN SERVICIOS ON \
                                            NOTAS.id_servicio=SERVICIOS.id_servicio WHERE NOTAS.folio=:folio AND NOTAS.estatus=1", valores) 
                        nota = mi_cursor.fetchall()
                        if nota:
                            print("NOTAS ENCONTRADAS:\n")
                            print("Folio \t Fecha \t Clave del cliente \t Nombre del cliente \t RFC\
                                        \tCorreo \tMonto de pago total \t Nombre del servicio \tCosto_servicio")
                            for Folio, Fecha,Clave_c, Nombre_c, rfc, Correo, monto_p, Servicio, costo_Servicio  in nota:
                                print(f"\n{Folio} \t {Fecha}\t {Clave_c}\t {Nombre_c}\t {rfc}\t {Correo}\t {monto_p}\t {Servicio}\t {costo_Servicio}")
                else: 
                    print("\nNo se encontraron coincidencias \nVolviendo al menú de consultas")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
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

def suspende_cliente():
      while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT clave_cliente, cliente\
                                   FROM CLIENTES WHERE estatus=1")
                notas = mi_cursor.fetchall()
                if notas:
                    print("CLIENTES ENCONTRADAS:\n")
                    print("Clave \t Cliente ")
                    for clave, cliente, in notas:
                        print(f"\n{clave} \t{cliente}")
                    while True:
                        clave_c =int(input("\nIngrese la clave del cliente que deasea cancelar (0 para cancelar): "))
                        if clave_c==clave_c:
                            valores={"clave_cliente":clave_c}
                            mi_cursor.execute("SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES WHERE clave_cliente=:clave_cliente AND estatus=1", valores) 
                            nota = mi_cursor.fetchall()
                            if nota:
                                print("INFORMACION DEL CLIENTE:\n")
                                print("Clave \t Cliente \t RFC \t Correo")
                                for Clave, Cliente,rfc,correo in nota:
                                    print(f"\n{Clave} \t {Cliente}\t {rfc}\t {correo}")
                                res=input("¿Desea cancelar la nota? SI/NO ")
                                if res.upper=='SI':
                                    mi_cursor.execute("UPDATE CLIENTE SET estatus=0 WHERE clave_cliente=:clave_cliente", valores) 
                                    print("Cliente suspendido con éxito")
                                else:
                                    print("Regresando al menú")
                                    menu_consultas_clientes()                               
                            break
                        elif clave_c==0:
                            print("Volviendo al menú de consultas")
                            menu_consultas_clientes()    
                        else:
                            print("Ingrese una clave válida")
                else: 
                    print("\nNo se encontraron coincidencias \nVolviendo al menú de consultas")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            menu_consultas_notas()   

  

def recuperar_cliente():
      while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute("SELECT clave_cliente, cliente\
                                   FROM CLIENTES WHERE estatus=0")
                notas = mi_cursor.fetchall()
                if notas:
                    print("CLIENTES ENCONTRADAS:\n")
                    print("Clave \t Cliente ")
                    for clave, cliente, in notas:
                        print(f"\n{clave} \t{cliente}")
                    while True:
                        clave_c =int(input("\nIngrese la clave del cliente que deasea cancelar (0 para cancelar): "))
                        if clave_c==clave_c:
                            valores={"clave_cliente":clave_c}
                            mi_cursor.execute("SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES WHERE clave_cliente=:clave_cliente AND estatus=0", valores) 
                            nota = mi_cursor.fetchall()
                            if nota:
                                print("INFORMACION DEL CLIENTE:\n")
                                print("Clave \t Cliente \t RFC \t Correo")
                                for Clave, Cliente,rfc,correo in nota:
                                    print(f"\n{Clave} \t {Cliente}\t {rfc}\t {correo}")
                                res=input("¿Desea cancelar la nota? SI/NO ")
                                if res.upper=='SI':
                                    mi_cursor.execute("UPDATE CLIENTE SET estatus=1 WHERE clave_cliente=:clave_cliente", valores) 
                                    print("Cliente recuperado con éxito")
                                else:
                                    print("Regresando al menú")
                                    menu_consultas_clientes()                               
                            break
                        elif clave_c==0:
                            print("Volviendo al menú de consultas")
                            menu_consultas_clientes()    
                        else:
                            print("Ingrese una clave válida")
                else: 
                    print("\nNo se encontraron coincidencias \nVolviendo al menú de consultas")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
            menu_consultas_notas()   




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
                mi_cursor=conn.cursor()
                mi_cursor.execute(("SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES ORDER BY clave_cliente"))
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("Listado de clientes ordenados por clave:\n")
                    print("Clave \tCliente \t RFC \tCorreo")
                    for clave, nombre, rfc, correo  in clientes:
                        print(f"\n{clave} \t {nombre}\t {rfc}\t {correo}")
                    print("\n¿Desea exportar el resultado o desea volver al menú?")
                    opcion=int(input("1. Exportar \n2. Volver al menú de consultas"))
                    if opcion==1:
                        op_Ex=(input("\n1. Exportar a execel \n2. Exportar a cvs \n"))
                        if op_Ex==1:
                            pass
                        elif op_Ex==2:
                            pass
                        break
                    elif opcion==2:
                            menu_clientes()    
                    break       
                else: 
                    print("No se encontraron coincidencias")
                    menu_clientes()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def ordenar_por_nombre_clientes():
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute(("SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES ORDER BY cliente"))
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("Listado de clientes ordenados por nombre:\n")
                    print("Clave \tCliente \t RFC \tCorreo")
                    for clave, cliente, rfc, correo  in clientes:
                        print(f"\n{clave} \t {cliente}\t {rfc}\t {correo}")
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
                            menu_clientes()    
                    break       
                else: 
                    print("No se encontraron coincidencias")
                    menu_clientes()
        except Error as e:
            print (e)
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
    print("2. Clientes con más notas")
    print("4. Volver al menú")
    op=int(input("Ingrese la opcion que desee realizar: "))
    if op==1:
        servicio_mas_prestado()
    elif op==2:
        clientes_mas_notas()
    elif op==3:
        promedio_montos_notas
    elif op==4:
        menu_principal()
    else:
        print("Opcion no válida")

def servicio_mas_prestado():
    cant_Servicios=int(input("\nIngrese la cantidad de servicios más prestados que desea ver "))
    fecha_inicial=input("Ingrese la fecha incial del periodo a reportar: ")
    fecha_final=input("Ingrese la fecha final del periodo a reportar: ")
    valores=fecha_inicial,fecha_final,cant_Servicios
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute(("SELECT SERVICIOS.nombre_servicio, (count(NOTAS.id_servicio)) as cantidad FROM NOTAS JOIN SERVICIOS \
                                   ON NOTAS.id_servicio=SERVICIOS.id_servicio WHERE NOTAS.fecha BETWEEN ? AND ?\
                                    GROUP BY SERVICIOS.nombre_servicio ORDER BY cantidad DESC LIMIT ?", valores))
                registros = mi_cursor.fetchall()
                if registros:
                    print(f"Listado los {cant_Servicios} más prestados entre las fechas:\n")
                    print("Nombre \Cnatidad")
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

    

def clientes_mas_notas():
    cant_clientes=int(input("\nIngrese la cantidad clientes con más notas que desea ver "))
    fecha_inicial=input("Ingrese la fecha incial del periodo a reportar: ")
    fecha_final=input("Ingrese la fecha final del periodo a reportar: ")
    valores=fecha_inicial,fecha_final,cant_clientes
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute(("SELECT CLIENTES.cliente, (count(NOTAS.clave_cliente)) as cantidad FROM NOTAS JOIN CLIENTES \
                                   ON NOTAS.clave_cliente=CLIENTES.clave_cliente WHERE NOTAS.fecha BETWEEN ? AND ?\
                                    GROUP BY CLIENTES.cliente ORDER BY cantidad DESC LIMIT ?", valores))
                registros = mi_cursor.fetchall()
                if registros:
                    print(f"Listado los {cant_clientes} clientes con más notas entre las fechas:\n")
                    print("Nombre \Cnatidad")
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

def promedio_montos_notas():
    fecha_inicial=input("Ingrese la fecha incial del periodo a reportar: ")
    fecha_final=input("Ingrese la fecha final del periodo a reportar: ")
    valores=fecha_inicial,fecha_final
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                mi_cursor.execute(("SELECT AVG(monto_pago) as promedio FROM NOTAS WHERE fecha BETWEEN ? AND ?", valores))
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

##funciones para validaciones y guardar datos


def exportar_a_excel(datos, nombre_archivo):
    df = pd.DataFrame(datos)
    df.to_excel(nombre_archivo, index=False)

def validar_rfc(rfc):
    # Expresion regular para validar el RFC 
    patron = r'^[A-Z&Ñ]{3,4}\d{6}[A-V1-9][0-9A-Z]([0-9A])?$'
    
    # Utiliza re.fullmatch para verificar si la cadena cumple con el patrón
    return bool(re.fullmatch(patron, rfc))


#Funcion para validar correo electronico
def validar_correo(correoelectronico):
    Filtro = r'^[\w\.]+@[\w\.]+$'    
    if re.match(Filtro, correoelectronico):
        print("El correo electrónico es válido.")
        return True 
    else:
        print("ERROR. El dato ingresado no es valido. Vuelva a intentarlo")
        return False

"""def guardar_datos_csv(notas):
    # Define los nombres de las columnas (campos del diccionario)
    columnas = notas[0].keys()
# Abrir el archivo CSV en modo escritura
    with open(archivo_csv, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=columnas)
    
    # Escribe los nombres de las columnas
        writer.writeheader()
    
    # Escribe cada diccionario en el archivo
        for diccionario in notas:
            writer.writerow(diccionario)


    folio =int(input("Ingrese el folio de la nota: "))
    while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                valores={"folio":folio}
                mi_cursor.execute("SELECT NOTAS.FOLIO, NOTAS.FECHA, NOTAS.clave_cliente, FROM CLIENTES.cliente, CLIENTES.RFC\
                                   CLIENTES.correo, NOTAS.monto_pago, SERVICIOS.nombre_servicio, SERVICIOS.costo_servicio\
                                   FROM NOTAS INNER JOIN CLIENTES ON NOTAS.clave_cliente=CLIENTES.clave_cliente INNER JOIN SERVICIOS ON \
                                    NOTAS.id_servicio=SERVICIOS.id_servicio WHERE NOTAS.folio=:folio AND NOTAS.estatus=False", valores) 
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("NOTAS ENCONTRADAS:\n")
                    print("Folio \t Fecha \t Clave del cliente \t Nombre del cliente \t RFC\
                                   \tCorreo \tMonto de pago total \t Nombre del servicio \tCosto_servicio")
                    for Folio, Fecha,Clave_c, Nombre_c, RFC, Correo, monto_p, Servicio, costo_Servicio  in clientes:
                        print(f"\n{Folio} \t {Fecha}\t {Clave_c}\t {Nombre_c}\t {RFC}\t {Correo}\t {monto_p}\t {Servicio}\t {costo_Servicio}")
                else: 
                    print("No se encontraron coincidencias")
                    menu_reportes_servicios()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()
        print("Desea preservar los datos en un archivo")
        print("1. Exportar a excel")
        print("2. Exportar a csv")
        print("3. Regresar al menu de consltas")
        opcion=int(input("Elija la opcion: "))
        if opcion==1:
            exportar_a_excel()
        elif opcion==2:
            exportar_a_csv()
        elif opcion==3:
            menu_consultas_notas()   
#"""#función para ordenar rfc 
def RFC_ORDENADO(RFC):
    return RFC['RFC']
#función para consultar por cliente
"""def consultar_por_rfc():
    rfc_ordenado=sorted(notas, key=RFC_ORDENADO)
    for nota in rfc_ordenado:
        if nota["Estatus"]==False:
            print("RFC del cliente: ", nota['RFC'], "   Folio: ", nota['Folio'])
    folio =int(input("Ingrese el folio de la persona que desea consultar: "))
    folio_encontrado=False
    for nota in notas:
        if nota['Folio'] == folio and nota['Estatus']==False:
            print("\nDetalle de la nota:\n")
            print(f"Folio: {nota['Folio']}\n")
            print(f"Fecha: {nota['Fecha']}\n")
            print(f"Nombre del cliente: {nota['Cliente']}\n")
            print(f"RFC: {nota['RFC']}\n")
            print(f"Servicio: \n {nota['Detalles']}\n")
            print(f"Costo del servicio: {nota['Monto_pago']}")
            print(f"Monto promedio: {nota['Promedio_monto']}")
            p_importar=input("¿Desea importar la información a excel? SI/NO ")
            folio_encontrado=True
            if p_importar.strip().upper()=="SI":
                rfcnota=nota['RFC']
                fecha_str = datetime.datetime.today().date().strftime('%d-%m-%Y')
                nombre_archivo=f"{rfcnota}_{fecha_str}.xlsx"
                print(type(nombre_archivo))
                exportar_a_excel(notas, nombre_archivo)
                print(f'Datos exportados a {os.path.abspath(nombre_archivo)}') ##pendiente ubicación de archivo
            else:
                print("Regresando al menu de consultas")
                menu_consultas_notas(notas) 
    if not folio_encontrado:
            print("No se encontró una nota válida para el folio ingresado.")
"""
#función para cancelar notas

def exportar_a_csv(datos, nombre_archivo):
    df = pd.DataFrame(datos, columns=['Clave', 'Nombre de servicio', 'Costo'])
    timestamp = datetime.now().strftime("%m_%d_%Y")
    nombre_archivo += f"_{timestamp}.csv"
    df.to_csv(nombre_archivo, index=False)
    print(f"Datos exportados a {nombre_archivo}")


def exportar_a_excel(datos, nombre_archivo):
    df = pd.DataFrame(datos, columns=['Clave', 'Nombre de servicio', 'Costo'])
    timestamp = datetime.now().strftime("%m_%d_%Y")
    nombre_archivo += f"_{timestamp}.xlsx"
    df.to_excel(nombre_archivo, index=False)
    print(f"Datos exportados a {nombre_archivo}")

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

            conn = sqlite3.connect('BD_TALLER_MECANICO.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO SERVICIOS (NOMBRE_SERVICIO, COSTO_SERVICIO) VALUES (?, ?)", (nombre_servicio, costo_servicio))
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
                mi_cursor.execute("SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS WHERE estatus = 1")
            else:
                mi_cursor.execute("SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS WHERE estatus = 0")
            servicios = mi_cursor.fetchall()

            if servicios:
                print("\nListado de servicios:\n")
                print("Clave \t Nombre de servicio")
                for servicio in servicios:
                    print(f"{servicio[0]} \t {servicio[1]}")

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
        print(e)
    except Exception:
        print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")

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
                print("Listado de servicios:\n")
                table = PrettyTable(["Nombre de servicio", "Clave"])
                for servicio in servicios_encontrados:
                    table.add_row([servicio[1], servicio[0]])
                print(table)
            else:
                print(f"No se encontró ningún servicio con el nombre '{nombre_servicio_buscar}'.")
    except Error as e:
        print(e)
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
                NOTAS (folio INTEGER NOT NULL PRIMARY KEY, fecha TIMESTAMP, estatus INTEGER NOT NULL, monto_pago INTEGER NOT NULL, clave_cliente INTEGER NOT NULL,\
                              id_servicio INTEGER NOT NULL, FOREIGN KEY (clave_cliente) REFERENCES CLIENTES(clave_cliente), FOREIGN KEY (id_servicio) REFERENCES SERVICIOS(id_servicio));")
            conn.commit()
    except Error as e:
        print(e)
    except Exception:
        print(f'Se produjo el siguiente error: {sys.exc_info()[0]}')
    conn.close()

crear_tablas()
menu_principal()


