import datetime
import pandas as pd
import re
import os
import csv

def menu_principal(notas, notas_canceladas):
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
                cliente=input("Ingrese el nombre del cliente: ")
                if cliente.strip() !="":
                    break
                else:
                    print("No puede dejar el campo vacío")
    
            while True:
                rfc = input("Por favor, ingrese su RFC: ")
                if validar_rfc(rfc):
                    break
                else:
                    print(f"RFC {rfc} no válido. Ingrese un RFC válido.")
            
            monto_pago = 0
            detalle = ""
            cant_servicios=0
            
            while True:
                # Pedir al usuario que ingrese un correo
                correoelectronico = input("Ingresa un correo electrónico: ")
                if (correoelectronico.strip()==""):
                    print("El correo no puede ser omitido")
                elif (validar_correo(correoelectronico)):
                    break 
            
            while True:
                servicio=input("Ingrese el detalle del servicio realizado (dejar vacío para cancelar): ") #Ingresar mas de un servicio
                if servicio.strip()=="":
                    break
                while True:
                    try:
                        costo_servicio=float(input("Ingrese el costo del servicio: "))
                        if costo_servicio!=0:
                            break
                    except ValueError:
                        print("Ingrese una cantidad valida. ")

                monto_pago+=costo_servicio #suma de los costos del servicio
                sum_detalle=f"Servicio: {servicio}, Costo: {costo_servicio} \n"
                detalle+=sum_detalle
                cant_servicios+=1
            promedio_monto=monto_pago/cant_servicios
                

            nota["Folio"] = folio_num
            nota["Fecha"] = fecha
            nota["Cliente"] = cliente
            nota["RFC"] = rfc 
            nota["Monto_pago"] = monto_pago
            nota["Detalles"] = detalle
            nota["Estatus"] = False
            nota["Promedio_monto"]=promedio_monto
            notas.append(nota)
            print(f"El folio es: {nota['Folio']}")

            
        elif opcion == "2":
            print("\n--- Submenú Consultas y Reportes ---")
            print("1. Consulta por período")
            print("2. Consulta por folio")
            print("3. Consulta por cliente")
            print("4. Regresa al menú principal")
            subopcion = input("Seleccione una opción: ")
            sub_menu_consultas(subopcion)

        elif opcion == "3":
            nota_cancelar=cancelar_nota(notas)
            notas_canceladas.append(nota_cancelar)
        elif opcion == "4":
            nota_recuperada = recuperar_nota_cancelada(notas_canceladas)
            if nota_recuperada:
                notas.append(nota_recuperada)
                print("Nota cancelada recuperada con éxito.")
        elif opcion == "5":
            confirmacion_salida = input("¿Está seguro de que desea salir? (si/no): ")
            if confirmacion_salida.lower() == 'si':
                print("¡Hasta luego!")
                break
        else:
            print("Opción inválida. Por favor, elija una opción válida.")


def sub_menu_consultas(opcion):
            if opcion == "1":
                consultar_por_periodo(notas)
            elif opcion == "2":
                consultar_por_folio(notas)
            elif opcion == "3":
                consultar_por_rfc(notas)
            elif opcion=="4":
                menu_principal()
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

archivo_csv = "datos.csv"

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
        
def comprobar_existencia_archivo():
    return os.path.exists(archivo_csv)

