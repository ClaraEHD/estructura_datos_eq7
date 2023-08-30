import datetime


#AQUI VA EL MENÚ
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