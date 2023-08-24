import concurrent.futures
import csv
import os
import random
import re
import string
import tkinter as tk
from datetime import date, datetime
from tkinter import filedialog
from tkinter import ttk

import requests_pkcs12

def cargar_csv():
    archivo = filedialog.askopenfilename(filetypes=[('Archivos CSV', '*.csv')])

    if archivo:
        try:
            with open(archivo, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.DictReader(csv_file)
                datos = {re.sub(r'\W+', '', header): [] for header in csv_reader.fieldnames}

                for fila in csv_reader:
                    for header, valor in fila.items():
                        datos[re.sub(r'\W+', '', header)].append(valor)

                # Utilizar los datos almacenados en el diccionario 'datos'
                dba = datos['MerchantDBAName']
                solution = datos['SolutionType']
                SID = datos['SID']
                MID = datos['MID']
                TID = datos['TID']
                MCC = datos['MCC']
                prosa = datos['Prosa']
                street = datos['Street']
                colony = datos['Colony']
                city = datos['City']
                state = datos['State']
                CP = datos['CP']
                contact = datos['Contact']
                email = datos['Email']
                phone = datos['Phone']

                # Procesar los datos según sea necesario
                for i in range(len(SID)):
                    # Obtener los valores específicos de la fila actual
                    current_dba = dba[i]
                    current_solution = solution[i]
                    current_SID = SID[i]
                    current_MID = MID[i]
                    current_TID = TID[i]
                    current_MCC = MCC[i]
                    current_prosa = prosa[i]
                    current_street = street[i]
                    current_colony = colony[i]
                    current_city = city[i]
                    current_state = state[i]
                    current_CP = CP[i]
                    current_contact = contact[i]
                    current_email = email[i]
                    current_phone = phone[i]
                    
                    # Realizar el procesamiento específico para cada fila de datos
                    if current_solution == 'Payment URL':
                        # Generar sharedsecret
                        sharedsec = generar_texto_alfanumerico(10)

                        # Crear el contenido XML específico para Payment URL
                        soap_xml = f'''
                        <!-- Aquí debes construir el contenido XML necesario para Payment URL -->
                        '''

                        # Realizar la petición SOAP para Payment URL
                        apireq = executor.submit(payment_url_req,
                                                baseURL, apiUser, apiPassword, p12path, CertPwd,
                                                current_SID, storepass, current_MCC, current_dba,
                                                reseller, currency, dtToday, acq, current_street,
                                                current_colony, current_CP, current_city, current_state,
                                                current_contact, current_email, current_phone, sharedsec,
                                                current_MID, current_MID, current_TID, current_MID, limit)

                        # Esperar el resultado de la petición y almacenar la respuesta
                        resultado_apireq = apireq.result()
                        responses.append(resultado_apireq)
                        responses_xml.append(resultado_apireq.text)

                        # Almacenar el sharedsecret generado
                        sharedsecrets.append(sharedsec)


                    elif current_solution == 'Link de Pago':
                        # Crear el contenido XML específico para Link de Pago
                        soap_xml = f'''
                        <!-- Aquí debes construir el contenido XML necesario para Link de Pago -->
                        '''

                        # Realizar la petición SOAP para Link de Pago
                        apireq = executor.submit(link_pago_req,
                                                baseURL, apiUser, apiPassword, p12path, CertPwd,
                                                current_SID, storepass, current_MCC, current_dba,
                                                reseller, currency, dtToday, acq, current_street,
                                                current_colony, current_CP, current_city, current_state,
                                                current_contact, current_email, current_phone,
                                                current_MID, current_MID, current_TID, current_MID, limit)

                        # Esperar el resultado de la petición y almacenar la respuesta
                        resultado_apireq = apireq.result()
                        responses.append(resultado_apireq)
                        responses_xml.append(resultado_apireq.text)

                    
                environment_value = environment.get()

                if environment_value == 'test':
                    process_data_for_environment(datos, 'test')

                if environment_value == 'prod':
                    process_data_for_environment(datos, 'prod')

                respuesta.config(text="Archivo cargado exitosamente.", fg="green")
        except Exception as e:
            respuesta.config(text="Error al cargar el archivo", fg="red")
            print(str(e))

def process_data_for_environment(datos, env):
    # Configuraciones específicas para cada entorno
    config = get_environment_config(env)
    
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_request, datos['SID'], datos['MerchantDBAName'], config))

    # Resto del código para guardar los resultados y generar el CSV
    # ...

def process_request(SID, dba, config):
    # Procesamiento de cada solicitud
    # ...

    # Ejemplo de llamada a la función para enviar la solicitud SOAP
    response = send_soap_request(config, SID, dba)
    
    return response

def send_soap_request(config, SID, dba):
    # Envío de solicitud SOAP
    # ...

    return response

def get_environment_config(env):
    if env == 'test':
        return {
            'baseURL': "https://test.ipg-online.com/mcsWebService",
            'apiPassword': "tester02",
            'apiUser': "WSIPG",
            'CertPwd': 'IPGAPI',
            'p12path': r'C:\Users\FISERV\Documents\p12_masivo\test\test.p12'
            # ... Otras configuraciones específicas para el entorno de test
        }
    elif env == 'prod':
        return {
            'baseURL': "https://www2.ipg-online.com/mcsWebService",
            'apiPassword': "z>GiE69~sh",
            'apiUser': "WST315869._.1",
            'CertPwd': 'password',
            'p12path': r'C:\Users\FISERV\Documents\p12_masivo\fdmx\fdmx.p12'
            # ... Otras configuraciones específicas para el entorno de producción
        }

# Resto del código para crear la ventana y GUI
# ...

ventana.mainloop()
