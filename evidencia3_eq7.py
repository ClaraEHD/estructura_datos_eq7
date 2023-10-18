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
            nota["Correo"]= correoelectronico
            nota["Monto_pago"] = monto_pago
            nota["Detalles"] = detalle
            nota["Estatus"] = False
            nota["Promedio_monto"]=promedio_monto
            notas.append(nota)
            print(f"El folio es: {nota['Folio']}")


lif opcion == "2":
            sub_menu_consultas(notas, notas_canceladas)

        elif opcion == "3":
            cancelar_nota(notas,notas_canceladas)
        elif opcion == "4":
            recuperar_nota_cancelada(notas,notas_canceladas)
        elif opcion == "5":
            confirmacion_salida = input("¿Está seguro de que desea salir? (si/no): ")
            if confirmacion_salida.lower() == 'si':
                print("¡Hasta luego!")
                guardar_datos_csv(notas)
                break
        else:
            print("Opción inválida. Por favor, elija una opción válida.")
