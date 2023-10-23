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
url = 'https://test.ipg-online.com/ipgapi/services'
body = '''<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:ipg="http://ipg-online.com/ipgapi/schemas/ipgapi" xmlns:v1="http://ipg-online.com/ipgapi/schemas/v1">
    <soapenv:Header/>
    <soapenv:Body>
        <ipg:IPGApiOrderRequest>
            <v1:Transaction>
                <v1:CreditCardTxType>
                    <v1:StoreId>8118990003</v1:StoreId>
                    <v1:Type>sale</v1:Type>
                </v1:CreditCardTxType>
                <v1:CreditCardData>
                    <v1:CardNumber>4111111111111111</v1:CardNumber>
                    <v1:ExpMonth>12</v1:ExpMonth>
                    <v1:ExpYear>25</v1:ExpYear>
                    <v1:CardCodeValue>123</v1:CardCodeValue>
                </v1:CreditCardData>
                <v1:Payment>
                    <v1:ChargeTotal>45.00</v1:ChargeTotal>
                    <v1:Currency>780</v1:Currency>
                </v1:Payment>
            </v1:Transaction>
        </ipg:IPGApiOrderRequest>
    </soapenv:Body>
</soapenv:Envelope>'''
username = 'WST41583819440._.1'
password = 'h.9egG5<kv'
pfx_file_path = r'C:\Users\FISERV\Downloads\WST41583819440._.1.p12'  # La ruta correcta de tu archivo .p12

# Llamar a la función y obtener la respuesta
response = post_request_with_pfx(url, body, username, password, pfx_file_path, 'UXxK>-59xA')

# Imprimir la respuesta
print(response)
print(response.text)
