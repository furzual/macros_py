from numba import njit
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import csv
import re
import os
from flask import Flask, send_file
import random
import string
from datetime import date
from datetime import datetime
import requests_pkcs12
import time
import concurrent.futures

def cargar_csv():
    archivo = filedialog.askopenfilename(filetypes=[('Archivos CSV', '*.csv')])

    if archivo:
        try:
            # Leer el archivo CSV
            with open(archivo, 'r', encoding='utf-8-sig') as csv_file:
                csv_reader = csv.reader(csv_file)

                # Leer los encabezados (headers)
                headers = next(csv_reader)

                # Crear un diccionario para almacenar los valores
                datos = {re.sub(r'\W+', '', header): [] for header in headers}

                # Leer los valores y guardarlos en el diccionario
                for fila in csv_reader:
                    for i, valor in enumerate(fila):
                        datos[re.sub(r'\W+', '', headers[i])].append(valor)

                # Aquí puedes procesar o mostrar los datos como desees
                # ...

                # Guardando info en variables
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
                fecha_actual = date.today()
                dtToday = fecha_actual.strftime("%Y-%m-%d")
                storepasswords = []
                sharedsecrets = []
                responses = []
                responses_xml = []
                csv_exp = []

                # Aquí puedes utilizar los datos para el procesamiento o la carga masiva

                # Obtener el valor seleccionado del switch button
                env_value = environment.get()
                print('Entorno seleccionado:', env_value)

                # Configuraciones para test
                if env_value == 'test':
                    inicio = time.time()
                    visamid = 9900003
                    mcmid = 9900004
                    baseURL = "https://test.ipg-online.com/mcsWebService"
                    apiPassword = "tester02"
                    apiUser = "WSIPG"
                    CertPwd = 'IPGAPI'
                    p12path = r'C:\Users\FISERV\Documents\p12_masivo\test\test.p12'

                    for i in range(0, len(SID)):
                        sol_type = solution[i]
                        node_xml = ''
                        storepass = generar_texto_alfanumerico(10)
                        storepasswords.append(storepass)
                        sharedsec = ''
                        
                        reseller = 'FDMX'
                        currency = 'MXN'
                        acq = 'Dummy-3DS2'
                        limit = '250000'
                        
                        with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
                            if sol_type == 'Payment URL':
                                sharedsec = generar_texto_alfanumerico(10)
                                #creacion de soap PaymentURL
                                apireq_tpu=executor.submit(payment_url_req,
                                                baseURL, 
                                                apiUser, 
                                                apiPassword, 
                                                p12path, 
                                                CertPwd, 
                                                SID[i], 
                                                storepass, 
                                                MCC[i], 
                                                dba[i], 
                                                reseller, 
                                                currency, 
                                                dtToday, 
                                                acq, 
                                                street[i], 
                                                colony[i], 
                                                CP[i], 
                                                city[i], 
                                                state[i], 
                                                contact[i], 
                                                email[i], 
                                                phone[i], 
                                                sharedsec,
                                                mcmid,
                                                visamid,
                                                TID[i],
                                                MID[i],
                                                limit)
                                
                                resultado_tpu = apireq_tpu.result()
                                print("resultado: ",resultado_tpu)
                                responses.append(resultado_tpu)
                                responses_xml.append(resultado_tpu.text)

                            if sol_type == 'Link de Pago':
                                #Petición SOAP Link de Pago
                                apireq_tlp=executor.submit(link_pago_req,
                                            baseURL,
                                            apiUser, 
                                            apiPassword, 
                                            p12path, 
                                            CertPwd, 
                                            SID[i], 
                                            storepass, 
                                            MCC[i], 
                                            dba[i], 
                                            reseller, 
                                            currency, 
                                            dtToday, 
                                            acq, 
                                            street[i], 
                                            colony[i], 
                                            CP[i], 
                                            city[i], 
                                            state[i], 
                                            contact[i], 
                                            email[i], 
                                            phone[i], 
                                            mcmid,
                                            visamid,
                                            TID[i],
                                            MID[i],
                                            limit)
                                resultado_tlp = apireq_tlp.result()
                                print("resultado: ",resultado_tlp)
                                responses.append(resultado_tlp)
                                responses_xml.append(resultado_tlp.text)
                                
                            sharedsecrets.append(sharedsec)
                        
                    csv_exp.append(SID)
                    csv_exp.append(MID)
                    csv_exp.append(dba)
                    csv_exp.append(storepasswords)
                    csv_exp.append(sharedsecrets)
                    csv_exp.append(responses)
                    csv_exp.append(responses_xml)
                    generar_csv(csv_exp)


                # Configuraciones para prod
                if env_value == 'prod':
                    inicio = time.time()
                    baseURL = "https://www2.ipg-online.com/mcsWebService"
                    apiPassword = "z>GiE69~sh"
                    apiUser = "WST315869._.1"
                    CertPwd = 'password'
                    p12path = r'C:\Users\FISERV\Documents\p12_masivo\fdmx\fdmx.p12'

                    for i in range(0, len(SID)):
                        node_xml = ''
                        storepass = generar_texto_alfanumerico(10)
                        storepasswords.append(storepass)
                        sharedsec = ''
                        
                        with concurrent.futures.ThreadPoolExecutor(max_workers = 4) as executor:
                            if sol_type == 'Payment URL':
                                sharedsec = generar_texto_alfanumerico(10)
                                #creacion de soap PaymentURL
                                apireq_ppu=executor.submit(payment_url_req,
                                                baseURL, 
                                                apiUser, 
                                                apiPassword, 
                                                p12path, 
                                                CertPwd, 
                                                SID[i], 
                                                storepass, 
                                                MCC[i], 
                                                dba[i], 
                                                reseller, 
                                                currency, 
                                                dtToday, 
                                                acq, 
                                                street[i], 
                                                colony[i], 
                                                CP[i], 
                                                city[i], 
                                                state[i], 
                                                contact[i], 
                                                email[i], 
                                                phone[i], 
                                                sharedsec,
                                                mcmid,
                                                visamid,
                                                TID[i],
                                                MID[i],
                                                limit)
                                
                                resultado_ppu = apireq_ppu.result()
                                print("resultado: ",resultado_ppu)
                                responses.append(resultado_ppu)
                                responses_xml.append(resultado_ppu.text)

                            if sol_type == 'Link de Pago':
                                #creacion de soap Link de Pago
                                apireq_plp=executor.submit(link_pago_req,
                                            baseURL,
                                            apiUser, 
                                            apiPassword, 
                                            p12path, 
                                            CertPwd, 
                                            SID[i], 
                                            storepass, 
                                            MCC[i], 
                                            dba[i], 
                                            reseller, 
                                            currency, 
                                            dtToday, 
                                            acq, 
                                            street[i], 
                                            colony[i], 
                                            CP[i], 
                                            city[i], 
                                            state[i], 
                                            contact[i], 
                                            email[i], 
                                            phone[i], 
                                            mcmid,
                                            visamid,
                                            TID[i],
                                            MID[i],
                                            limit)
                                resultado_plp = apireq_plp.result()
                                print("resultado: ",resultado_plp)
                                responses.append(resultado_plp)
                                responses_xml.append(resultado_plp.text)
                                
                            sharedsecrets.append(sharedsec)
                        
                    csv_exp.append(SID)
                    csv_exp.append(MID)
                    csv_exp.append(dba)
                    csv_exp



                opciones = ['test', 'prod']
                with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
                    resultados = list(executor.map(cargar_csv))

                # Actualizar el cuadro de respuesta
                tiempo_total = time.time() - inicio
                print("resultados", resultados)
                print("responses: ", responses)
                print(f"Tiempo total de ejecución: {tiempo_total:.4f} segundos")
                respuesta.config(text="Archivo cargado exitosamente. \n CSV generado en downloads del proyecto", fg="green")
        except Exception as e:
            # Actualizar el cuadro de respuesta en caso de error
            respuesta.config(text="Error al cargar el archivo", fg="red")
            print(str(e))

