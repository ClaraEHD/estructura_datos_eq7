import datetime
import pandas as pd
import re
import os
import csv
import sqlite3

def menu_principal(notas,clientes,servicios):
    while True:
        print("\n--- Menú Taller Mecánico ---")
        print("1. Registrar una nota")
        print("2. Consultas y reportes")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota")
        print("5. Salir")
            
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            nota={}
            folio_num = len(notas) + 1
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
                if cliente_clave:
                    break
                elif cliente_clave==False:
                    print("No puede dejar el campo vacío") ##arreglar la validación
                    cliente=1
                #aquí se agrega el nombre, rfc, correo desde la base de datos

           # while True:
            #    rfc = input("Por favor, ingrese su RFC: ")
             #   if validar_rfc(rfc):
              #      break
               # else:
                #    print(f"RFC {rfc} no válido. Ingrese un RFC válido.")
            
            monto_pago = 0
            detalle = ""
            cant_servicios=0
            
          #  while True:
                # Pedir al usuario que ingrese un correo
           #     correoelectronico = input("Ingresa un correo electrónico: ")
            #    if (correoelectronico.strip()==""):
             #       print("El correo no puede ser omitido")
              #  elif (validar_correo(correoelectronico)):
               #     break 
            
            while True:
                servicio_clave=input("Ingrese la clave del servicio realizado (0 para cancelar): ") #Ingresar mas de un servicio
                if servicio_clave==0:
                    break
                costo_servicio=1#agregar un select de la base de datos
                servicio=1#agreagr un select de la base de datos 
    

                monto_pago+=costo_servicio #suma de los costos del servicio
                sum_detalle=f"Servicio: {servicio}, Costo: {costo_servicio} \n"
                detalle+=sum_detalle
                cant_servicios+=1
            promedio_monto=monto_pago/cant_servicios
                

            nota["Folio"] = folio_num
            nota["Fecha"] = fecha
            nota["Cliente"] = cliente
            nota["RFC"] = 1#pendiente también
            nota["Correo"]= 1 #pendiente
            nota["Monto_pago"] = monto_pago
            nota["Detalles"] = detalle
            nota["Estatus"] = False
            nota["Promedio_monto"]=promedio_monto
            notas.append(nota)
            print(f"El folio es: {nota['Folio']}")


        elif opcion == "2":
            sub_menu_consultas(notas)

        elif opcion == "3":
            cancelar_nota(notas)
        elif opcion == "4":
            recuperar_nota_cancelada(notas)
        elif opcion == "5":
            confirmacion_salida = input("¿Está seguro de que desea salir? (si/no): ")
            if confirmacion_salida.lower() == 'si':
                print("¡Hasta luego!")
                guardar_datos_csv(notas)
                break
        else:
            print("Opción inválida. Por favor, elija una opción válida.")


def sub_menu_consultas(notas):
            print("\n--- Submenú Consultas y Reportes ---")
            print("1. Consulta por período")
            print("2. Consulta por folio")
            print("3. Consulta por cliente")
            print("4. Regresa al menú principal")
            subopcion = input("Seleccione una opción: ")
            if subopcion == "1":
                consultar_por_periodo(notas)
            elif subopcion == "2":
                consultar_por_folio(notas)
            elif subopcion == "3":
                consultar_por_rfc(notas)
            elif subopcion=="4":
                menu_principal(notas)
            else:
                print("Opción inválida. Por favor, elija una opción válida.")

##función para exportar a excel

def exportar_a_excel(datos, nombre_archivo):
    # Crear un DataFrame a partir de la lista de diccionarios
    
    df = pd.DataFrame(datos)
    
    # Guardar el DataFrame en un archivo Excel
    
    df.to_excel(nombre_archivo, index=False)

def validar_rfc(rfc):
    # Expresion regular para validar el RFC 
    patron = r'^[A-Z&Ñ]{3,4}\d{6}[A-V1-9][0-9A-Z]([0-9A])?$'
    
    # Utiliza re.fullmatch para verificar si la cadena cumple con el patrón
    return bool(re.fullmatch(patron, rfc))

archivo_csv = "Datos_taller_mecanico.csv"


#Funcion para validar correo electronico
def validar_correo(correoelectronico):
    Filtro = r'^[\w\.]+@[\w\.]+$'    
    # Validar el correo
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

def comprobar_existencia_archivo():
    return os.path.exists(archivo_csv)

