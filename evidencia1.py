import datetime


#AQUI VA EL MENÚ
import uuid
import datetime

class Servicio:
    def __init__(self, nombre, costo):
        self.nombre = nombre
        self.costo = costo

class Nota:
    def __init__(self, cliente):
        self.folio = str(uuid.uuid4())[:8]
        self.fecha = datetime.datetime.now()
        self.cliente = cliente
        self.servicios = []

    def agregar_servicio(self, servicio):
        self.servicios.append(servicio)

    def calcular_monto_total(self):
        return sum(servicio.costo for servicio in self.servicios)

def ingresar_servicio():
    nombre = input("Nombre del servicio: ")
    costo = float(input("Costo del servicio: "))
    while costo <= 0:
        print("El costo debe ser mayor que cero.")
        costo = float(input("Costo del servicio: "))
    return Servicio(nombre, costo)

def crear_nota():
    cliente = input("Nombre del cliente: ")
    nota = Nota(cliente)

    while True:
        servicio = ingresar_servicio()
        nota.agregar_servicio(servicio)
        if input("¿Agregar otro servicio? (S/N): ").strip().lower() != 's':
            break

    return nota

def mostrar_nota(nota):
    print("\n--- Nota ---")
    print(f"Folio: {nota.folio}")
    print(f"Fecha: {nota.fecha}")
    print(f"Cliente: {nota.cliente}")
    print("Servicios:")
    for idx, servicio in enumerate(nota.servicios, start=1):
        print(f"{idx}. {servicio.nombre}: ${servicio.costo:.2f}")
    print(f"Total a pagar: ${nota.calcular_monto_total():.2f}")

def main():
    print("Bienvenido al sistema de registro de notas de servicios del taller mecánico.")
    
    nota = crear_nota()
    mostrar_nota(nota)

if __name__ == "__main__":
    main()

#MANEJAR EL MENÚ CON UN MATCH

    #REGISTRAR UNA NOTA 
nota={}
folio=max(nota.keys(), default=1000)+1
fecha=datetime.datetime.today().date()
cliente=input("Ingrese el nombre del cliente: ")
monto_pago=0
detalle=""
while True:
    servicio=input("Ingrese el detalle del servicio realizado: ") #Ingresar más de un servicio
    if servicio.strip()=="":
        break
    costo_servicio=float(input("Ingrese el costo del servicio: "))
    monto_pago+=costo_servicio #suma de los costos del servicio
    sum_detalle=(f"Servicio: {servicio}, Costo: {costo_servicio} \n")
    detalle+=sum_detalle

nota[folio]=(cliente, fecha, monto_pago, detalle)
print(detalle)
print(nota)



    #CONSULTAS Y REPORTES

    #CANCELAR UNA NOTA

    #RECUPERAR UNA NOTA
