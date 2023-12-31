import datetime
import pandas as pd
import re
import os
import csv
import sqlite3
from sqlite3 import Error
import sys


def menu_clientes():
    while True:
        print("\n\t--- Menú Clientes ---")
        print("1. Agregar un cliente")
        print("2. Consultas y reportes de clientes")
        print("3. Volver al menú anterior (Menú Principal)")
        eleccion=int(input("Elija una opción: "))
        if eleccion==1:
            agregar_cliente()
        elif eleccion==2:
            menu_consultas_clientes()
        elif eleccion==3:
            menu_principal()
        else:
            print("Opción inválida")
def agregar_cliente():
    print("Agregar Cliente: \n")
    print("Lista de clientes activos: ")
    
    rfc = input("Por favor, ingrese su RFC: ")
    validar_rfc(rfc)
    nombre = input("Ingresa el nombre completo del cliente: ")
    if nombre.strip()=="":
        print("No se puede dejar el campo vacío")
        
    correo = input("Ingrese el correo del cliente: ")
    validar_correo(correo)
    while True:
        try:
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                valores=(rfc, nombre, correo)
                mi_cursor.execute("INSERT INTO CLIENTES (RFC, cliente, correo) VALUES(?,?,?)",valores)
                print("Datos insertados correctamente")          
                break      
        except Error as e:
            print(e)
        except Exception:
            print(f"Se produjo el error: {sys.exc_info()}")
        finally:
            conn.close()

def menu_consultas_clientes():
    while True:
        print("\n\t--- Menú Consultas y Reportes ---")
        print("Listado de Clientes Registrados")
        print("1. Busqueda por clave")
        print("2. Busqueda por nombre")
        print("3. Volver al menú anterior (clientes)")
        ##listado de clientes
        opcion=int(input("Elija una opcion: "))
        if opcion==1:
            ordenar_por_clave_clientes()
        elif opcion==2:
            ordenar_por_nombre_clientes()
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
                    print("Clave \t Nombre de servicio")
                    for clave, nombre, rfc, correo  in clientes:
                        print(f"\n{clave} \t {nombre}\t {rfc}\t {correo}")
                else: 
                    print("No se encontraron coincidencias")
                    menu_reportes_servicios()
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
                mi_cursor.execute(("SELECT clave_cliente, cliente, RFC, correo FROM CLIENTES ORDER BY nombre"))
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("Listado de clientes ordenados por nombre:\n")
                    print("Clave \t Nombre de servicio")
                    for clave, nombre, rfc, correo  in clientes:
                        print(f"\n{clave} \t {nombre}\t {rfc}\t {correo}")
                else: 
                    print("No se encontraron coincidencias")
                    menu_reportes_servicios()
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()

def menu_notas():
    while True:
        print("\n--- Menú Taller Mecánico ---")
        print("1. Registrar una nota")
        print("2. Consultas y reportes")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota")
        print("5. Salir")
        opcion=int(input("Ingrese una opción: "))
        if opcion == 1:
            insertar_notas()
        elif opcion ==2:
            sub_menu_consultas()
        elif opcion == 3:
            cancelar_nota()
        elif opcion == 4:
            recuperar_nota_cancelada()
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
                    print("Clave \t Nombre de servicio")
                    for clave, nombre in clientes:
                        print(f"\n{clave} \t {nombre}")
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
            cliente_clave=int(input("Ingrese la clave del cliente: "))
            if cliente_clave==False:
                print("No puede dejar el campo vacío") ##arreglar la 
            if cliente_clave==True:
                break

        monto_pago = 0
        detalle = ""
        cant_servicios=0

        while True:
            servicio_clave=input("Ingrese la clave del servicio realizado (0 para cancelar): ") #Ingresar mas de un servicio
            if servicio_clave==0:
                break
            valores={"id_servicio":servicio_clave}
            costo_servicio=("SELECT costo_servicio FROM SERVICIOS WHERE id_servicio=:id_servicio", valores)
            servicio=("SELECT nombre_servicio FROM SERVICIOS WHERE id_servicio=:id_servicio", valores)

            monto_pago+=costo_servicio 
            sum_detalle=f"Servicio: {servicio}, Costo: {costo_servicio} \n"
            detalle+=sum_detalle
            cant_servicios+=1
            nombre_id_servicio=f"id_servicio{cant_servicios}"
            servicio[nombre_id_servicio]=servicio_clave
                
        promedio_monto=monto_pago/cant_servicios
                

            #nota["Folio"] = folio_num
        nota["Fecha"] = fecha
        nota["Estatus"] = False
        nota["Promedio_monto"]=promedio_monto
        nota["Monto_pago"] = monto_pago
        nota["clave_cliente"] = cliente_clave
        notas.append(nota)
        servicios_notas=list(servicio.values())