def leer_datos_desde_csv():
    notas = []
    with open(archivo_csv, 'r', newline='')as archivo:
        lector = csv.reader(archivo)
        next(lector)
        for Folio, Fecha, Cliente, RFC, Correo, Monto_pago, Detalles, Estatus, Promedio_monto in lector:
            nota=dict()
            nota['Folio']=int(Folio)
            nota['Fecha']=datetime.datetime.strptime(Fecha, '%Y-%m-%d').date()
            nota['Cliente']=Cliente
            nota['RFC']=RFC
            nota['Correo']=Correo
            nota['Monto_pago']=float(Monto_pago)
            nota['Detalles']=Detalles
            nota['Estatus']=Estatus
            nota['Promedio_monto']=float(Promedio_monto)
            if nota['Estatus']=='False':
                nota['Estatus']=False
                notas.append(nota)
            elif nota['Estatus']=='True':
                nota['Estatus']==True
                notas.append(nota)
    return notas

def consultar_por_periodo(notas): 
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
    
    total_monto = 0
    count_notas = 0

    for nota in notas:
        if fecha_inicial <= nota['Fecha'] <= fecha_final and nota['Estatus']==False:
            total_monto += nota['Monto_pago']
            count_notas += 1
            notas_periodo.append(nota)
        if not notas_periodo:
            print("No hay notas registradas para el período especificado.")
    else:
        promedio_monto = total_monto / count_notas if count_notas > 0 else 0
        print("Reporte de notas para el período especificado: ")
        print("Folio\tFecha\tNombre\tCosto")
        for nota in notas_periodo:
            print(f"{nota['Folio']}\t{nota['Fecha']}\t{nota['Cliente']}\t{nota['Monto_pago']:.2f}")
        print(f"\nMonto promedio de las notas en el período: {promedio_monto:.2f}")
    sub_menu_consultas(notas)

def consultar_por_folio(notas):
    folio =int(input("Ingrese el folio de la nota: "))
    nota_encontrada=False
    for nota in notas:    
        if nota['Folio'] == folio and nota['Estatus']==False:
            print("\nDetalle de la nota:\n")
            print(f"Folio: {nota['Folio']}\n")
            print(f"Fecha: {nota['Fecha']}\n")
            print(f"Nombre del cliente: {nota['Cliente']}\n")
            print(f"RFC: {nota['RFC']}\n")
            print(f"Servicio: {nota['Detalles']}\n")
            print(f"Costo del servicio: {nota['Monto_pago']}")
            nota_encontrada=True
            break
    if not nota_encontrada:
        print("No se encontró una nota válida para el folio ingresado.")
    sub_menu_consultas(notas)

##función para ordenar rfc 
def RFC_ORDENADO(RFC):
    return RFC['RFC']
#función para consultar por cliente
def consultar_por_rfc(notas):
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
def cancelar_nota(notas):
    folio = int(input("Ingrese el folio de la nota a cancelar: "))
    nota_encontrada=False
    for nota in notas:
        if nota['Folio'] == folio and nota['Estatus']==False:
            print("\nDetalle de la nota a cancelar:\n")
            print(f"Folio: {nota['Folio']}\n")
            print(f"Fecha: {nota['Fecha']}\n")
            print(f"Nombre del cliente: {nota['Cliente']}\n")
            print(f"RFC: {nota['RFC']}\n")
            print(f"Tipo de servicio: {nota['Detalles']}\n")
            print(f"Costo del servicio: {nota['Monto_pago']}\n")
            confirmacion = input("¿Desea confirmar la cancelación de esta nota? (si/no): ")
            if confirmacion.lower() == 'si':
                nota['Estatus'] = True
                print("Nota cancelada con éxito.")
                nota_encontrada=True
                return notas
            print("\nVolviendo al menu ")
    if not nota_encontrada:
        print("No se encontró una nota válida para el folio ingresado.")
        print("\nVolviendo al menu ")

#función para recuperar una nota cancelada
def recuperar_nota_cancelada(notas):
    print("\nNotas canceladas disponibles:")
    print("Folio\tNombre")
    for nota in notas:
        if nota["Estatus"]==True:
            print(f"{nota['Folio']}\t{nota['Cliente']}\n")
    try:
        folio_recuperar =int(input("Ingrese el folio de la nota cancelada que desea recuperar (o 'no' para cancelar): "))
    except ValueError:
        print("\nVolviendo al menu ")
        return None
    
    for nota in notas:
        if nota['Folio'] == folio_recuperar:
            print("\nDetalle de la nota cancelada a recuperar:")
            print(f"Folio: {nota['Folio']}")
            print(f"Nombre del cliente: {nota['Cliente']}")
            print(f"RFC: {nota['RFC']}\n")
            print(f"Tipo de servicio: {nota['Detalles']}")
            print(f"Costo del servicio: {nota['Monto_pago']}")
            confirmacion = input("¿Desea confirmar la recuperación de esta nota cancelada? (SI/NO): ")
            if confirmacion.lower() == "si":
                print("La nota fue recuperada con éxito")
                nota['Estatus']=False
                return notas 
            else:
                return None
            
    print("No se encontró una nota cancelada válida para el folio ingresado.")
    print("\nVolviendo al menu ")
    return None


