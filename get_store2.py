import requests_pkcs12
import time
import concurrent.futures
import xml.etree.ElementTree as ET
import os
import csv
from datetime import date
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk 
from interface import body_req

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

# Resto del código

matriz = [6206115,6206114,6206113]

username = os.getlogin()
csv_exp=[]
sid=[]
mid=[]
dba=[]
tid=[]
tnode=[]
env=""
#prosa=[]

#FDMX
# baseURL = "https://www2.ipg-online.com/mcsWebService"
# apiPassword = "z>GiE69~sh"
# apiUser = "WST315869._.1"
# CertPwd = 'password'
# p12path = fr'C:\Users\FISERV\Documents\p12_masivo\\prod\fdmx.p12'

#FGB
# baseURL = "https://www2.ipg-online.com/mcsWebService"
# apiPassword = "b\\v=d9A7eg"
# apiUser = "WST313086._.1"
# CertPwd = 'Welcome@123'
# p12path = fr'C:\Users\FISERV\Documents\p12_masivo\\fgb\WST313086.p12'


#TEST
# baseURL = "https://test.ipg-online.com/mcsWebService"
# apiPassword = "tester02"
# apiUser = "WSIPG"
# CertPwd = 'IPGAPI'
# p12path = fr'C:\Users\{username}\Documents\p12_masivo\test\test.p12'


inicio = time.time()

def generar_csv(matriz,username):
    encabezados = ['SID', 'MID','TID','DBA','NODE']
    # Obtener la fecha y hora actual
    fecha_hora_actual = datetime.now().strftime('%Y%m%d_%H%M%S')

    # Nombre del archivo con la fecha y hora actual
    nombre_archivo = f'respuestas_url_{fecha_hora_actual}.csv'

    # Obtener el nombre de usuario actual de Windows
    username = os.getlogin()

    # Construir la ruta completa del directorio de descargas
    ruta_descargas = fr'C:\Users\{username}\Downloads'

    # Comprobar si la carpeta de descargas existe, de lo contrario, crearla
    if not os.path.exists(ruta_descargas):
        os.makedirs(ruta_descargas)

    # Ruta completa del archivo CSV
    ruta_archivo = os.path.join(ruta_descargas, nombre_archivo)

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


#def process_request(i, baseURL, apiUser, apiPassword, p12path, CertPwd):
def process_request(i,env):
    print('env: ',env)
    
    if env == '1':
        baseURL = "https://test.ipg-online.com/mcsWebService"
        apiPassword = "tester02"
        apiUser = "WSIPG"
        CertPwd = 'IPGAPI'
        p12path = fr'C:\Users\{username}\Documents\p12_masivo\test\test.p12'
        
    if env == '2':
        baseURL = "https://www2.ipg-online.com/mcsWebService"
        apiPassword = "z>GiE69~sh"
        apiUser = "WST315869._.1"
        CertPwd = 'password'
        p12path = fr'C:\Users\{username}\Documents\p12_masivo\\fdmx\\fdmx.p12'
        
    if env == '3':
        baseURL = "https://www2.ipg-online.com/mcsWebService"
        apiPassword = "b\\v=d9A7eg"
        apiUser = "WST313086._.1"
        CertPwd = 'Welcome@123'
        p12path = fr'C:\Users\{username}\Documents\p12_masivo\\fgb\WST313086.p12'

    soap_xml = f'''   
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mcs="http://www.ipg-online.com/mcsWebService">
        <soapenv:Header/>
        <soapenv:Body>
            <mcs:mcsRequest>
                <mcs:getStore>
                    <mcs:storeID>{i}</mcs:storeID>
                </mcs:getStore>
            </mcs:mcsRequest>
        </soapenv:Body>
    </soapenv:Envelope>
    '''
    resp = post_request_with_pfx(baseURL, soap_xml, apiUser, apiPassword, p12path, CertPwd)
    return i, resp
    