#insersión de datos en las notas
        try:
                with sqlite3.connect("PrimerIntentoDemo.db") as conn:
                    mi_cursor = conn.cursor()
                    mi_cursor.execute("INSERT INTO NOTAS (fecha, estatus, monto_promedio, monto_pago, clave_cliente)\
                                      (:Fecha,:Estatus,:Promedio_monto,:Monto_pago,:clave_cliente')",notas)
                    print(f"Datos insertados conrrectamente \nEl folio de la nota es {mi_cursor.lastrowid}")
                  ##  folio={"FOLIO":mi_cursor.lastrowid}
                  ##  folio_servicio=("SELECT FOLIO FROM NOTAS WHERE FOLIO=:FOLIO",folio)
                    folio=mi_cursor.lastrowid
                    for servicio in servicios_notas:
                        valores=(folio, servicios_notas)
                        mi_cursor.execute("INSERT INTO SERVICIOS_NOTAS (folio, ID_SERVICIO) \
                        VALUES(?,?)",valores)
                    print(f"La clave asignada a la nota fue {folio}")
        except Error as e:
                print (e)
        except:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
                conn.close()

def sub_menu_consultas(notas):
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
                consultar_por_rfc()
            elif subopcion=="4":
                menu_principal()
            else:
                print("Opción inválida. Por favor, elija una opción válida.")


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

def guardar_datos_csv(notas):
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

def consultar_por_periodo(): 
    notas_periodo = []
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
        return
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
            sub_menu_consultas()

def consultar_por_folio():
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
            sub_menu_consultas()   
##función para ordenar rfc 
def RFC_ORDENADO(RFC):
    return RFC['RFC']
#función para consultar por cliente
def consultar_por_rfc():
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
                sub_menu_consultas(notas) 
    if not folio_encontrado:
            print("No se encontró una nota válida para el folio ingresado.")

#función para cancelar notas
def cancelar_nota():
    while True:
        try: 
            with sqlite3.connect("BD_TALLER_MECANICO.db") as conn:
                mi_cursor=conn.cursor()
                valores={"folio":folio}
                mi_cursor.execute("SELECT NOTAS.FOLIO, NOTAS.FECHA, NOTAS.clave_cliente, FROM CLIENTES.cliente, CLIENTES.RFC\
                                   CLIENTES.correo, NOTAS.monto_pago, SERVICIOS.nombre_servicio, SERVICIOS.costo_servicio\
                                   FROM NOTAS INNER JOIN CLIENTES ON NOTAS.clave_cliente=CLIENTES.clave_cliente INNER JOIN SERVICIOS ON \
                                    NOTAS.id_servicio=SERVICIOS.id_servicio WHERE NOTAS.estatus=False", valores)#PENDIENTE LO DE LAS FECHAS 
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("NOTAS ENCONTRADAS:\n")
                    print("Folio \t Fecha \t Clave del cliente \t Nombre del cliente \t RFC\
                                   \tCorreo \tMonto de pago total \t Nombre del servicio \tCosto_servicio")
                    for Folio, Fecha,Clave_c, Nombre_c, RFC, Correo, monto_p, Servicio, costo_Servicio  in clientes:
                        print(f"\n{Folio} \t {Fecha}\t {Clave_c}\t {Nombre_c}\t {RFC}\t {Correo}\t {monto_p}\t {Servicio}\t {costo_Servicio}")
                
                print("¿Desea cancelar una nota?")
                cancelar=input()
                if cancelar.upper=="SI":
                    cancelar_folio=int(input("Ingrese el folio: "))
                    values={"folio":cancelar_folio}
                    mi_cursor.execute("UPDATE NOTAS SET estatus=True WHERE folio=:folio", values)
                else: 
                    print("No se encontraron coincidencias")
                    menu_reportes_servicios()
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
                mi_cursor.execute("SELECT NOTAS.FOLIO, NOTAS.FECHA, NOTAS.clave_cliente, FROM CLIENTES.cliente, CLIENTES.RFC\
                                   CLIENTES.correo, NOTAS.monto_pago, SERVICIOS.nombre_servicio, SERVICIOS.costo_servicio\
                                   FROM NOTAS INNER JOIN CLIENTES ON NOTAS.clave_cliente=CLIENTES.clave_cliente INNER JOIN SERVICIOS ON \
                                    NOTAS.id_servicio=SERVICIOS.id_servicio WHERE NOTAS.estatus=True")
                clientes = mi_cursor.fetchall()
                if clientes:
                    print("NOTAS ENCONTRADAS:\n")
                    print("Folio \t Fecha \t Clave del cliente \t Nombre del cliente \t RFC\
                                   \tCorreo \tMonto de pago total \t Nombre del servicio \tCosto_servicio")
                    for Folio, Fecha,Clave_c, Nombre_c, RFC, Correo, monto_p, Servicio, costo_Servicio  in clientes:
                        print(f"\n{Folio} \t {Fecha}\t {Clave_c}\t {Nombre_c}\t {RFC}\t {Correo}\t {monto_p}\t {Servicio}\t {costo_Servicio}")
                
                print("¿Desea cancelar una nota?")
                cancelar=input()
                if cancelar.upper=="SI":
                    cancelar_folio=int(input("Ingrese el folio: "))
                    values={"folio":cancelar_folio}
                    mi_cursor.execute("UPDATE NOTAS SET estatus=False WHERE folio=:folio", values)
                else: 
                    print("No se encontraron coincidencias")
                    menu_reportes_servicios()
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

        if opcion ==1:
            buscar_por_clave_servicio()
        elif opcion ==2:
            buscar_por_nombre_servicio()
        elif opcion ==3:
            print("\n--- Menú de listado de Servicios ---")
            print("1. Listado de servicios ordenados por clave")
            print("2. Listado de servicios ordenados por nombre") 
            listado_opcion=int(input("Seleccione una opción: "))  
            if listado_opcion==1:
                generar_reporte_servicios_por_clave()
            elif listado_opcion==2:
                generar_reporte_servicios_por_nombre()
        elif opcion ==4:
            menu_servicios()
            break #enduda
        else:
            print("Opción inválida. Por favor, elija una opción válida.")


