import datetime
import pandas as pd

##función para exportar a excel
def exportar_a_excel(datos, nombre_archivo):
    # Crear un DataFrame a partir de la lista de diccionarios
    df = pd.DataFrame(datos)
    
    # Guardar el DataFrame en un archivo Excel
    df.to_excel(nombre_archivo, index=False)

def consultar_por_periodo(notas):
    notas_periodo=[]
    fecha_inicial =datetime.datetime.strptime(input("Ingrese la fecha inicial dd/mm/aaaa: "),"%d/%m/%Y").date()
    fecha_final =datetime.datetime.strptime(input("Ingrese la fecha final dd/mm/aaaa: "),"%d/%m/%Y").date()
    for nota in notas:
        if fecha_inicial<=nota['Fecha'] <= fecha_final and nota['Estatus']==False:
            info_nota=(f"{nota['Folio']}\t{nota['Fecha']}\t{nota['Cliente']}\t{nota['Monto_pago']}") 
            notas_periodo.append(info_nota)
    if len(notas_periodo)==0:
        print("No hay notas registradas para el periodo especificado")
    else:
        print("Reporte de notas para el periodo especificado: ")
        print("Folio'\tFecha\tNombre\tCosto")
        for nota in notas_periodo:
            print(nota)


def consultar_por_folio(notas):
    folio =int(input("Ingrese el folio de la nota: "))
    for nota in notas:
        if nota['Folio'] == folio and nota['Estatus']==False:
            print("\nDetalle de la nota:\n")
            print(f"Folio: {nota['Folio']}\n")
            print(f"Fecha: {nota['Fecha']}\n")
            print(f"Nombre del cliente: {nota['Cliente']}\n")
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
            print(f"Servicio: {nota['Detalles']}\n")
            print(f"Costo del servicio: {nota['Monto_pago']}")
            print(f"Monto promedio: {nota['Promedio_costo']}")
            p_importar=input("¿Desea importar la información a excel? S/N")
            if p_importar.upper=="S":
                nombre_archivo=nota['RFC']"_"+datetime.datetime.today().date()
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
        folio_num=max(nota.keys(), default=1000)+1
        while True:
            try:
                fecha=datetime.datetime.strptime(input("Ingrese la fecha dd/mm/aaaa: "),"%d/%m/%Y").date()
                if fecha<datetime.datetime.today().date():
                    break
                else: 
                    print("Ingrese una fecha válida")  
            except Exception:
                print("Ingrese una fecha válida")    
        while True:
            cliente=input("Ingrese el nombre del cliente: ")
            if cliente.strip()=="":
                print("No puede dejar el campo vacío")
            else:break
        monto_pago=0
        detalle=""
        while True:
            servicio=input("Ingrese el detalle del servicio realizado (dejar vacío para cancelar): ") #Ingresar más de un servicio
            if servicio.strip()=="":
                break
            while True:
                try:
                    costo_servicio=float(input("Ingrese el costo del servicio: "))
                    costo_servicio!=0
                    break
                except Exception:
                    print("Ingrese una cantidad")
            monto_pago+=costo_servicio #suma de los costos del servicio
            sum_detalle=(f"Servicio: {servicio}, Costo: {costo_servicio} \n")
            detalle+=sum_detalle
            promedio=monto_pago/len
            cancelada=False

        nota["Folio"]=(folio_num)
        nota["Fecha"]=(fecha)
        nota["Cliente"]=(cliente)
        nota["Monto_pago"]=(monto_pago)
        nota["Detalles"]=(detalle)
        nota["Estatus"]=(cancelada)
        nota["Promedio_costo"]=(promedio)
        notas.append(nota)
        print("El folio es:", nota["Folio"])
        for x in notas:
            fechas=x['Fecha']

        
    elif opcion == "2":
        print("\n--- Submenú Consultas y Reportes ---")
        print("1. Consulta por período")
        print("2. Consulta por folio")
        subopcion = input("Seleccione una opción: ")
        if subopcion == "1":
            consultar_por_periodo(notas)
        elif subopcion == "2":
            consultar_por_folio(notas)
        else:
            print("Opción inválida. Por favor, elija una opción válida.")
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
