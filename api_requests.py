from suds.client import Client
from suds.transport.http import HttpAuthenticated
from base64 import b64encode

def make_soap_request(url, p12_file_path, p12_password, username, password, soap_operation, soap_body):
    # Load P12 certificate
    with open(p12_file_path, 'rb') as p12_file:
        p12_data = p12_file.read()

    # Create a SOAP client using suds
    client = Client(url, transport=HttpAuthenticated())

    # Set P12 certificate in HTTP headers
    connection = client.options.transport.open()
    connection.sock = client.options.transport.sock
    connection.send(f"PKCS12 {b64encode(p12_data).decode()}\n".encode())
    connection.send(p12_password.encode())
    connection.send('\n'.encode())

    # Set basic authorization credentials
    auth_token = b64encode(f"{username}:{password}".encode()).decode("ascii")

    # Set authorization header
    headers = {"Authorization": f"Basic {auth_token}"}
    client.options.transport.set_options(headers=headers)

    # Call the SOAP operation
    response = getattr(client.service, soap_operation)(soap_body)

    return response


# Ejemplo de uso:
url2 = 'http://www.otravuelta.cl/soap/index.php?wsdl'
url = 'https://test.ipg-online.com/'
p12_file_path = r'C:\Users\FISERV\Documents\p12_masivo\test\test.p12'
p12_password = 'IPGAPI'
username = 'WSIPG'
password = 'tester02'
soap_operation = 'mcsWebService'
soap_body = '''
<SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
                               <SOAP-ENV:Header />
                               <SOAP-ENV:Body>
                                  <ns2:mcsRequest xmlns:ns2="http://www.ipg-online.com/mcsWebService">
                                     <ns2:createStore>
                                         <ns2:merchant>
                                             <ns2:merchantID>832207603</ns2:merchantID>
                                             <ns2:merchantAdmin>
                                                 <ns2:id>T832207603</ns2:id>
                                             </ns2:merchantAdmin>
                                         </ns2:merchant>
                                         <ns2:store>
                                             <ns2:storeID>62998899</ns2:storeID>
                                             <ns2:storeAdmin>
                                                 <ns2:id>62998899</ns2:id>
                                                 <ns2:password>WEbd+!1F</ns2:password>
                                             </ns2:storeAdmin>
                                             <ns2:mcc>1234</ns2:mcc>
                                                <ns2:legalName>GRUPO ALTERNATIVA</ns2:legalName>
                                                <ns2:dba>GRUPO ALTERNATIVA</ns2:dba>
                                                <ns2:reseller>FDMX</ns2:reseller>
                                                <ns2:url>https://www.fiserv.com/es-mx.html</ns2:url>
                                             <ns2:defaultCurrency>MXN</ns2:defaultCurrency>
                                             <ns2:timezone>America/Mexico_City</ns2:timezone>
                                             <ns2:status>OPEN</ns2:status>
                                             <ns2:openDate>2023-08-08</ns2:openDate>
                                             <ns2:acquirer>FDMX-MXN</ns2:acquirer>
                                             <ns2:address>
                                                 <ns2:address1>CALLE ZANDUNGA 37</ns2:address1>
                                                 <ns2:address2>CDA DE PUEBLO NUEVO</ns2:address2>
                                                 <ns2:zip>50337</ns2:zip>
                                                 <ns2:city>ALVARO OBREGO</ns2:city>
                                                 <ns2:state>MEX</ns2:state>
                                                 <ns2:country>MEX</ns2:country>
                                             </ns2:address>
                                             <ns2:contact>
                                                 <ns2:name>MEJIA OROPEZA FANNY ILENIA</ns2:name>
                                                 <ns2:email>ilenia-moropeza@hotmail.com</ns2:email>
                                                 <ns2:phone>5521555733</ns2:phone>
                                             </ns2:contact>
                                             <ns2:service>
                                                 <ns2:type>api</ns2:type>
                                             </ns2:service>
                                             <ns2:service>
                                                 <ns2:type>creditCard</ns2:type>
                                                 <ns2:config>
                                                     <ns2:item>allowECI7_EPAS</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowECI7_API</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>accountUpdaterVisa</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>AVS</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>IPaddressInAuthRequest</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>exceedPreauthAllowedInPercent</ns2:item>
                                                     <ns2:value>0</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>Visa</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowECI7_VT</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>Amex</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowCredits</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>cardCodeMandatory</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>CUP</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>Diners</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowPurchaseCards</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>JCB</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>Mastercard</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>mexicoLocal</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowOnlineAuthForRefund</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowECI7_Connect</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                             </ns2:service>
                                             <ns2:service>
                                                 <ns2:type>hostedData</ns2:type>
                                                 <ns2:config>
                                                     <ns2:item>flagRecurring</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                             </ns2:service>
                                             <ns2:service>
                                                 <ns2:type>3dSecure</ns2:type>
                                                 <ns2:config>
                                                     <ns2:item>declineSameXIDandECI</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>dinersMID</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>jcbMID</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>maestroMID</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowSplitAuthentication</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>integration</ns2:item>
                                                     <ns2:value>Modirum3DSServer</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>excludedCardCountries</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>transactionRiskAnalysis</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowECI1andECI6</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>visaPassword</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowECI7onIVRPAResUifInternational</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowSoftDeclineRetry_Connect</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>visaMID</ns2:item>
                                                     <ns2:value>9140592</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>amexMID</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>mastercardMID</ns2:item>
                                                     <ns2:value>9140592</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>vmid</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowed3dsServerVersionMax</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>iciciOnUsVereq</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>mc3DS2DataOnly</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>TRAGhostCall</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowAuthenticationRetry</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>acquirerName</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowMPIViaAPI</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowMPIViaRESTAPI</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>amex3DSRequestorId</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>declineSameAAV</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>jcbPassword</ns2:item>
                                                     <ns2:value xsi:nil="true" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"/>
                                                 </ns2:config>
                                             </ns2:service>
                                             <ns2:terminal>
                                                 <ns2:terminalID>4478999</ns2:terminalID>
                                                 <ns2:externalMerchantID>84315600999</ns2:externalMerchantID>
                                                 <ns2:endpointID>NASHVILLE MEXICO</ns2:endpointID>
                                                 <ns2:paymentMethod>MEXICOLOCAL</ns2:paymentMethod>
                                                 <ns2:paymentMethod>MASTERCARD</ns2:paymentMethod>
                                                 <ns2:paymentMethod>VISA</ns2:paymentMethod>
                                                 <ns2:transactionOrigin>ECI</ns2:transactionOrigin>
                                                 <ns2:submissionComponent>API</ns2:submissionComponent>
                                                 <ns2:payerSecurityLevel>EMPTY</ns2:payerSecurityLevel>
                                                 <ns2:payerSecurityLevel>NOT EMPTY</ns2:payerSecurityLevel>
                                                 <ns2:currency>MXN</ns2:currency>
                                                 <ns2:active>true</ns2:active>
                                             </ns2:terminal>
                                             <ns2:purchaseLimit>
                                                 <ns2:currency>MXN</ns2:currency>
                                                 <ns2:limit>250000</ns2:limit>
                                             </ns2:purchaseLimit>
                                             <ns2:fraudSettings>
                                                 <ns2:binBlockProfile>99</ns2:binBlockProfile>
                                                 <ns2:checkBlockedIP>true</ns2:checkBlockedIP>
                                                 <ns2:checkBlockedClass-C>true</ns2:checkBlockedClass-C>
                                                 <ns2:checkBlockedName>true</ns2:checkBlockedName>
                                                 <ns2:checkBlockedCard>true</ns2:checkBlockedCard>
                                                 <ns2:duplicateLockoutTimeSeconds>0</ns2:duplicateLockoutTimeSeconds>
                                                 <ns2:autoLockoutTimeSeconds>0</ns2:autoLockoutTimeSeconds>
                                             </ns2:fraudSettings>
                                         </ns2:store>
                                     </ns2:createStore>
                                  </ns2:mcsRequest>
                               </SOAP-ENV:Body>
                            </SOAP-ENV:Envelope>
                            '''
response = make_soap_request(url, p12_file_path, p12_password, username, password, soap_operation, soap_body)
print(response)
