import tkinter as tk
from tkinter import messagebox
import requests_pkcs12
import time
import concurrent.futures

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

# baseURL = "https://test.ipg-online.com/mcsWebService"
# apiPassword = "tester02"
# apiUser = "WSIPG"
# CertPwd = 'IPGAPI'
# p12path = r'C:\Users\FISERV\Documents\p12_masivo\test\test.p12'

baseURL = "https://www2.ipg-online.com/mcsWebService"
apiPassword = "z>GiE69~sh"
apiUser = "WST315869._.1"
CertPwd = 'password'
p12path = r'.\p12\prod\fdmx.p12'

inicio = time.time()

def process_request(i):
    soap_xml = f'''
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mcs="http://www.ipg-online.com/mcsWebService">
       <soapenv:Header/>
       <soapenv:Body>
          <mcs:mcsRequest>
             <mcs:deleteStore>
                <mcs:storeID>{i}</mcs:storeID>
             </mcs:deleteStore>
          </mcs:mcsRequest>
       </soapenv:Body>
    </soapenv:Envelope>
    '''
    resp = post_request_with_pfx(baseURL, soap_xml, apiUser, apiPassword, p12path, CertPwd)
    return i, resp

def execute_code():
    # Obtener los valores de la matriz desde el cuadro de entrada
    matriz_input = matriz_entry.get()
    matriz = [int(val) for val in matriz_input.split(',')]
    
    # Ejecutar el código con los valores de matriz ingresados
    inicio = time.time()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = list(executor.map(process_request, matriz))
    
    for i, resp in results:
        result_text.insert(tk.END, f"SID: {i}  response: {resp}   response xml: {resp.text}\n")
    
    tiempo_total = time.time() - inicio
    result_text.insert(tk.END, f"Tiempo total de ejecución: {tiempo_total:.4f} segundos\n")

# Crear la ventana principal
window = tk.Tk()
window.title("Ejecución de Código")

# Crear y posicionar elementos en la ventana
matriz_label = tk.Label(window, text="Valores de SID (separados por comas):")
matriz_label.pack()

matriz_entry = tk.Entry(window)
matriz_entry.pack()

execute_button = tk.Button(window, text="Ejecutar Código", command=execute_code)
execute_button.pack()

result_text = tk.Text(window, height=10, width=50)
result_text.pack()

# Iniciar la aplicación
window.mainloop()
