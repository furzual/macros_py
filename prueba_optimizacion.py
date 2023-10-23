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

matriz = [62997899, 62997898]  # Puedes agregar más valores a la matriz
baseURL = "https://test.ipg-online.com/mcsWebService"
apiPassword = "tester02"
apiUser = "WSIPG"
CertPwd = 'IPGAPI'
p12path = r'C:\Users\FISERV\Documents\p12_masivo\test\test.p12'

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

with concurrent.futures.ThreadPoolExecutor() as executor:
    results = list(executor.map(process_request, matriz))

for i, resp in results:
    print("SID:", i, "  response:", resp, "   response xml:", resp.text)

tiempo_total = time.time() - inicio
print(f"Tiempo total de ejecución: {tiempo_total:.4f} segundos")