def  leer_datos_desde_csv():
    datos = []
    with open(archivo_csv, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for fila in reader:
            datos.append(fila)
    return datos


def consultar_por_periodo(notas): 
    notas_periodo = []
    try:
        fecha_inicial_str = input("Ingrese la fecha inicial dd/mm/aaaa (deje en blanco para usar 01/01/2000): ")
        if fecha_inicial_str.strip() == '':
            fecha_inicial = datetime.date(2000, 1, 1)
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
        if fecha_inicial <= nota['Fecha'] <= fecha_final and not nota['Estatus']:
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


def consultar_por_folio(notas):
    folio =int(input("Ingrese el folio de la nota: "))
    for nota in notas:
        if nota['Folio'] == folio and nota['Estatus']==False:
            print("\nDetalle de la nota:\n")
            print(f"Folio: {nota['Folio']}\n")
            print(f"Fecha: {nota['Fecha']}\n")
            print(f"Nombre del cliente: {nota['Cliente']}\n")
            print(f"RFC: {nota['RFC']}\n")
            print(f"Servicio: {nota['Detalles']}\n")
            print(f"Costo del servicio: {nota['Monto_pago']}")
        else:
            print("No se encontró una nota válida para el folio ingresado.")

##función para ordenar rfc 
def RFC_ORDENADO(RFC):
    return RFC['RFC']
def consultar_por_rfc(notas):
    rfc_ordenado=sorted(notas, key=RFC_ORDENADO)
    for nota in rfc_ordenado:
        print("RFC del cliente: ", nota['RFC'], "   Folio: ", nota['Folio'])

    folio =int(input("Ingrese el RFC de la persona que desea consultar: "))
    for nota in notas:
        if nota['Folio'] == folio and nota['Estatus']==False:
            print("\nDetalle de la nota:\n")
            print(f"Folio: {nota['Folio']}\n")
            print(f"Fecha: {nota['Fecha']}\n")
            print(f"Nombre del cliente: {nota['Cliente']}\n")
            print(f"RFC: {nota['RFC']}\n")
            print(f"Servicio: {nota['Detalles']}\n")
            print(f"Costo del servicio: {nota['Monto_pago']}")
            print(f"Monto promedio: {nota['Promedio_monto']}")
            p_importar=input("¿Desea importar la información a excel? S/N")
            if p_importar.upper=="S":
                nombre_archivo=nota['RFC']+"_"+datetime.datetime.today().date()
                exportar_a_excel(notas, nombre_archivo)
                print(f'Datos exportados a {nombre_archivo}') ##pendiente ubicación de archivo 
        else:
            print("No se encontró una nota válida para el folio ingresado.")

def cancelar_nota(notas):
    folio = int(input("Ingrese el folio de la nota a cancelar: "))
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
                return nota
                
        else:
            print("No se encontró una nota válida para el folio ingresado.")

def recuperar_nota_cancelada(notas_canceladas):
    print("\nNotas canceladas disponibles:")
    print("Folio\tNombre")
    for nota in notas_canceladas:
        print(f"{nota['Folio']}\t{nota['Cliente']}\n")
    try:
        folio_recuperar =int(input("Ingrese el folio de la nota cancelada que desea recuperar (o 'no' para cancelar): "))
        
    except ValueError:
        print("\nVolviendo al menu ")
        return None
    
    for nota in notas_canceladas:
        if nota['Folio'] == folio_recuperar:
            print("\nDetalle de la nota cancelada a recuperar:")
            print(f"Folio: {nota['Folio']}")
            print(f"Nombre del cliente: {nota['Cliente']}")
            print(f"RFC: {nota['RFC']}\n")
            print(f"Tipo de servicio: {nota['Detalles']}")
            print(f"Costo del servicio: {nota['Monto_pago']}")
            confirmacion = input("¿Desea confirmar la recuperación de esta nota cancelada? (s/n): ")
            if confirmacion.lower() == "s" or confirmacion.lower() == "n":
                print("La nota fue recuperada con éxito")
            else:
                return nota
    print("No se encontró una nota cancelada válida para el folio ingresado.")
    return None


notas=list()
notas_canceladas=list()

# Comprobar la existencia del archivo CSV
if comprobar_existencia_archivo():
    datos_recuperados = leer_datos_desde_csv()
    print("Se ha recuperado el estado de la aplicación a partir del archivo CSV.")
    print("Datos recuperados:", datos_recuperados)
else:
    print("No se ha encontrado un archivo CSV existente.")
    print("Se parte de un estado inicial vacío.")
    
menu_principal(notas, notas_canceladas)
