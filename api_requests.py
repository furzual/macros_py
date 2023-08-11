import requests_pkcs12

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

# Variables de prueba
url = 'https://test.ipg-online.com/mcsWebService'
body = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:mcs="http://www.ipg-online.com/mcsWebService">
   <soapenv:Header/>
   <soapenv:Body>
      <mcs:mcsRequest>
         <mcs:getStore>
            <mcs:storeID>230995000</mcs:storeID>
         </mcs:getStore>
      </mcs:mcsRequest>
   </soapenv:Body>
</soapenv:Envelope>'''
username = 'WSIPG'
password = 'tester02'
pfx_file_path = r'C:\Users\FISERV\Documents\p12_masivo\test\test.p12'  # La ruta correcta de tu archivo .p12

# Llamar a la función y obtener la respuesta
response = post_request_with_pfx(url, body, username, password, pfx_file_path, 'IPGAPI')

# Imprimir la respuesta
print(response.text)
