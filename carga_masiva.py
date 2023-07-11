import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import csv
import re
import json
import random
import string
from datetime import date
import io
from concurrent.futures import ThreadPoolExecutor, as_completed

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
                storepasswords=[]
                csv_exp=[]

                # Aquí puedes utilizar los datos para el procesamiento o la carga masiva

                # Obtener el valor seleccionado del switch button
                env_value = environment.get()
                print('Entorno seleccionado:', env_value)

                #Configuracion para test
                if env_value == 'test':
                    visamid = 9900003
                    mcmid = 9900004
                    baseURL = "https://test.ipg-online.com/mcsWebService"
                    apiPassword = "tester02"
                    apiUser = "WSIPG"
                    certificateName = "WSIPG"
                    CertPwd = 'password'

                    for i in range (0,len(SID)):
                        storepass = generar_texto_alfanumerico(8)
                        print('visamid:', visamid)
                        print('mcmid:', mcmid)
                        print('storepass:', storepass)

                #Configuracion para produccion
                if env_value == 'prod':

                    baseURL = "https://test.ipg-online.com/mcsWebService"
                    apiPassword = "tester02"
                    apiUser = "WSIPG"
                    certificateName = "WSIPG"
                    CertPwd = 'password'

##                    baseURL = "https://www2.ipg-online.com/mcsWebService"
##                    apiPassword = "z>GiE69~sh"
##                    apiUser = "WST315869._.1"
##                    certificateName = "WST315869._.1"
##                    CertPwd = 'password'

                    for i in range (0,len(SID)):
                        node_xml = ''
                        storepass = generar_texto_alfanumerico(8)
                        storepasswords.append(storepass)
                        # Lista para almacenar los resultados de las solicitudes
                        resultados = []

                        #print('storepass:', storepass)
                        #Configuracion para pesos
                        if prosa[i] != '':   
                            visamid = prosa[i]
                            mcmid = prosa[i]
                            reseller = 'FDMX'
                            currency = 'MXN'
                            acq = 'FDMX-MXN'
                            limit = '250000'

                        #Configuracion para dolares
                        if prosa[i] == '':
                            visamid = MID[i]
                            mcmid = MID[i]
                            reseller = 'FDMX'
                            currency = 'USD'
                            acq = 'FDMX-USD'
                            limit = '10000'

                        sol_type = solution[i]

                        if sol_type == 'Payment URL':
                            #creacion de soap PaymentURL
                            soap_xml = f'''
                            <SOAP-ENV:Envelope xmlns:SOAP-ENV=""http://schemas.xmlsoap.org/soap/envelope/"">
                               <SOAP-ENV:Header />
                               <SOAP-ENV:Body>
                                  <ns2:mcsRequest xmlns:ns2=""http://www.ipg-online.com/mcsWebService"">
                                     <ns2:createStore>
                                        <ns2:store>
                                                <ns2:storeID>{SID[i]}</ns2:storeID>
                                                <ns2:storeAdmin>
                                                    <ns2:id>{SID[i]}</ns2:id>
                                                    <ns2:password>{storepass}</ns2:password>
                                                </ns2:storeAdmin>
                                                <ns2:mcc>{MCC[i]}</ns2:mcc>
                                                <ns2:legalName>{dba[i]}</ns2:legalName>
                                                <ns2:dba>{dba[i]}</ns2:dba>
                                                <ns2:reseller>{reseller}</ns2:reseller>
                                                <ns2:url>https://www.fiserv.com/es-mx.html</ns2:url>
                                                <ns2:defaultCurrency>{currency}</ns2:defaultCurrency>
                                                <ns2:timezone>America/Mexico_City</ns2:timezone>
                                                <ns2:status>OPEN</ns2:status>
                                                <ns2:openDate>{dtToday}</ns2:openDate>
                                                <ns2:acquirer>{acq}</ns2:acquirer>
                                                <ns2:address>
                                                    <ns2:address1>{street[i]}</ns2:address1>
                                                    <ns2:zip>{CP[i]}</ns2:zip>
                                                    <ns2:city>{city[i]}</ns2:city>
                                                    <ns2:state>{state[i]}</ns2:state>
                                                    <ns2:country>MEX</ns2:country>
                                                </ns2:address>
                                                <ns2:contact>
                                                    <ns2:name>{contact[i]}</ns2:name>
                                                    <ns2:email>{email[i]}</ns2:email>
                                                    <ns2:phone>{phone[i]}</ns2:phone>
                                                </ns2:contact>
                                                <ns2:service>
                                                    <ns2:type>connect</ns2:type>
                                                    <ns2:config>
                                                        <ns2:item>overwriteURLsAllowed</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>reviewURL</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>transactionNotificationURL</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowVoid</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>responseSuccessURL</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>responseFailureURL</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>checkoutOptionCombinedPage</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>skipResultPageForFailure</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowMaestroWithout3DS</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowMOTO</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowExtendedHashCalculationWithoutCardDetails</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>cardCodeBehaviour</ns2:item>
                                                        <ns2:value>mandatory</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>hideCardBrandLogoInCombinedPage</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>skipResultPageForSuccess</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>sharedSecret</ns2:item>
                                                        <ns2:value>sharedSecret</ns2:value>
                                                    </ns2:config>
                                                </ns2:service>
                                                <ns2:service>
                                                    <ns2:type>creditCard</ns2:type>
                                                    <ns2:config>
                                                        <ns2:item>Mastercard</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>JCB</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>cardCodeMandatory</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowECI7_EPAS</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowECI7_API</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>IPaddressInAuthRequest</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>Diners</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>accountUpdaterVisa</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>Amex</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>AVS</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>exceedPreauthAllowedInPercent</ns2:item>
                                                        <ns2:value>0</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowECI7_Connect</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>Visa</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>CUP</ns2:item>
                                                        <ns2:value>false</ns2:value>
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
                                                        <ns2:item>allowECI7_VT</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowPurchaseCards</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowCredits</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                </ns2:service>
                                                <ns2:service>
                                                    <ns2:type>installment</ns2:type>
                                                </ns2:service>
                                                <ns2:service>
                                                    <ns2:type>paymentUrl</ns2:type>
                                                </ns2:service>
                                                <ns2:service>
                                                    <ns2:type>3dSecure</ns2:type>
                                                    <ns2:config>
                                                        <ns2:item>amex3DSRequestorId</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>acquirerName</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowed3dsServerVersionMax</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowECI7onIVRPAResUifInternational</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowSplitAuthentication</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>TRAGhostCall</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowECI1andECI6</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>amexMID</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>iciciOnUsVereq</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>dinersMID</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>mc3DS2DataOnly</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>integration</ns2:item>
                                                        <ns2:value>Modirum3DSServer</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>maestroMID</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowMPIViaAPI</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>vmid</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>declineSameXIDandECI</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>transactionRiskAnalysis</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>jcbMID</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>declineSameAAV</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>mastercardMID</ns2:item>
                                                        <ns2:value>{mcmid}</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>visaMID</ns2:item>
                                                        <ns2:value>{visamid}</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowAuthenticationRetry</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowMPIViaRESTAPI</ns2:item>
                                                        <ns2:value>true</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>allowSoftDeclineRetry_Connect</ns2:item>
                                                        <ns2:value>false</ns2:value>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>visaPassword</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>excludedCardCountries</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                    <ns2:config>
                                                        <ns2:item>jcbPassword</ns2:item>
                                                        <ns2:value xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance"" xsi:nil=""true""/>
                                                    </ns2:config>
                                                </ns2:service>
                                                <ns2:terminal>
                                                    <ns2:terminalID>{TID[i]}</ns2:terminalID>
                                                    <ns2:externalMerchantID>{MID[i]}</ns2:externalMerchantID>
                                                    <ns2:endpointID>NASHVILLE MEXICO</ns2:endpointID>
                                                    <ns2:paymentMethod>MASTERCARD</ns2:paymentMethod>
                                                    <ns2:paymentMethod>VISA</ns2:paymentMethod>
                                                    <ns2:paymentMethod>MEXICOLOCAL</ns2:paymentMethod>
                                                    <ns2:transactionOrigin>ECI</ns2:transactionOrigin>
                                                    <ns2:submissionComponent>CONNECT</ns2:submissionComponent>
                                                    <ns2:payerSecurityLevel>EMPTY</ns2:payerSecurityLevel>
                                                    <ns2:payerSecurityLevel>NOT EMPTY</ns2:payerSecurityLevel>
                                                    <ns2:currency>{currency}</ns2:currency>
                                                    <ns2:active>true</ns2:active>
                                                </ns2:terminal>
                                                <ns2:purchaseLimit>
                                                    <ns2:currency>{currency}</ns2:currency>
                                                    <ns2:limit>{limit}</ns2:limit>
                                                </ns2:purchaseLimit>
                                                <ns2:fraudSettings>
                                                    <ns2:binBlockProfile>99</ns2:binBlockProfile>
                                                    <ns2:checkBlockedIP>true</ns2:checkBlockedIP>
                                                    <ns2:checkBlockedClass-C>true</ns2:checkBlockedClass-C>
                                                    <ns2:checkBlockedName>true</ns2:checkBlockedName>
                                                    <ns2:checkBlockedCard>true</ns2:checkBlockedCard>
                                                    <ns2:duplicateLockoutTimeSeconds>60</ns2:duplicateLockoutTimeSeconds>
                                                    <ns2:autoLockoutTimeSeconds>30</ns2:autoLockoutTimeSeconds>
                                                </ns2:fraudSettings>
                                            </ns2:store>
                                     </ns2:createStore>
                                  </ns2:mcsRequest>
                               </SOAP-ENV:Body>
                            </SOAP-ENV:Envelope>
                            '''
                            
                            #Petición SOAP PaymentURL
                            # Crear un ThreadPoolExecutor con un máximo de hilos
                            executor = ThreadPoolExecutor(max_workers=10)

                            peticion = realizar_solicitud_soap(baseURL, apiPassword, apiUser, certificateName, soap_xml)
                            resultados.append(peticion)

                            print('resultados',resultados)

                        if sol_type == 'Link de Pago':
                            #creacion de soap Link de Pago
                            soap_xml = f'''
                            <SOAP-ENV:Envelope xmlns:SOAP-ENV=""http://schemas.xmlsoap.org/soap/envelope/"">
                               <SOAP-ENV:Header />
                               <SOAP-ENV:Body>
                                  <ns2:mcsRequest xmlns:ns2=""http://www.ipg-online.com/mcsWebService"">
                                     <ns2:createStore>
                                         <ns2:store>
                                             <ns2:storeID>{SID[i]}</ns2:storeID>
                                             <ns2:storeAdmin>
                                                 <ns2:id>{SID[i]}</ns2:id>
                                                 <ns2:password>{storepass}</ns2:password>
                                             </ns2:storeAdmin>
                                             <ns2:mcc>{MCC[i]}</ns2:mcc>
                                                <ns2:legalName>{dba[i]}</ns2:legalName>
                                                <ns2:dba>{dba[i]}</ns2:dba>
                                                <ns2:reseller>{reseller}</ns2:reseller>
                                                <ns2:url>https://www.fiserv.com/es-mx.html</ns2:url>
                                             <ns2:defaultCurrency>{currency}</ns2:defaultCurrency>
                                             <ns2:timezone>America/Mexico_City</ns2:timezone>
                                             <ns2:status>OPEN</ns2:status>
                                             <ns2:openDate>{dtToday}</ns2:openDate>
                                             <ns2:acquirer>{acq}</ns2:acquirer>
                                             <ns2:address>
                                                 <ns2:address1>{street[i]}</ns2:address1>
                                                 <ns2:address2>{colony[i]}</ns2:address2>
                                                 <ns2:zip>{CP[i]}</ns2:zip>
                                                 <ns2:city>{city[i]}</ns2:city>
                                                 <ns2:state>{state[i]}</ns2:state>
                                                 <ns2:country>MEX</ns2:country>
                                             </ns2:address>
                                             <ns2:contact>
                                                 <ns2:name>{contact[i]}</ns2:name>
                                                 <ns2:email>{email[i]}</ns2:email>
                                                 <ns2:phone>{phone[i]}</ns2:phone>
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
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>jcbMID</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>maestroMID</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
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
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>transactionRiskAnalysis</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowECI1andECI6</ns2:item>
                                                     <ns2:value>true</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>visaPassword</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
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
                                                     <ns2:value>{visamid}</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>amexMID</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>mastercardMID</ns2:item>
                                                     <ns2:value>{mcmid}</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>vmid</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>allowed3dsServerVersionMax</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
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
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
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
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>declineSameAAV</ns2:item>
                                                     <ns2:value>false</ns2:value>
                                                 </ns2:config>
                                                 <ns2:config>
                                                     <ns2:item>jcbPassword</ns2:item>
                                                     <ns2:value xsi:nil=""true"" xmlns:xsi=""http://www.w3.org/2001/XMLSchema-instance""/>
                                                 </ns2:config>
                                             </ns2:service>
                                             <ns2:terminal>
                                                 <ns2:terminalID>{TID[i]}</ns2:terminalID>
                                                 <ns2:externalMerchantID>{MID[i]}</ns2:externalMerchantID>
                                                 <ns2:endpointID>NASHVILLE MEXICO</ns2:endpointID>
                                                 <ns2:paymentMethod>MEXICOLOCAL</ns2:paymentMethod>
                                                 <ns2:paymentMethod>MASTERCARD</ns2:paymentMethod>
                                                 <ns2:paymentMethod>VISA</ns2:paymentMethod>
                                                 <ns2:transactionOrigin>ECI</ns2:transactionOrigin>
                                                 <ns2:submissionComponent>API</ns2:submissionComponent>
                                                 <ns2:payerSecurityLevel>EMPTY</ns2:payerSecurityLevel>
                                                 <ns2:payerSecurityLevel>NOT EMPTY</ns2:payerSecurityLevel>
                                                 <ns2:currency>{currency}</ns2:currency>
                                                 <ns2:active>true</ns2:active>
                                             </ns2:terminal>
                                             <ns2:purchaseLimit>
                                                 <ns2:currency>{currency}</ns2:currency>
                                                 <ns2:limit>{limit}</ns2:limit>
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
                            node_xml=f'''
                            <SOAP-ENV:Envelope xmlns:SOAP-ENV=""http://schemas.xmlsoap.org/soap/envelope/"">
                               <SOAP-ENV:Header />
                               <SOAP-ENV:Body>
                                  <ns2:mcsRequest xmlns:ns2=""http://www.ipg-online.com/mcsWebService"">
                                     <ns2:reassignStoreInHierarchy>
                                        <ns2:merchantID>41583802634</ns2:merchantID>
                                        <ns2:storeID>{SID[i]}</ns2:storeID>
                                     </ns2:reassignStoreInHierarchy>
                                  </ns2:mcsRequest>
                               </SOAP-ENV:Body>
                            </SOAP-ENV:Envelope>
                            '''
                        #print ('xml',soap_xml)
                        #print('node_xml: ',node_xml)

                    csv_exp.append(SID)
                    csv_exp.append(MID)
                    csv_exp.append(dba)
                    csv_exp.append(storepasswords)
                    print('csv_exp: ',csv_exp)
                    
                    

                # Actualizar el cuadro de respuesta
                respuesta.config(text="Archivo cargado exitosamente", fg="green")
        except Exception as e:
            # Actualizar el cuadro de respuesta en caso de error
            respuesta.config(text="Error al cargar el archivo", fg="red")
            print(str(e))

def generar_texto_alfanumerico(longitud):
    caracteres = string.ascii_letters + string.digits + '!@#$%^&*()_+-=[]{}|;:,.<>/?'
    caracteres = caracteres.replace('~', '').replace('\\', '').replace('"', '').replace("'", "")
    texto = ''.join(random.choice(caracteres) for _ in range(longitud))
    return texto

def generar_csv(datos):
    nombre_archivo = 'carga_masiva.csv'
    with open(nombre_archivo, 'w', newline='') as archivo_csv:
        writer = csv.writer(archivo_csv)
        writer.writerows(datos)

    return send_file(nombre_archivo, as_attachment=True, attachment_filename='carga_masiva.csv')

import http.client
import ssl

def realizar_solicitud_soap(baseURL, apiPassword, apiUser, certificateName, xml):
    # Establecer la conexión
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile='ruta/al/archivo.p12', password='contraseña_del_certificado')

    conn = http.client.HTTPSConnection(baseURL, context=context)

    # Configurar los encabezados y el cuerpo de la solicitud
    headers = {
        'Content-Type': 'text/xml;charset=UTF-8',
        'SOAPAction': 'URI_de_la_acción_SOAP'
    }
    body = xml

    # Realizar la solicitud POST
    conn.request('POST', '/', headers=headers, body=body, auth=(apiUser, apiPassword))

    # Obtener la respuesta
    response = conn.getresponse()

    if response.status == 200:
        respuesta = response.read()
        # Procesar la respuesta como desees
        return respuesta.decode('utf-8')
    else:
        # Manejar el caso de una respuesta no exitosa
        return f'Error en la solicitud: {response.status} {response.reason}'


# Crear la ventana principal
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

# Botón descargable
btn_descargar = tk.Button(
    ventana,
    text="Descargar CSV",
    command=generar_csv,
    font=estilo_fuente,
    bg="brown",
    fg="white",
    relief=tk.FLAT
)
btn_descargar.pack(pady=10)

# Ajustar tamaño de la ventana
ventana.geometry("400x350")

# Ejecutar la aplicación
ventana.mainloop()