# Función para procesar la solicitud con la matriz ingresada
def procesar_matriz():
    # Actualizar la variable body_req con el valor seleccionado
    #body_req.set(modo_var.get())
    valores_matriz = entrada_matriz.get()
    print("body_req: ", body_req.get())
    
    if body_req.get()=='test':
        env = '1'
        
    if body_req.get()=='fdmx':
        env = '2'
        
    if body_req.get()=='fgb':
        env = '3'
        
    #print('baseURL',baseURL)
    try:
        matriz = [int(valor.strip()) for valor in valores_matriz.split(',')]
        if not matriz:
            raise ValueError
        for valor in matriz:
            if not isinstance(valor, int):
                raise ValueError

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_request, matriz,env))
            #results = list(executor.map(process_request, matriz, baseURL, apiUser, apiPassword, p12path, CertPwd))

        csv_exp = []
        sid = []
        mid = []
        dba = []
        tid = []
        tnode = []
        #print('results: ',results)
        for i, resp in results:
            print('resp: ',resp.text)
            root = ET.fromstring(resp.text)
            external_merchant_id_element = root.find(".//ns2:externalMerchantID", namespaces={"ns2": "http://www.ipg-online.com/mcsWebService"})
            dba_xml = root.find(".//ns2:dba", namespaces={"ns2": "http://www.ipg-online.com/mcsWebService"})
            tid_xml = root.find(".//ns2:terminalID", namespaces={"ns2": "http://www.ipg-online.com/mcsWebService"})
            tnode_xml = root.find(".//ns2:id", namespaces={"ns2": "http://www.ipg-online.com/mcsWebService"})

            if external_merchant_id_element is not None:
                external_merchant_id = external_merchant_id_element.text
                print("SID:", i, "MID:", external_merchant_id, 'TID:', tid_xml.text, "DBA:", dba_xml.text)
                sid.append(i)
                mid.append(external_merchant_id)
                tid.append(tid_xml.text)
                dba.append(dba_xml.text)
                tnode.append(resp.text)
            else:
                print("No se encontró el elemento externalMerchantID en el XML.")
                sid.append(i)
                mid.append("NO MID")
                tid.append("NO TID")
                dba.append("NO DBA")
                tnode.append("NO NODO")

        csv_exp.append(sid)
        csv_exp.append(mid)
        csv_exp.append(tid)
        csv_exp.append(dba)
        csv_exp.append(tnode)
        generar_csv(csv_exp, username)

        tiempo_total = time.time() - inicio
        print(f"Tiempo total de ejecución: {tiempo_total:.4f} segundos")
    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos separados por comas (por ejemplo, 6206115,6206114,6206113).")

# Crear la ventana Tkinter con un tamaño personalizado
ventana = tk.Tk()
ventana.title("Programa con Interfaz")
ventana.geometry("400x300")  # Ancho x Alto

# Variable para el modo (test, fdmx, fgb)
body_req = tk.StringVar()
body_req.set("test")  # Valor inicial en "test"

# Etiqueta y campo de entrada para la matriz con tamaño de fuente grande
etiqueta_matriz = tk.Label(ventana, text="Valores de los SID:", font=("Arial", 16))
etiqueta_matriz.pack(pady=10)
entrada_matriz = tk.Entry(ventana, font=("Arial", 14), width=40)
entrada_matriz.pack(pady=10)

# Crear el dropdown menu para seleccionar el modo
modo_label = tk.Label(ventana, text="Selecciona el modo:", font=("Arial", 16))
modo_label.pack(pady=10)

modos = ["test", "fdmx", "fgb"]

def seleccionar_modo(event):
    body_req.set(modo_dropdown.get())

modo_dropdown = ttk.Combobox(ventana, values=modos, textvariable=body_req, font=("Arial", 14))
modo_dropdown.set("test")
modo_dropdown.pack(pady=10)
modo_dropdown.bind("<<ComboboxSelected>>", seleccionar_modo)

# Botón para ejecutar el programa con tamaño de fuente grande
boton_ejecutar = tk.Button(ventana, text="Ejecutar", command=procesar_matriz, font=("Arial", 16))
boton_ejecutar.pack(pady=10)

# Iniciar el bucle principal de Tkinter
ventana.mainloop()