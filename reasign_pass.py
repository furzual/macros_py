import time
import concurrent.futures
import xml.etree.ElementTree as ET
import os
import csv
from datetime import date
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import random
import string
import requests_pkcs12
import time

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
password=[]
#prosa=[]
baseURL = "https://www2.ipg-online.com/mcsWebService"
apiPassword = "z>GiE69~sh"
apiUser = "WST315869._.1"
CertPwd = 'password'
p12path = fr'C:\Users\FISERV\Documents\p12_masivo\fdmx\fdmx.p12'

# baseURL = "https://test.ipg-online.com/mcsWebService"
# apiPassword = "tester02"
# apiUser = "WSIPG"
# CertPwd = 'IPGAPI'
# p12path = fr'C:\Users\{username}\Documents\p12_masivo\test\test.p12'


inicio = time.time()

def generar_csv(matriz,username):
    encabezados = ['SID', 'MID','TID','DBA']
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


def process_request(i):
    
    store_pass=generar_texto_alfanumerico(12)
    print("store_pass: ",store_pass)
    soap_xml = f'''   
      <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mcs="http://www.ipg-online.com/mcsWebService">
         <soapenv:Header/>
         <soapenv:Body>
            <mcs:mcsRequest>
               <mcs:resetStoreAdminUserPassword>
                  <mcs:storeID>{i}</mcs:storeID>
                  <mcs:storeAdmin>
                     <mcs:id>{i}</mcs:id>
                     <mcs:password>{store_pass}</mcs:password>
                  </mcs:storeAdmin>
               </mcs:resetStoreAdminUserPassword>
            </mcs:mcsRequest>
         </soapenv:Body>
      </soapenv:Envelope>
    '''
    resp = post_request_with_pfx(baseURL, soap_xml, apiUser, apiPassword, p12path, CertPwd)
    print('Respuesta', resp.text)
    return i, resp, store_pass

def generar_texto_alfanumerico(longitud):
    caracteres = string.ascii_letters + string.digits + '!@#$%^*()_+-=[]{}|;:,./?'
    caracteres = caracteres.replace('<', '').replace('>', '').replace('&','')
    primer_caracter = random.choice(string.ascii_letters + string.digits + '!@#$%^*()_+-=[]{}|;:,./?')
    texto = primer_caracter + ''.join(random.choice(caracteres) for _ in range(longitud - 1))
    return texto
 
# Función para procesar la solicitud con la matriz ingresada
def procesar_matriz():
    valores_matriz = entrada_matriz.get()
    try:
        matriz = [int(valor.strip()) for valor in valores_matriz.split(',')]
        if not matriz:
            raise ValueError
        for valor in matriz:
            if not isinstance(valor, int):
                raise ValueError

        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = list(executor.map(process_request, matriz))

        csv_exp = []
        sid = []
        mid = []
        dba = []
        tid = []

        for i, resp in results:
            root = ET.fromstring(resp.text)
            external_merchant_id_element = root.find(".//ns2:externalMerchantID", namespaces={"ns2": "http://www.ipg-online.com/mcsWebService"})
            dba_xml = root.find(".//ns2:dba", namespaces={"ns2": "http://www.ipg-online.com/mcsWebService"})
            tid_xml = root.find(".//ns2:terminalID", namespaces={"ns2": "http://www.ipg-online.com/mcsWebService"})

            if external_merchant_id_element is not None:
                external_merchant_id = external_merchant_id_element.text
                print("SID:", i, "MID:", external_merchant_id, 'TID:', tid_xml.text, "DBA:", dba_xml.text)
                password.append(store_pass)
                sid.append(i)
                mid.append(external_merchant_id)
                tid.append(tid_xml.text)
                dba.append(dba_xml.text)
            else:
                print("No se encontró el elemento externalMerchantID en el XML.")
                password.append("NO PASS")
                sid.append(i)
                mid.append("NO MID")
                tid.append("NO TID")
                dba.append("NO DBA")

        csv_exp.append(sid)
        csv_exp.append(mid)
        csv_exp.append(tid)
        csv_exp.append(dba)
        generar_csv(csv_exp, username)

        tiempo_total = time.time() - inicio
        print(f"Tiempo total de ejecución: {tiempo_total:.4f} segundos")
    except ValueError:
        messagebox.showerror("Error", "Ingresa valores válidos separados por comas (por ejemplo, 6206115,6206114,6206113).")


# Crear la ventana Tkinter con un tamaño personalizado
ventana = tk.Tk()
ventana.title("Programa con Interfaz")
ventana.geometry("400x200")  # Ancho x Alto

# Etiqueta y campo de entrada para la matriz con tamaño de fuente grande
etiqueta_matriz = tk.Label(ventana, text="Valores de los SID:", font=("Arial", 16))
etiqueta_matriz.pack(pady=10)
entrada_matriz = tk.Entry(ventana, font=("Arial", 14), width=40)
entrada_matriz.pack(pady=10)

# Botón para ejecutar el programa con tamaño de fuente grande
boton_ejecutar = tk.Button(ventana, text="Ejecutar", command=procesar_matriz, font=("Arial", 16))
boton_ejecutar.pack(pady=10)

# Iniciar el bucle principal de Tkinter
ventana.mainloop()