notas=list()
clientes=list()
servicios=list()

# Comprobar la existencia del archivo CSV
if comprobar_existencia_archivo():
    notas=leer_datos_desde_csv()
    print("Se ha recuperado el estado de la aplicación a partir del archivo CSV.")
    print("Datos recuperados:")
    for nota in notas:
        if nota["Estatus"]==False:
            print("Notas vigentes: \n ", nota)
        elif nota["Estatus"]==True:
            print("Notas canceladas: \n ", nota)
else:
    print("No se ha encontrado un  CSV existente.")
    print("Se parte de un estado inicial vacío.")
    
menu_principal(notas,clientes,servicios)

def agregar_servicios(servicios):
    #clave unica que tiene que ser generada automaticamente id_servicio
    while True:
            try:
                nombre_servicio = input("Ingrese el nombre del servicio (no puede quedar vacío): ")
                if not nombre_servicio.strip():
                    print("El nombre del servicio no puede estar vacío. Intente nuevamente.")
                    continue
                
                costo = float(input("Ingrese el costo del servicio (debe ser superior a 0.00): "))
                if costo <= 0.00:
                    print("El costo del servicio debe ser superior a 0.00. Intente nuevamente.")
                    continue

                # Insertara los datos en la tabla
                conn = sqlite3.connect('BD_TALLER_MECANICO.db')
                cursor = conn.cursor()
                cursor.execute("INSERT INTO SERVICIOS (NOMBRE_SERVICIO, COSTO) VALUES (?, ?, ?, ?)", (nombre_servicio, costo))
                conn.commit()
                print("Servicio agregado con éxito.")
                break
            except ValueError:
                print("Error: Ingrese un valor numérico válido para el costo.")

            conn.close()

def buscar_por_clave_servicio():
    conn = sqlite3.connect('BD_TALLER_MECANICO.db')
    cursor = conn.cursor()

    # Mostrar el listado tabular de claves y nombres de servicio mediante sentencia select
    cursor.execute("SELECT ID_SERVICIO, NOMBRE_SERVICIO FROM SERVICIOS")
    servicios = cursor.fetchall()

    # Imprimir el listado tabular
    print("Listado de servicios:\n")
    print("Clave \t Nombre de servicio")
    for servicio in servicios:
        print(f"{servicio[0]} \t {servicio[1]}")

    # Pedir al usuario que elija una clave
    while True:
        try:
            clave_elegida = int(input("\nElija una clave de servicio: "))
            break
        except ValueError:
            print("Ingrese un valor numérico para la clave.")

    # Se realiza la consulta select para obtener el detalle del servicio asociado con esa clave
    cursor.execute("SELECT * FROM SERVICIOS WHERE ID_SERVICIO=?", (clave_elegida,))
    servicio_elegido = cursor.fetchone()

    # Imprimir el detalle del servicio
    if servicio_elegido:
        print("\nDetalle del servicio:\n")
        print(f"Clave: {servicio_elegido[0]}")
        print(f"Nombre de servicio: {servicio_elegido[1]}")
        print(f"Costo: {servicio_elegido[2]}")
    else:
        print("No se encontró ningún servicio con la clave ingresada.")

    conn.close()

def buscar_por_nombre_servicio():
    conn = sqlite3.connect('BD_TALLER_MECANICO.db')
    cursor = conn.cursor()

    # Pedir al usuario que ingrese el nombre del servicio a buscar
    nombre_servicio_buscar = input("Ingrese el nombre del servicio a buscar: ")

    # Realizar la consulta SELECT con el filtro de nombre de servicio (ignorando mayúsculas y minúsculas)
    cursor.execute("SELECT * FROM SERVICIOS WHERE UPPER(NOMBRE_SERVICIO) = UPPER(?)", (nombre_servicio_buscar,))
    servicios_encontrados = cursor.fetchall()

    # Imprimir el reporte de detalles de los servicios encontrados
    if servicios_encontrados:
        print("\nDetalle del servicio/es encontrado/s:\n")
        for servicio in servicios_encontrados:
            print(f"Clave: {servicio[0]}")
            print(f"Nombre de servicio: {servicio[1]}")
            print(f"Costo: {servicio[2]}\n")
    else:
        print(f"No se encontró ningún servicio con el nombre '{nombre_servicio_buscar}'.")
    conn.close()