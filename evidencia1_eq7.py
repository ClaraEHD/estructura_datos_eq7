import datetime
def agregar_nota(notas):
    nota={}
    folio=max(nota.keys(), default=1000)+1
    while True:
        try:
            fecha=datetime.datetime.strptime(input("Ingrese la fecha dd/mm/aaaa: "),"%d/%m/%Y").date()
            fecha<datetime.datetime.today().date()
            break
        except Exception:
            print("Ingrese una fecha válida")    
    cliente=input("Ingrese el nombre del cliente: ")
    monto_pago=0
    detalle=""
    while True:
        servicio=input("Ingrese el detalle del servicio realizado: ") #Ingresar más de un servicio
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

    nota[folio]=(cliente, fecha, monto_pago, detalle)
    print(costo_servicio)

def consultar_por_periodo(notas):
    fecha_inicial = input("Ingrese la fecha inicial (YYYY-MM-DD): ")
    fecha_final = input("Ingrese la fecha final (YYYY-MM-DD): ")
    notas_periodo = [nota for nota in notas if nota['fecha'] >= fecha_inicial and nota['fecha'] <= fecha_final]
    
    if notas_periodo:
        print("\nReporte de notas por período:")
        print("Folio\tNombre\tServicio\tCosto")
        for nota in notas_periodo:
            print(f"{nota['folio']}\t{nota['nombre']}\t{nota['servicio']}\t{nota['costo']}")
    else:
        print("No hay notas registradas para el período especificado.")

def consultar_por_folio(notas):
    folio = input("Ingrese el folio de la nota: ")
    for nota in notas:
        if nota['folio'] == folio and not nota['cancelada']:
            print("\nDetalle de la nota:")
            print(f"Folio: {nota['folio']}")
            print(f"Nombre del cliente: {nota['nombre']}")
            print(f"Tipo de servicio: {nota['servicio']}")
            print(f"Costo del servicio: {nota['costo']}")
            return
    print("No se encontró una nota válida para el folio ingresado.")

def cancelar_nota(notas, notas_canceladas):
    folio = input("Ingrese el folio de la nota a cancelar: ")
    for nota in notas:
        if nota['folio'] == folio and not nota['cancelada']:
            print("\nDetalle de la nota a cancelar:")
            print(f"Folio: {nota['folio']}")
            print(f"Nombre del cliente: {nota['nombre']}")
            print(f"Tipo de servicio: {nota['servicio']}")
            print(f"Costo del servicio: {nota['costo']}")
            confirmacion = input("¿Desea confirmar la cancelación de esta nota? (si/no): ")
            if confirmacion.lower() == 'si':
                nota['cancelada'] = True
                notas_canceladas.append(nota)
                print("Nota cancelada con éxito.")
            return
    print("No se encontró una nota válida para el folio ingresado.")

def recuperar_nota_cancelada(notas_canceladas):
    print("\nNotas canceladas disponibles:")
    print("Folio\tNombre")
    for nota in notas_canceladas:
        print(f"{nota['folio']}\t{nota['nombre']}")
    
    folio_recuperar = input("Ingrese el folio de la nota cancelada que desea recuperar (o 'no' para cancelar): ")
    if folio_recuperar == 'no':
        return None
    
    for nota in notas_canceladas:
        if nota['folio'] == folio_recuperar:
            print("\nDetalle de la nota cancelada a recuperar:")
            print(f"Folio: {nota['folio']}")
            print(f"Nombre del cliente: {nota['nombre']}")
            print(f"Tipo de servicio: {nota['servicio']}")
            print(f"Costo del servicio: {nota['costo']}")
            confirmacion = input("¿Desea confirmar la recuperación de esta nota cancelada? (s/n): ")
            if confirmacion.lower() == 's':
                notas_canceladas.remove(nota)
                return nota
            else:
                return None
    print("No se encontró una nota cancelada válida para el folio ingresado.")
    return None

def menu():
    notas = []
    notas_canceladas = []
    folio_actual = 1
    
    while True:
        print("\n--- Menú Taller Mecánico ---")
        print("1. Registrar una nota")
        print("2. Consultas y reportes")
        print("3. Cancelar una nota")
        print("4. Recuperar una nota")
        print("5. Salir")
        
        opcion = input("Seleccione una opción: ")
        
        if opcion == "1":
            agregar_nota(notas)
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
            cancelar_nota(notas, notas_canceladas)
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

if __name__ == "__main__":
    menu()