def payment_url_req(baseURL,  
                    apiUser, 
                    apiPassword, 
                    p12path, 
                    CertPwd, 
                    SID, 
                    storepass, 
                    MCC, 
                    dba, 
                    reseller, 
                    currency, 
                    dtToday, 
                    acq, 
                    street, 
                    colony, 
                    CP, 
                    city, 
                    state, 
                    contact, 
                    email, 
                    phone, 
                    sharedsec,
                    mcmid,
                    visamid,
                    TID,
                    MID,
                    limit):
    #creacion de soap PaymentURL
    soap_xml = f'''
    <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Header />
        <SOAP-ENV:Body>
        </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    '''
    
    #Petición SOAP PaymentURL
    resp = post_request_with_pfx(baseURL, soap_xml, apiUser, apiPassword, p12path, CertPwd)
    return resp

def link_pago_req(baseURL, 
                    soap_xml, 
                    apiUser, 
                    apiPassword, 
                    p12path, 
                    CertPwd, 
                    SID, 
                    storepass, 
                    MCC, 
                    dba, 
                    reseller, 
                    currency, 
                    dtToday, 
                    acq, 
                    street, 
                    colony, 
                    CP, 
                    city, 
                    state, 
                    contact, 
                    email, 
                    phone, 
                    mcmid,
                    visamid,
                    TID,
                    MID,
                    limit):
    soap_xml = f'''
    <SOAP-ENV:Envelope2 xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
        <SOAP-ENV:Body2>
        </SOAP-ENV:Body2>
    </SOAP-ENV:Envelope2>
    '''
    #Petición SOAP Link de Pago
    resp = post_request_with_pfx(baseURL, soap_xml, apiUser, apiPassword, p12path, CertPwd)
    return resp

