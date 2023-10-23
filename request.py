import requests
import xml.etree.ElementTree as ET

celcius = "-20"

url = "https://www.w3schools.com/xml/tempconvert.asmx"

SOAPEnvelope = '''
<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
  <soap:Body>
    <CelsiusToFahrenheit xmlns="https://www.w3schools.com/xml/">
      <Celsius>20</Celsius>
    </CelsiusToFahrenheit>
  </soap:Body>
</soap:Envelope>
'''

options = {
    'Content-Type':"text/xml; charset=utf-8"
}

response = requests.post(url, data=SOAPEnvelope, headers=options)

print ("holiwis \n")

root = ET.fromstring(response.text)

for child in root.iter("*"):
   C2F = child.text
   print(C2F)