def agregar_servicios():
    while True:
            try:
                nombre_servicio = input("Ingrese el nombre del servicio (no puede quedar vacío): ")
                if nombre_servicio.strip()=="":
                    print("El nombre del servicio no puede estar vacío. Intente nuevamente.")
                
                costo = float(input("Ingrese el costo del servicio (debe ser superior a 0.00): "))
                if costo <= 0.00:
                    print("El costo del servicio debe ser superior a 0.00. Intente nuevamente.")

                valores=(nombre_servicio, costo)
                with sqlite3.connect('BD_TALLER_MECANICO.db') as conn:
                    mi_cursor = conn.cursor()
                    mi_cursor.execute("INSERT INTO SERVICIOS (nombre_servicio, costo_servicio) VALUES (?, ?)", (valores))
                    conn.commit() ##algoahi
                    print("Servicio agregado con éxito.")
                    menu_servicios()
                    break #necesario?
            except ValueError:
                print("Error: Ingrese un valor numérico válido para el costo.")
            except Error as e:
                print(e)
            except:
                print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
            conn.close()


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


def generar_reporte_servicios_por_nombre():
    while True:
        try:
            conn = sqlite3.connect('BD_TALLER_MECANICO.db')
            cursor = conn.cursor()

            cursor.execute("SELECT * FROM SERVICIOS ORDER BY nombre_servicio")
            servicios = cursor.fetchall()

            if servicios:
                print("\nReporte de servicios ordenados por clave:\n")
                print("Clave \t Nombre de servicio \t Costo")
                for servicio in servicios:
                    print(f"{servicio[0]} \t {servicio[1]} \t {servicio[2]}")

                while True:
                    opcion = input("\n \nElija una opcion: 1. Exportar a CSV \n2. Exportar a Excel \n3. Regresar al menú de reportes: ")
                    if opcion == '1':
                        exportar_a_csv(servicios, "ReporteServiciosPorClave")
                        break
                    elif opcion == '2':
                        exportar_a_excel(servicios, "ReporteServiciosPorClave")
                        break
                    elif opcion == '3':
                        break
                    else:
                        print("Opción no válida. Intente nuevamente.")
        except Error as e:
            print (e)
        except Exception:
            print(f"Se produjo el siguiente error: {sys.exc_info()[0]}")
        finally:
            conn.close()


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
            break ##necesario?
        else:
            print("Opción inválida. Por favor, elija una opción válida.")


def menu_principal():
    while True:
        print("\n--- Menú Taller Mecánico ---")
        print("1. Notas")
        print("2. Clientes")
        print("3. Servicios")
        print("4. Salir")
        op=int(input("Por favor escoja una opción: "))
        if op == 1:
            menu_notas()
        elif op == 2:
            menu_clientes()
        elif op == 3:
            menu_servicios()
        elif op == 4:
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida. Por favor, elija una opción válida.")

def crear_tablas():
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
crear_tablas()
menu_principal()