def generar_texto_alfanumerico(longitud):
    caracteres = string.ascii_letters + string.digits + '!@#$%^*()_+-=[]{}|;:,./?'
    caracteres = caracteres.replace('<', '').replace('>', '').replace('&','')
    primer_caracter = random.choice(string.ascii_letters + string.digits + '!@#$%^*()_+-=[]{}|;:,./?')
    texto = primer_caracter + ''.join(random.choice(caracteres) for _ in range(longitud - 1))
    return texto

def post_request_with_pfx(url, xml_body, username, password, pfx_file_path, pfx_password):
    """
    Realiza una solicitud POST a una URL usando autenticación y certificado.

    Args:
        url (str): La URL del endpoint.
        xml_body (str): El contenido XML del body de la solicitud.
        username (str): El nombre de usuario para la autenticación.
        password (str): La contraseña para la autenticación.
        pfx_file_path (str): Ruta al archivo del certificado (.p12).
        pfx_password (str): Contraseña del certificado.

    Returns:
        requests.Response: El objeto de respuesta de la solicitud.
    """

    headers = {
        "Content-Type": "text/xml",
        "SOAPAction": ""
    }

    response = requests_pkcs12.post(
        url, 
        headers=headers, 
        data=xml_body, 
        auth=(username, password), 
        pkcs12_filename=pfx_file_path,
        pkcs12_password=pfx_password,
        verify=True  # A veces es necesario deshabilitar la verificación, pero no es lo más seguro
    )

    return response
    
def generar_csv(matriz):
    encabezados = ['SID', 'MID', 'DBA', 'Password','SharedSecret','Responses','XML_response']
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Nombre del archivo con la fecha y hora actual
    nombre_archivo = f'respuestas_url_{fecha_hora_actual}.csv'

    # Comprobar si la carpeta "downloads" existe, de lo contrario, crearla
    if not os.path.exists('downloads'):
        os.makedirs('downloads')

    # Ruta del archivo CSV
    ruta_archivo = os.path.join('downloads', nombre_archivo)

    # Transponer la matriz para cambiar las filas por columnas
    matriz_transpuesta = list(map(list, zip(*matriz)))

    # Escribir los datos en el archivo CSV
    with open(ruta_archivo, 'w', newline='') as archivo:
        writer = csv.writer(archivo)

        # Escribir los encabezados
        writer.writerow(encabezados)

        # Escribir los datos de la matriz transpuesta
        writer.writerows(matriz_transpuesta)

    print(f'Archivo CSV generado: {ruta_archivo}')


ventana = tk.Tk()
ventana.title("Cargas Masivas")
ventana.configure(bg="#F5F5F5")

# Estilo de fuente personalizado
estilo_fuente = ("Arial", 14)

# Encabezado
encabezado = tk.Label(
    ventana,
    text="Carga Masiva",
    font=estilo_fuente,
    bg="#F5F5F5",
    fg="#333333"
)
encabezado.pack(pady=20)

# Cuadro de respuesta
respuesta = tk.Label(
    ventana,
    text="",
    font=estilo_fuente,
    bg="#F5F5F5"
)
respuesta.pack(pady=10)

# Frame para el switch button
frame_switch = tk.Frame(ventana, bg="#F5F5F5")
frame_switch.pack(pady=10)

# Variable para almacenar el valor seleccionado del switch button
environment = tk.StringVar()

# Etiqueta para el switch button
switch_label = tk.Label(frame_switch, text="Entorno:", font=estilo_fuente, bg="#F5F5F5")
switch_label.pack(side=tk.LEFT)

# Switch button - Opción Test
switch_button_test = ttk.Radiobutton(frame_switch, text="Test", variable=environment, value="test", style="Switch.TRadiobutton")
switch_button_test.pack(side=tk.LEFT)

# Switch button - Opción Prod
switch_button_prod = ttk.Radiobutton(frame_switch, text="Prod", variable=environment, value="prod", style="Switch.TRadiobutton")
switch_button_prod.pack(side=tk.LEFT)

# Estilo para el switch button
style = ttk.Style()
style.configure("Switch.TRadiobutton", background="#F5F5F5", font=estilo_fuente)

# Botón de carga
btn_cargar = tk.Button(
    ventana,
    text="Cargar CSV",
    command=cargar_csv,
    font=estilo_fuente,
    bg="orange",
    fg="white",
    relief=tk.FLAT
)
btn_cargar.pack(pady=10)

# Ajustar tamaño de la ventana
ventana.geometry("400x350")

# Ejecutar la aplicación
ventana.mainloop()
